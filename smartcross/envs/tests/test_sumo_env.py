import os
import numpy as np
import pytest
import torch
import yaml
from easydict import EasyDict

from smartcross.envs import SumoEnv


@pytest.fixture(scope='function')
def setup_config():
    with open(os.path.join(os.path.dirname(__file__), '../sumo_arterial_wj3_default_config.yaml')) as f:
        cfg = yaml.safe_load(f)
    cfg = EasyDict(cfg)
    return cfg.env


@pytest.mark.envtest
class TestSumoEnv:

    def get_random_action(self, action_space):
        min, max, shape = action_space.value['min'], action_space.value['max'], action_space.shape
        action = np.random.randint(min, max, shape)
        action = [torch.LongTensor([v]) for v in action]
        return action

    def test_naive(self, setup_config):
        env = SumoEnv(setup_config)
        obs = env.reset()
        assert (len(obs) == env.info().obs_space.shape)
        for i in range(10):
            action = self.get_random_action(env.info().act_space)
            timestep = env.step(action)
            print(timestep.reward)
            print('step {} with action {}'.format(i, action))
        print('end')
        env.close()
