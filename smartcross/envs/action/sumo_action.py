from typing import Dict

from ding.envs import BaseEnv
from ding.envs.common import EnvElement

ALL_ACTION_TYPE = set(['change'])


class SumoAction(EnvElement):
    r"""
    Overview:
        the action element of Sumo enviroment

    Interface:
        _init, _from_agent_processor
    """
    _name = "SumoAction"

    def _init(self, env: BaseEnv, cfg: Dict) -> None:
        r"""
        Overview:
            init the sumo action environment with the given config file
        Arguments:
            - cfg(:obj:`EasyDict`): config, you can refer to `envs/sumo/sumo_env_default_config.yaml`
        """
        self._env = env
        self._cfg = cfg
        action_shape = []
        self._action_type = cfg.action_type
        assert self._action_type in ALL_ACTION_TYPE
        self._use_multi_discrete = cfg.use_multi_discrete
        for tl, cross in self._env.crosses.items():
            if self._action_type == 'change':
                action_shape.append(cross.phase_num)
            else:
                # TODO: add switch action
                raise NotImplementedError
        if self._use_multi_discrete:
            self._shape = len(action_shape)
        else:
            # TODO: add naive discrete action
            raise NotImplementedError
        self._value = {
            'min': 0,
            'max': action_shape[0],
            'dtype': int,
        }

    def _from_agent_processor(self, data: Dict) -> Dict:
        r"""
        """
        # TODO: add switch action
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

    # override
    def _details(self):
        return 'action dim: {}'.format(self._shape)