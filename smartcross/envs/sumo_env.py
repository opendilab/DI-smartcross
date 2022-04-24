import os
import sys
import time
import gym
from typing import Dict, Any, List, Tuple, Union
import numpy as np
import random

import traci
from sumolib import checkBinary

from ding.envs import BaseEnv, BaseEnvTimestep  # , BaseEnvInfo
from ding.utils import ENV_REGISTRY
from ding.torch_utils import to_ndarray, to_tensor
from smartcross.envs.crossing import Crossing
from smartcross.envs.obs import SumoObsRunner
from smartcross.envs.action import SumoActionRunner
from smartcross.envs.reward import SumoRewardRunner
from smartcross.utils.config_utils import get_sumocfg_inputs


@ENV_REGISTRY.register('sumo_env')
class SumoEnv(BaseEnv):

    def __init__(self, cfg: Dict) -> None:
        self._cfg = cfg
        self._sumocfg_path = os.path.dirname(__file__) + '/' + cfg.sumocfg_path
        self._sumo_inputs = get_sumocfg_inputs(self._sumocfg_path)
        self._gui = cfg.get('gui', False)
        self._dynamic_flow = cfg.get('dynamic_flow', False)
        if self._dynamic_flow:
            self._flow_range = cfg.flow_range
        self._tls = cfg.tls
        self._max_episode_steps = cfg.max_episode_steps
        self._yellow_duration = cfg.yellow_duration
        self._green_duration = cfg.green_duration

        self._launch_env_flag = False
        self._crosses = {}
        self._vehicle_info_dict = {}
        self._label = str(int(time.time() * (10 ** 6)))[-6:]

        self._launch_env(False)
        for tl in self._cfg.tls:
            self._crosses[tl] = Crossing(tl, self)
        self._obs_runner = SumoObsRunner(self, cfg.obs)
        self._action_runner = SumoActionRunner(self, cfg.action)
        self._reward_runner = SumoRewardRunner(self, cfg.reward)
        self.close()
        self._observation_space = self._obs_runner.space
        self._action_space = self._action_runner.space
        self._reward_space = gym.spaces.Box(low=-float('inf'), high=0, shape=(1, ), dtype=np.float32)

    def _launch_env(self, gui: bool = False) -> None:
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
        sumo_cmd = [sumoBinary]
        for k, v in self._sumo_inputs.items():
            sumo_cmd.append('--' + k)
            sumo_cmd.append(v)
        sumo_cmd.append("--no-warnings")
        sumo_cmd.append("--no-step-log")
        traci.start(sumo_cmd, label=self._label)
        self._launch_env_flag = True

    def _simulate(self, action: Dict) -> None:
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

    def _set_route_flow(self, route_flow: int) -> None:
        assert 'route-files' in self._sumo_inputs
        rf_old = self._sumo_inputs['route-files']
        rf_parent = os.path.split(os.path.split(rf_old)[0])[0]
        rf_folder = os.path.join(rf_parent, str(route_flow))
        rf_list = [f for f in os.listdir(rf_folder) if f[-3:] == 'xml']
        rf_new_flow = random.choice(rf_list)
        rf_new = os.path.join(rf_folder, rf_new_flow)
        self._sumo_inputs['route-files'] = rf_new
        print("reset sumocfg file to ", route_flow)

    def reset(self) -> Any:
        self._current_steps = 0
        self._total_reward = 0
        self._last_action = None
        if self._dynamic_flow:
            route_flow = random.choice(list(range(*self._flow_range)))
            self._set_route_flow(route_flow)
        self._crosses.clear()
        self._vehicle_info_dict.clear()
        self._action_runner.reset()
        self._obs_runner.reset()
        self._reward_runner.reset()
        if self._launch_env_flag:
            self.close()
        self._launch_env(self._gui)
        for tl in self._cfg.tls:
            self._crosses[tl] = Crossing(tl, self)
            self._crosses[tl].update_timestep()
        return self._obs_runner.get()

    def step(self, action: Any) -> 'BaseEnv.timestep':
        action_per_tl = self._action_runner.get(action)
        self._simulate(action_per_tl)
        for cross in self._crosses.values():
            cross.update_timestep()
        obs = self._obs_runner.get()
        reward = self._reward_runner.get()
        self._total_reward += reward
        done = self._current_steps > self._max_episode_steps
        info = {}
        if done:
            info['final_eval_reward'] = self._total_reward
            self.close()
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

    # def info(self) -> 'BaseEnvInfo':
    #     info_data = {
    #         'agent_num': len(self._tls),
    #         'obs_space': self._obs_runner.info,
    #         'act_space': self._action_runner.info,
    #         'rew_space': self._reward_runner.info,
    #         'use_wrappers': False
    #     }
    #     return BaseEnvInfo(**info_data)

    def __repr__(self) -> str:
        return "SumoEnv"

    @property
    def observation_space(self) -> gym.spaces.Space:
        return self._observation_space

    @property
    def action_space(self) -> gym.spaces.Space:
        return self._action_space

    @property
    def reward_space(self) -> gym.spaces.Space:
        return self._reward_space

    @property
    def vehicle_info(self) -> Dict[str, Dict]:
        return self._vehicle_info_dict

    @property
    def crosses(self) -> Dict[int, Crossing]:
        return self._crosses

    @property
    def duration(self) -> Tuple[float]:
        return self._green_duration, self._yellow_duration
