import os
import sys
import time
from typing import Dict, Any
import numpy as np

import traci
from sumolib import checkBinary

from ding.envs import BaseEnv, BaseEnvTimestep, BaseEnvInfo
from ding.envs.common.env_element import EnvElementInfo
from ding.utils import ENV_REGISTRY
from ding.torch_utils import to_ndarray, to_tensor
from smartcross.envs.crossing import Crossing
from smartcross.envs.obs.sumo_obs_helper import SumoObsHelper
from smartcross.utils.config_utils import set_route_flow

ALL_OBS_TPYE = set(['phase', 'lane_pos_vec', 'traffic_volumn', 'queue_len'])
ALL_ACTION_TYPE = set(['change'])
ALL_REWARD_TYPE = set(['queue_len', 'wait_time', 'delay_time', 'pressure'])


@ENV_REGISTRY.register('sumo_env')
class SumoEnv(BaseEnv):

    def __init__(self, cfg: Dict) -> None:
        self._cfg = cfg
        self._sumocfg_path = os.path.dirname(__file__) + '/' + cfg.sumocfg_path
        self._gui = cfg.get('gui', False)
        self._dynamic_flow = cfg.get('dynamic_flow', False)
        if self._dynamic_flow:
            self._flow_range = cfg.flow_range
        self._tls = cfg.tls
        self._max_episode_steps = cfg.max_episode_steps
        self._yellow_duration = cfg.yellow_duration
        self._green_duration = cfg.green_duration

        self._action_type = cfg.action.action_type
        self._reward_type = cfg.reward.reward_type
        assert self._action_type in ALL_ACTION_TYPE
        assert set(self._reward_type.keys()).issubset(ALL_REWARD_TYPE)

        self._use_multi_discrete = cfg.action.use_multi_discrete
        self._use_centralized_reward = cfg.reward.use_centralized_reward

        self._launch_env_flag = False
        self._crosses = {}
        self._vehicle_info_dict = {}
        self._label = str(int(time.time() * (10 ** 6)))[-6:]

        self._launch_env(False)
        for tl in self._cfg.tls:
            self._crosses[tl] = Crossing(tl, self)
        self._obs_helper = SumoObsHelper(self, cfg.obs)
        self._init_info()
        self.close()

    def _launch_env(self, gui=False):
        # set gui=True can get visualization simulation result with sumo, apply gui=False in the normal training
        # and test setting

        # sumo things - we need to import python modules from the $SUMO_HOME/tools directory
        if 'SUMO_HOME' in os.environ:
            tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
            sys.path.append(tools)
        else:
            sys.exit("please declare environment variable 'SUMO_HOME'")

        # setting the cmd mode or the visual mode
        if gui is False:
            sumoBinary = checkBinary('sumo')
        else:
            sumoBinary = checkBinary('sumo-gui')

        # setting the cmd command to run sumo at simulation time
        sumo_cmd = [
            sumoBinary,
            "-c",
            self._sumocfg_path,
            "--no-step-log",
            "--no-warnings",
        ]
        traci.start(sumo_cmd, label=self._label)
        self._launch_env_flag = True

    def _init_info(self):
        self._obs_helper.init_info()
        action_shape = []
        for tl, cross in self._crosses.items():
            if self._action_type == 'change':
                action_shape.append(cross.phase_num)
            else:
                # TODO: add switch action
                raise NotImplementedError
        if self._use_multi_discrete:
            self._action_shape = action_shape
        else:
            # TODO: add naive discrete action
            raise NotImplementedError
        self._action_value = {
            'min': 0,
            'max': self._action_shape[0],
            'dtype': int,
        }

    def _get_observation(self):
        for cross in self._crosses.values():
            cross.update_timestep()
        obs = self._obs_helper.get_observation()
        return obs

    def _get_action(self, raw_action):
        raw_action = np.squeeze(raw_action)
        if self._last_action is None:
            self._last_action = [None for _ in range(len(raw_action))]
        action = {tl: {} for tl in self._tls}
        for tl, act, last_act in zip(self._tls, raw_action, self._last_action):
            if last_act is not None and act != last_act:
                yellow_phase = self._crosses[tl].get_yellow_phase_index(last_act)
            else:
                yellow_phase = None
            action[tl]['yellow'] = yellow_phase
            action[tl]['green'] = self._crosses[tl].get_green_phase_index(act)
        self._last_action = raw_action
        return action

    def _get_reward(self):
        reward = {tl: 0 for tl in self._tls}
        for tl in self._tls:
            cross = self._crosses[tl]
            if 'queue_len' in self._reward_type:
                queue_len = np.average(list(cross.get_lane_queue_len().values()))
                reward[tl] += self._reward_type['queue_len'] * -queue_len
            if 'wait_time' in self._reward_type:
                wait_time = np.average(list(cross.get_lane_wait_time().values()))
                reward[tl] += self._reward_type['wait_time'] * -wait_time
            if 'delay_time' in self._reward_type:
                delay_time = np.average(list(cross.get_lane_delay_time().values()))
                reward[tl] += self._reward_type['delay_time'] * -delay_time
            if 'pressure' in self._reward_type:
                pressure = cross.get_pressure()
                reward[tl] += self._reward_type['pressure'] * -pressure
        if self._use_centralized_reward:
            reward = sum(reward.values())
        return reward

    def _simulate(self, action):
        for tl, a in action.items():
            yellow_phase = a['yellow']
            if yellow_phase is not None:
                self._crosses[tl].set_phase(yellow_phase, self._yellow_duration)
        self._current_steps += self._yellow_duration
        traci.simulationStep(self._current_steps)

        for tl, a in action.items():
            green_phase = a['green']
            self._crosses[tl].set_phase(green_phase, self._yellow_duration + self._green_duration + 1)
        self._current_steps += self._green_duration
        traci.simulationStep(self._current_steps)

    def _set_route_flow(self, route_flow):
        self._sumocfg_path = set_route_flow(
            os.path.dirname(__file__) + '/' + self._cfg.sumocfg_path, route_flow, self._label
        )
        self._route_flow = route_flow
        print("reset sumocfg file to ", self._sumocfg_path)

    def reset(self) -> Any:
        self._current_steps = 0
        self._total_reward = 0
        self._last_action = None
        if self._dynamic_flow:
            route_flow = np.random.randint(*self._flow_range) * 100
            self._set_route_flow(route_flow)
        self._crosses.clear()
        self._vehicle_info_dict.clear()
        self._launch_env(self._gui)
        for tl in self._cfg.tls:
            self._crosses[tl] = Crossing(tl, self)
        return to_ndarray(self._get_observation(), dtype=np.float32)

    def step(self, action: Any) -> 'BaseEnv.timestep':
        action_per_tl = self._get_action(action)
        self._simulate(action_per_tl)
        obs = self._get_observation()
        reward = self._get_reward()
        if self._use_centralized_reward:
            self._total_reward += reward
        else:
            self._total_reward += sum(reward.values())
        done = self._current_steps > self._max_episode_steps
        info = {}
        if done:
            info['final_eval_reward'] = self._total_reward
            self.close()
        obs = to_ndarray(obs, dtype=np.float32)
        reward = to_ndarray([reward], dtype=np.float32)
        return BaseEnvTimestep(obs, reward, done, info)

    def seed(self, seed: int, dynamic_seed: bool = True) -> None:
        self._seed = seed
        self._dynamic_seed = dynamic_seed
        np.random.seed(self._seed)

    def close(self) -> None:
        r"""
        close traci, set launch_env_flag as False
        """
        if self._launch_env_flag:
            self._launch_env_flag = False
            traci.close()

    def info(self) -> 'BaseEnvInfo':
        info_data = {
            'agent_num': len(self._tls),
            'obs_space': self._obs_helper.info(),
            'act_space': EnvElementInfo(shape=[len(self._action_shape)], value=self._action_value),
            'rew_space': len(self._tls),
            'use_wrappers': False
        }
        return BaseEnvInfo(**info_data)

    def __repr__(self) -> str:
        return "SumoEnv"

    @property
    def vehicle_info(self):
        return self._vehicle_info_dict

    @property
    def crosses(self):
        return self._crosses


def squeeze(obs):
    res = []
    for tl, tl_obs in obs.itmes():
        res += tl_obs
    return res
