import os
import numpy as np
import pytest
import torch
import yaml
from easydict import EasyDict

from smartcross.envs import CityflowEnv


@pytest.fixture(scope='function')
def setup_config():
    cfg = dict(
        obs_type=['phase', 'lane_vehicle_num', 'lane_waiting_vehicle_num'],
        n_evaluator_episode=1,
        max_episode_duration=1000,
        green_duration=30,
        yellow_duration=5,
        red_duration=0,
        stop_value=0,
        config_path="smartcross/envs/cityflow_grid/cityflow_grid_config.json",
    )
    cfg = EasyDict(cfg)
    return cfg


@pytest.mark.envtest
class TestCityFlowEnv:

    def get_random_action(self, action_space):
        return action_space.sample()

    def test_naive(self, setup_config):
        env = CityflowEnv(setup_config)
        obs = env.reset()
        assert len(obs) == env.observation_space.shape[0]
        for i in range(10):
            action = self.get_random_action(env.action_space)
            timestep = env.step(action)
            print(timestep.reward)
            print('step {} with action {}'.format(i, action))
        print('end')
        env.close()
