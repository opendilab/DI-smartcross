from typing import Dict
import numpy as np

from ding.envs import BaseEnv
from ding.envs.common import EnvElement

ALL_REWARD_TYPE = set(['queue_len', 'wait_time', 'delay_time', 'pressure'])


class SumoReward(EnvElement):
    r"""
    Overview:
        the reward element of Sumo enviroment

    Interface:
        _init, to_agent_processor
    """
    _name = "SumoReward"

    def _init(self, env: BaseEnv, cfg: Dict) -> None:
        r"""
        Overview:
            init the sumo reward environment with the given config file
        Arguments:
            - cfg(:obj:`EasyDict`): config, you can refer to `envs/sumo/sumo_env_default_config.yaml`
        """
        self._env = env
        self._cfg = cfg
        self._reward_type = cfg.reward_type
        assert set(self._reward_type.keys()).issubset(ALL_REWARD_TYPE)
        self._use_centralized_reward = cfg.use_centralized_reward
        if self._use_centralized_reward:
            self._shape = (1, )
        else:
            raise NotImplementedError
        self._value = {'min': '-inf', 'max': 'inf', 'dtype': float}

    def _to_agent_processor(self):
        reward = {k: 0 for k in self._env.crosses.keys()}
        for k in self._env.crosses.keys():
            cross = self._env.crosses[k]
            if 'queue_len' in self._reward_type:
                queue_len = np.average(list(cross.get_lane_queue_len().values()))
                reward[k] += self._reward_type['queue_len'] * -queue_len
            if 'wait_time' in self._reward_type:
                wait_time = np.average(list(cross.get_lane_wait_time().values()))
                reward[k] += self._reward_type['wait_time'] * -wait_time
            if 'delay_time' in self._reward_type:
                delay_time = np.average(list(cross.get_lane_delay_time().values()))
                reward[k] += self._reward_type['delay_time'] * -delay_time
            if 'pressure' in self._reward_type:
                pressure = cross.get_pressure()
                reward[k] += self._reward_type['pressure'] * -pressure
        if self._use_centralized_reward:
            reward = sum(reward.values())
        return reward

    # override
    def _details(self):
        return '{}'.format(self._shape)
