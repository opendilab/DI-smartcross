from typing import Dict, Any
import numpy as np
import torch

from ding.envs.common import EnvElementRunner
from ding.envs.env.base_env import BaseEnv
from ding.torch_utils import to_ndarray
from .sumo_action import SumoAction


class SumoActionRunner(EnvElementRunner):

    def _init(self, engine: BaseEnv, cfg: Dict) -> None:
        r"""
        Overview:
            init the sumo observation helper with the given config file
        Arguments:
            - cfg(:obj:`EasyDict`): config, you can refer to `envs/sumo_wj3_default_config.yaml`
        """
        # set self._core and other state variable
        self._engine = engine
        self._core = SumoAction(engine, cfg)
        self._last_action = None

    def get(self, raw_action: Any) -> Dict:
        raw_action = np.squeeze(raw_action)
        if self._last_action is None:
            self._last_action = [None for _ in range(len(raw_action))]
        data = {}
        for tl, act, last_act in zip(self._engine.crosses.keys(), raw_action, self._last_action):
            data[tl] = {'action': act, 'last_action': last_act}
        action = self._core._from_agent_processor(data)
        return action

    def reset(self) -> None:
        self._last_action = None

    @property
    def space(self):
        return self._core.space
