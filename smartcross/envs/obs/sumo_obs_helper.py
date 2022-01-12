from typing import Dict

from ding.envs import BaseEnv
from ding.envs.common.env_element import EnvElementInfo

ALL_OBS_TPYE = set(['phase', 'lane_pos_vec', 'traffic_volumn', 'queue_len'])


class SumoObsHelper():

    def __init__(self, core: BaseEnv, cfg: Dict):
        self._core = core
        self._cfg = cfg
        self._obs_type = self._cfg.obs_type
        assert set(self._obs_type).issubset(ALL_OBS_TPYE)
        self._use_centralized_obs = self._cfg.use_centralized_obs
        self._padding = self._cfg.padding

    def init_info(self):
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

        self._global_state_shape = obs_shape
        if self._padding:
            self._tl_feature_shape = tl_obs_max_dict
            self._agent_state_shape = sum(self._tl_feature_shape.values())
        else:
            self._agent_state_shape = max(obs_shape)
        self._obs_shape = {
            'agent_state': self._agent_state_shape,
            'global_state': self._global_state_shape,
        }
        self._obs_value = {
            'min': 0,
            'max': 1,
            'dtype': float,
        }

    def _get_tls_feature(self, tl_id):
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
            tl_obs['queue_len'] += list(cross.get_lane_queue_len(self._queue_len_ratio).values())
        return tl_obs

    def get_observation(self):
        obs = {}
        for tl in self._core.crosses.keys():
            tl_obs = self._get_tls_feature(tl)
            if self._padding:
                tl_obs = padding_obs_by_fearure(tl_obs, self._tl_feature_shape)
            obs[tl] = tl_obs
        return obs

    def info(self, centralized=False):
        if centralized:
            obs_shape = sum(self._global_state_shape)
            return EnvElementInfo(obs_shape, self._obs_value)
        return EnvElementInfo(self._obs_shape, self._obs_value)


def max_dict(dict1: Dict, dict2: Dict) -> Dict:
    assert len(dict1) == len(dict2)
    for k, v in dict1.items():
        assert k in dict2
        if isinstance(v, dict):
            dict1[k] = max_dict(dict1[k], dict2[k])
        else:
            dict1[k] = max(dict1[k], dict2[k])
    return dict1


def padding_obs_by_fearure(tl_obs, tl_feature_shape):
    for feature in tl_obs:
        if len(tl_obs[feature]) < tl_feature_shape[feature]:
            tl_obs[feature] += [0] * (tl_feature_shape[feature] - len(tl_obs[feature]))
    return tl_obs
