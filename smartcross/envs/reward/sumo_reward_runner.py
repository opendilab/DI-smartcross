import numpy as np
from typing import Dict, Any

from ding.envs.common import EnvElementRunner
from ding.envs.env.base_env import BaseEnv
from ding.torch_utils import to_ndarray
from .sumo_reward import SumoReward


class SumoRewardRunner(EnvElementRunner):
    r"""
    Overview:
        the reward element of Sumo enviroment

    Interface:
        _init, to_agent_processor
    """

    def _init(self, engine: BaseEnv, cfg: dict) -> None:
        r"""
        Overview:
            init the sumo reward environment with the given config file
        Arguments:
            - cfg(:obj:`EasyDict`): config, you can refer to `envs/sumo/sumo_env_default_config.yaml`
        """
        self._engine = engine
        self._core = SumoReward(engine, cfg)
        self._final_eval_reward = 0

    def get(self) -> Any:
        reward = self._core._to_agent_processor()
        self._final_eval_reward += reward
        return reward

    def reset(self) -> None:
        self._final_eval_reward = 0
