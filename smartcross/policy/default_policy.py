from typing import Dict, List
import torch
import numpy as np
from easydict import EasyDict
import copy

from ding.utils import POLICY_REGISTRY
from ding.envs.common import EnvElementInfo


@POLICY_REGISTRY.register('smartcross_random')
class RandomPolicy():

    config = dict()

    def __init__(self, act_space: EnvElementInfo) -> None:
        self._act_space = act_space
        self._min_val = self._act_space.value['min']
        self._max_val = self._act_space.value['max']
        self._act_shape = act_space.shape

    def reset(self, *args, **keargs) -> None:
        pass

    def get_random_action(self) -> List:
        action = np.random.randint(self._min_val, self._max_val, self._act_shape)
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


@POLICY_REGISTRY.register('smartcross_fix')
class FixedPolicy():

    config = dict()

    def __init__(self, act_space: EnvElementInfo) -> None:
        self._act_space = act_space
        self._min_val = self._act_space.value['min']
        self._max_val = self._act_space.value['max']
        self._act_shape = act_space.shape
        self._last_act = {}

    def reset(self, *args, **keargs) -> None:
        self._last_act.clear()

    def get_next_action(self, i: int) -> List:
        if i not in self._last_act:
            action = np.zeros(self._act_shape)
        else:
            action = self._last_act[i] + 1
            action[action >= self._max_val] = 0
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
