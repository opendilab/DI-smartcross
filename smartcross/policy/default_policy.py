from typing import Dict, List, Any
import torch
import numpy as np
from easydict import EasyDict
import copy

from ding.utils import POLICY_REGISTRY


@POLICY_REGISTRY.register('smartcross_random')
class RandomPolicy():

    config = dict()

    def __init__(self, act_space: Any) -> None:
        self._act_space = act_space

    def reset(self, *args, **keargs) -> None:
        pass

    def get_random_action(self) -> List:
        action = self._act_space.sample()
        action = [torch.LongTensor([v]) for v in action]
        return action

    def forward(self, data: Dict) -> Dict[int, Dict]:
        data_id = list(data.keys())
        output = {}
        for i in data_id:
            action = self.get_random_action()
            output[i] = {'action': action}
        return output

    @classmethod
    def default_config(cls: type) -> EasyDict:
        cfg = EasyDict(copy.deepcopy(cls.config))
        cfg.cfg_type = cls.__name__ + 'Dict'
        return cfg


def get_random_sample_func(act_space):
    def _forward(data: Dict[int, Any], *args, **kwargs) -> Dict[int, Any]:
        actions = {}
        for env_id in data:
            action = act_space.sample()
            action = [torch.LongTensor([v]) for v in action]
            actions[env_id] = {'action': action}
        return actions
    return _forward


@POLICY_REGISTRY.register('smartcross_fix')
class FixedPolicy():

    config = dict()

    def __init__(self, act_space: Any) -> None:
        self._act_space = act_space
        self._nvec = self._act_space.nvec
        self._last_act = {}

    def reset(self, *args, **keargs) -> None:
        self._last_act.clear()

    def get_next_action(self, i: int) -> List:
        if i not in self._last_act:
            action = np.zeros(self._act_space.shape)
        else:
            action = self._last_act[i] + 1
            action[action >= self._nvec] = 0
        self._last_act[i] = action
        action = [torch.LongTensor([v]) for v in action]
        return action

    def forward(self, data: Dict) -> Dict[int, Dict]:
        data_id = list(data.keys())
        output = {}
        for i in data_id:
            action = self.get_next_action(i)
            output[i] = {'action': action}
        return output

    @classmethod
    def default_config(cls: type) -> EasyDict:
        cfg = EasyDict(copy.deepcopy(cls.config))
        cfg.cfg_type = cls.__name__ + 'Dict'
        return cfg
