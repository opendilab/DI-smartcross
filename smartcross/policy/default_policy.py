import torch
import random
from easydict import EasyDict
import copy

from ding.utils import POLICY_REGISTRY


@POLICY_REGISTRY.register('smartcross_random')
class RandomPolicy():

    config = dict()

    def __init__(self, act_space):
        self._act_space = act_space

    def reset(self, *args, **keargs):
        pass

    def get_random_action(self):
        action = []
        for k in self._act_space:
            action.append(random.choice(list(range(k))))
        action = [torch.LongTensor([v]) for v in action]
        return action

    def forward(self, data):
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

    def __init__(self, act_space):
        self._act_space = act_space
        self._last_act = {}

    def reset(self, *args, **keargs):
        self._last_act.clear()

    def get_next_action(self, i):
        action = []
        if i not in self._last_act:
            for k in self._act_space:
                action.append(0)
        else:
            pos = 0
            for k in self._act_space:
                act = self._last_act[i][pos] + 1
                if act >= k:
                    act = 0
                action.append(act)
                pos += 1
        self._last_act[i] = action
        action = [torch.LongTensor([v]) for v in action]
        return action

    def forward(self, data):
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