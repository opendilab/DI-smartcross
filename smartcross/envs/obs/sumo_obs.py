from typing import Dict, List
import numpy as np

from ding.envs import BaseEnv
from ding.envs.common.env_element import EnvElementInfo
from ding.envs.common import EnvElement

ALL_OBS_TPYE = set(['phase', 'lane_pos_vec', 'traffic_volumn', 'queue_len'])


class SumoObs(EnvElement):
    r"""
    Overview:
        the observation element of Sumo enviroment

    Interface:
        _init, to_agent_processor
    """

    _name = "SumoObs"

    def _init(self, env: BaseEnv, cfg: Dict) -> None:
        self._core = env
        self._cfg = cfg
        self._tl_num = len(self._core.crosses)
        self._obs_type = self._cfg.obs_type
        assert set(self._obs_type).issubset(ALL_OBS_TPYE)
        self._use_centralized_obs = self._cfg.use_centralized_obs
        self._padding = self._cfg.padding

        obs_shape = []
        tl_obs_max_dict = None
        for tl, cross in self._core.crosses.items():
            tl_obs_shape_map = {}
            if 'phase' in self._obs_type:
                tl_obs_shape_map['phase'] = cross.phase_num
            if 'lane_pos_vec' in self._obs_type:
                self._lane_grid_num = self._cfg.lane_grid_num
                tl_obs_shape_map['lane_pos_vec'] = cross.lane_num * self._lane_grid_num
            if 'traffic_volumn' in self._obs_type:
                tl_obs_shape_map['traffic_volumn'] = cross.lane_num
            if 'queue_len' in self._obs_type:
                self._queue_len_ratio = self._cfg.queue_len_ratio
                tl_obs_shape_map['queue_len'] = cross.lane_num
            obs_shape.append(sum(tl_obs_shape_map.values()))

            if tl_obs_max_dict is None:
                tl_obs_max_dict = tl_obs_shape_map
            else:
                tl_obs_max_dict = max_dict(tl_obs_max_dict, tl_obs_shape_map)

        if self._use_centralized_obs:
            self._shape = sum(obs_shape)
        else:
            global_state_shape = sum(obs_shape)
            if self._padding:
                self._tl_feature_shape = tl_obs_max_dict
                agent_state_shape = sum(self._tl_feature_shape.values())
            else:
                agent_state_shape = max(obs_shape)
            self._shape = {
                'agent_state': agent_state_shape,
                'global_state': global_state_shape,
                'action_mask': self._tl_num
            }
        self._value = {
            'min': 0,
            'max': 1,
            'dtype': float,
        }

    def _get_tls_feature(self, tl_id: int) -> Dict:
        cross = self._core.crosses[tl_id]
        tl_obs = {}
        if 'phase' in self._obs_type:
            tl_obs['phase'] = cross.get_onehot_phase()
        if 'lane_pos_vec' in self._obs_type:
            tl_obs['lane_pos_vec'] = [
                ele for lst in cross.get_lane_vehicle_pos_vector(self._lane_grid_num).values() for ele in lst
            ]
        if 'traffic_volumn' in self._obs_type:
            tl_obs['traffic_volumn'] = list(cross.get_lane_traffic_volumn().values())
        if 'queue_len' in self._obs_type:
            tl_obs['queue_len'] = list(cross.get_lane_queue_len(self._queue_len_ratio).values())
        return tl_obs

    def _to_agent_processor(self) -> Dict:
        obs = {}
        tl_num = len(self._core.crosses)
        for tl in self._core.crosses.keys():
            tl_obs = self._get_tls_feature(tl)
            obs[tl] = tl_obs
        global_obs = squeeze_obs(obs)
        if self._use_centralized_obs:
            return global_obs
        else:
            agent_obs = []
            for tl, tl_obs in obs.items():
                if self._padding:
                    tl_obs = padding_obs_by_fearure(tl_obs, self._tl_feature_shape)
                tl_obs = [element for lis in tl_obs.values() for element in lis]
                agent_obs.append(tl_obs)
            action_num = self._core.info().act_space.value['max']
            action_mask = [1] * action_num
            return {
                'global_state': np.array([global_obs] * tl_num),
                'agent_state': np.array(agent_obs),
                'action_mask': np.array([action_mask] * tl_num)
            }

    def __repr__(self) -> str:
        return '{}: {}'.format(self._name, self._details())

    def _details(self) -> str:
        return '{}'.format(self._shape)


def max_dict(dict1: Dict, dict2: Dict) -> Dict:
    assert len(dict1) == len(dict2)
    for k, v in dict1.items():
        assert k in dict2
        if isinstance(v, dict):
            dict1[k] = max_dict(dict1[k], dict2[k])
        else:
            dict1[k] = max(dict1[k], dict2[k])
    return dict1


def padding_obs_by_fearure(tl_obs: Dict, tl_feature_shape: Dict) -> Dict:
    for feature in tl_obs:
        if len(tl_obs[feature]) < tl_feature_shape[feature]:
            tl_obs[feature] += [0] * (tl_feature_shape[feature] - len(tl_obs[feature]))
    return tl_obs


def squeeze_obs(obs: Dict) -> List:
    assert obs is not None
    if isinstance(obs, dict):
        return [value for key in sorted(obs) for value in squeeze_obs(obs[key])]
    elif isinstance(obs, (tuple, list, set)):
        return [value for item in obs for value in squeeze_obs(item)]
    elif isinstance(obs, (int, float, str)):
        return (obs, )
    else:
        raise ValueError('Cannot process type: {}, {}'.format(type(obs), obs))
