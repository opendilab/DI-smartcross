import numpy as np

from ding.envs.common import EnvElementRunner
from ding.envs.env.base_env import BaseEnv
from ding.torch_utils import to_ndarray
from .sumo_obs import SumoObs


class SumoObsRunner(EnvElementRunner):
    r"""
    Overview:
        runner that help to get the observation space
    Interface:
        _init, get, reset
    """

    def _init(self, engine: BaseEnv, cfg: dict) -> None:
        r"""
        Overview:
            init the sumo observation helper with the given config file
        Arguments:
            - cfg(:obj:`EasyDict`): config, you can refer to `envs/sumo/sumo_env_default_config.yaml`
        """
        # set self._core and other state variable
        self._engine = engine
        self._core = SumoObs(engine, cfg)
        self._obs = None

    def get(self):
        """
        Overview:
            return the formated observation
        Returns:
            - obs (:obj:`torch.Tensor` or :obj:`dict`): the returned observation,\
            :obj:`torch.Tensor` if used centerlized_obs, else :obj:`dict` with format {traffic_light: reward}
        """
        self._obs = self._core._to_agent_processor()
        return to_ndarray(self._obs, dtype=np.float32)

    # override
    def reset(self) -> None:
        r"""
        Overview:
            reset obs runner, and return the initial obs
        """
        return to_ndarray(self._obs, dtype=np.float32)
