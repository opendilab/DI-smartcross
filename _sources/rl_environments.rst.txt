Reinforcement Learning Environments
########################################


SUMO environments
====================

configuration
-----------------

The configuration of sumo env is stored in a config ``.yaml`` file. You can take a look at the default config file to see how to modify env settings.

.. code:: python

    import yaml
    from easy_dict import EasyDict
    from smartcross.env import SumoEnv

    with open('smartcross/envs/sumo_wj3_default_config.yaml') as f:
        cfg = yaml.safe_load(f)
    cfg = EasyDict(cfg)
    env = SumoEnv(config=cfg.env)

The env configuration consists of basic definition and observation\\action\\reward settings. The basic definition includes the cumo config file, episode length and light duration. The obs\action\reward define the detail setting of each contains.

.. code:: yaml

    env:
        sumocfg_path: 'wj3/rl_wj.sumocfg'
        max_episode_steps: 1500
        green_duration: 10
        yellow_duration: 3
        obs:
            ...
        action:
            ...
        reward:
            ...

Observation
----------------

We provide several types of observations of a traffic cross. If `use_centrolized_obs` is set `True`, the observation of each cross will be concatenated into one vector. The contents of observation can me modified by setting `obs_type`. The following observation is supported now.

- phase: One-hot phase vector of current cross signal
- lane_pos_vec: Lane occupancy in each grid position. The grid num can be set with `lane_grid_num`
- traffic_volumn: Traffic volumn of each lane. Vehicle num / lane length * volumn ratio
- queue_len: Vehicle waiting queue length of each lane. Waiting num / lane length * volumn ratio

Action
-------------

Sumo environment supports changing cross signal to target phase. The action space is set to multi-discrete for each cross to reduce action num.

Reward
-------------

Reward can be set with `reward_type`. Reward is calculated cross by cross. If `use_centrolized_obs` is set True, the reward of each cross will be summed up.

- queue_len: Vehicle waiting queue num of each lane
- wait_time: Wait time increment of vehicles in each lane
- delay_time: Delay time of all vahicles in incomming and outgoing lanes
- pressure: Pressure of a cross

Multi-agent
---------------

**DI-smartcross** supports a one-step configurable multi-agent RL training.
It is only necessary to add ``multi_agent`` in **DI-engine** config file to convert common PPO into MAPPO,
and change the ``use_centrolized_obs`` in environment config into ``True``. The policy and observations can
be automatically changed to run individual agent for each cross.

Roadnets
-------------

.. `Beijing Wangjing 3 Crossings <./envs/wj3_env.html>`_

.. `RL Arterial 7 Crossings <./envs/rl_arterial7_env.html>`_

.. toctree::
    :maxdepth: 2

    envs/wj3_env
    envs/rl_arterial7_env
