import os
import json
import numpy as np
from typing import Dict, Any, List, Tuple, Union

import cityflow

from ding.envs import BaseEnv, BaseEnvTimestep, BaseEnvInfo
from ding.envs.common.env_element import EnvElementInfo
from ding.utils import ENV_REGISTRY
from ding.torch_utils import to_ndarray
from smartcross.utils.env_utils import get_suffix_num, squeeze_obs, get_onehot_obs


@ENV_REGISTRY.register('cityflow_env')
class CityflowEnv(BaseEnv):

    def __init__(self, cfg: Dict) -> None:
        self._cfg = cfg
        self._config_path = cfg.config_path
        self._obs_type = cfg.obs_type
        self._max_episode_duration = cfg.max_episode_duration
        self._green_duration = cfg.green_duration
        self._yellow_duration = cfg.yellow_duration
        self._red_duration = cfg.red_duration
        self._debug = cfg.debug
        self._eng = cityflow.Engine(self._config_path)
        self._parse_config_file()
        self._init_info()
    
    def _parse_config_file(self):
        with open(self._config_path, 'r') as fc:
            file_config = json.load(fc)
            
        roadnet_file = os.path.join(file_config['dir'], file_config['roadnetFile'])
        with open(roadnet_file, 'r') as fr:
            roadnet_config = json.load(fr)

        self._crossing_in_roads = {}
        self._crossing_out_roads = {}
        self._crossing_phases = {}
        crossings_config = roadnet_config['intersections']
        for item in crossings_config:
            if item['virtual']:
                continue
            crossing_id = item['id']
            self._crossing_in_roads[crossing_id] = []
            self._crossing_out_roads[crossing_id] = []
            crossing_id_num = get_suffix_num(crossing_id)
            crossing_roads = item['roads']
            for road_id in crossing_roads:
                road_id_num = get_suffix_num(road_id)
                if road_id_num[0] == crossing_id_num[0] and road_id_num[1] == crossing_id_num[1]:
                    self._crossing_out_roads[crossing_id].append(road_id)
                else:
                    self._crossing_in_roads[crossing_id].append(road_id)
            self._crossing_phases[crossing_id] = {'G':[], 'Y':[], 'R':[]}
            light_phases = item['trafficLight']['lightphases']
            for id, it in enumerate(light_phases):
                if len(it['availableRoadLinks']) > 4:
                    self._crossing_phases[crossing_id]['G'].append(id)
                elif len(it['availableRoadLinks']) == 4:
                    self._crossing_phases[crossing_id]['Y'].append(id)
                elif len(it['availableRoadLinks']) == 0:
                    self._crossing_phases[crossing_id]['R'].append(id)
                else:
                    print("Unrecognized phase!")
            
        self._crossings = list(self._crossing_in_roads.keys())
        self._road_lanes = {}
        all_lanes = list(self._eng.get_lane_vehicle_count().keys())

        for road in roadnet_config['roads']:
            road_id = road['id']
            self._road_lanes[road_id] = []
        
        for lane in all_lanes:
            self._road_lanes[lane[:-2]].append(lane)
    
    def _init_info(self):
        obs_len = 0
        act_shape = []
        if 'phase' in self._obs_type:
            for cross in self._crossing_phases:
                obs_len += len(self._crossing_phases[cross]['G'])
        if 'lane_vehicle_num' in self._obs_type:
            for road in self._crossing_in_roads.values():
                for r in road:
                    obs_len += len(self._road_lanes[r])
        if 'lane_waiting_vehicle_num' in self._obs_type:
            for road in self._crossing_in_roads.values():
                for r in road:
                    obs_len += len(self._road_lanes[r])
        for cross in self._crossings:
            act_shape.append(len(self._crossing_phases[cross]['G']))
        self._obs_shape = obs_len
        self._action_shape = act_shape
    
    def _get_obs(self) -> Dict:
        obs = {cross: [] for cross in self._crossings}
        if 'phase' in self._obs_type:
            for cross in self._crossing_phases:
                onehot_phase = [0] * len(self._crossing_phases[cross]['G'])
                ph = self._current_phases[cross]
                onehot_phase[ph] = 1
                obs[cross] += onehot_phase
        if 'lane_vehicle_num' in self._obs_type:
            all_lane_vehicle_num = self._eng.get_lane_vehicle_count()
            for cross, roads in self._crossing_in_roads.items():
                vehicle_nums = []
                for k, v in all_lane_vehicle_num.items():
                    if k[:-2] in roads:
                        vehicle_nums.append(v)
                obs[cross] += vehicle_nums
        if 'lane_waiting_vehicle_num' in self._obs_type:
            all_lane_waiting_vehicle = self._eng.get_lane_waiting_vehicle_count()
            for cross, roads in self._crossing_in_roads.items():
                vehicle_nums = []
                for k, v in all_lane_waiting_vehicle.items():
                    if k[:-2] in roads:
                        vehicle_nums.append(v)
                obs[cross] += vehicle_nums
        return obs
    
    def _get_reward(self):
        reward = {cross: 0 for cross in self._crossings}
        all_lane_waiting_vehicle = self._eng.get_lane_waiting_vehicle_count()
        for cross in self._crossings:
            cross_reward = 0
            for roads in self._crossing_in_roads.values():
                for k, v in all_lane_waiting_vehicle.items():
                    if k[:-2] in roads:
                        cross_reward += v
            for roads in self._crossing_out_roads.values():
                for k, v in all_lane_waiting_vehicle.items():
                    if k[:-2] in roads:
                        cross_reward -= v
            reward[cross] = -cross_reward
        return reward
    
    def _process_action(self, raw_action):
        raw_action = np.squeeze(raw_action)
        if self._last_action is None:
            self._last_action = [None for _ in range(len(raw_action))]
        data = {}
        for intersec_id, act, last_act in zip(self._crossings, raw_action, self._last_action):
            data[intersec_id] = {'action': act, 'last_action': last_act}
        action = {k: {} for k in data.keys()}
        for k, v in data.items():
            act, last_act = v['action'], v['last_action']
            if last_act is not None and act != last_act:
                yellow_phase = self._env.crosses[k].get_yellow_phase_index(last_act)
            else:
                yellow_phase = None
            action[k]['yellow'] = yellow_phase
            action[k]['green'] = self._env.crosses[k].get_green_phase_index(act)
        return action

    def _simulate(self, action):
        changed_tl_id = {}
        for act, (cross, cur_act) in zip(action, self._current_phases.items()):
            if act == cur_act:
                new_phase = self._crossing_phases[cross]['G'][act]
                self._eng.set_tl_phase(cross, new_phase)
                self._current_phases[cross] = int(act)
            else:
                changed_tl_id[cross] = (act, cur_act)

        if len(changed_tl_id) == 0:
            for t in range(self._red_duration + self._yellow_duration + self._green_duration):
                self._eng.next_step()
        else:
            if self._red_duration > 0:
                for cross in changed_tl_id:
                    red_phase = self._crossing_phases[cross]['R'][0]
                    self._eng.set_tl_phase(cross, red_phase)
                for t in range(self._red_duration):
                    self._eng.next_step()
            if self._yellow_duration > 0:
                for cross, (act, cur_act) in changed_tl_id.items():
                    yellow_phase = self._crossing_phases[cross]['Y'][cur_act]
                    self._eng.set_tl_phase(cross, yellow_phase)
                for t in range(self._yellow_duration):
                    self._eng.next_step()
            for cross, (act, cur_act) in changed_tl_id.items():
                green_phase = self._crossing_phases[cross]['G'][act]
                self._eng.set_tl_phase(cross, green_phase)
                self._current_phases[cross] = int(act)
            for t in range(self._green_duration):
                    self._eng.next_step()
        
        self._total_duration += self._red_duration + self._yellow_duration + self._green_duration
        
    def reset(self) -> Any:
        self._eng.reset()
        self._total_duration = 0
        self._total_reward = 0
        self._current_phases = {}
        for cross in self._crossings:
            phase = self._crossing_phases[cross]['G'][0]
            self._eng.set_tl_phase(cross, phase)
            self._current_phases[cross] = 0
        obs = self._get_obs()
        return to_ndarray(squeeze_obs(obs), dtype=np.float32)

    def step(self, action: Any) -> 'BaseEnvTimestep':
        action = np.squeeze(action)
        self._simulate(action)
        obs = self._get_obs()
        obs = to_ndarray(squeeze_obs(obs), dtype=np.float32)
        reward = self._get_reward()
        reward = to_ndarray(sum(reward.values()), dtype=np.float32)
        self._total_reward += reward
        done = self._total_duration > self._max_episode_duration
        info = {}
        if done:
            info['final_eval_reward'] = self._total_reward
            self.close()
        return BaseEnvTimestep(obs, reward, done, info)
    
    def close(self) -> None:
        return 
    
    def seed(self, seed: int, dynamic_seed: bool = True) -> None:
        self._seed = seed
        self._dynamic_seed = dynamic_seed
    
    def info(self) -> 'BaseEnvInfo':
        info_data = {
            'agent_num': 1,
            'obs_space': EnvElementInfo(
                shape=self._obs_shape,
                value={'min': 0, 'max': float('inf')},
            ),
            'act_space': EnvElementInfo(
                shape=len(self._crossings), 
                value={'min': 0, 'max': self._action_shape[0], 'dtype': int},
            ),
            'rew_space': 1,
            'use_wrappers': False,
        }
        return BaseEnvInfo(**info_data)
    
    def __repr__(self) -> str:
        return "CityFlowEnv"