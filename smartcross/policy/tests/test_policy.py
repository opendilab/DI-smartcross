import os
import pytest
import yaml
from easydict import EasyDict

from smartcross.envs import SumoEnv
from smartcross.policy import RandomPolicy, FixedPolicy


@pytest.fixture(scope='function')
def setup_env():
    with open(os.path.join(os.path.dirname(__file__), '../../envs/sumo_wj3_default_config.yaml')) as f:
        cfg = yaml.safe_load(f)
    cfg = EasyDict(cfg)
    env = SumoEnv(cfg.env)
    return env


@pytest.mark.policytest
class TestPolicy:

    def test_random_policy(self, setup_env):
        env = setup_env
        obs = env.reset()
        policy = RandomPolicy(env.action_space)
        for i in range(10):
            action = policy.forward({0: obs})
            assert 0 in action
            assert len(action[0]['action']) == len(env.action_space.nvec)
            timestep = env.step(action[0]['action'])
            obs = timestep.obs
            print(action)
        print('end')
        env.close()

    def test_fix_policy(self, setup_env):
        env = setup_env
        obs = env.reset()
        policy = FixedPolicy(env.action_space)
        for i in range(10):
            action = policy.forward({0: obs})
            assert 0 in action
            assert len(action[0]['action']) == len(env.action_space.nvec)
            assert action[0]['action'][0].item() == i % env.action_space.nvec[0]
            timestep = env.step(action[0]['action'])
            obs = timestep.obs
            print(action)
        print('end')
        env.close()
