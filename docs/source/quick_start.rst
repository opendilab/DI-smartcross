Quick Start
###############

.. toctree::
    :maxdepth: 2

SUMO entries
================

**DI-smartcross** supports DQN, Off-policy PPO and Rainbow DQN RL methods
with multi-discrete actions for each crossing. A set of default **DI-engine**
configs is provided for each policy. You can check the document of DI-engine
to get detail instructions of these configs.

train RL policies
--------------------

The type of policy can be automatically parsed from the config file.

.. code::

    usage: sumo_train [-h] -d DING_CFG -e ENV_CFG [-s SEED] [--dynamic-flow]
                      [-cn COLLECT_ENV_NUM] [-en EVALUATE_ENV_NUM]
                      [--exp-name EXP_NAME]

    DI-smartcross training script

    optional arguments:
    -h, --help            show this help message and exit
    -d DING_CFG, --ding-cfg DING_CFG
                            DI-engine configuration path
    -e ENV_CFG, --env-cfg ENV_CFG
                            sumo environment configuration path
    -s SEED, --seed SEED  random seed for sumo
    --dynamic-flow        use dynamic route flow
    -cn COLLECT_ENV_NUM, --collect-env-num COLLECT_ENV_NUM
                            collector sumo env num for training
    -en EVALUATE_ENV_NUM, --evaluate-env-num EVALUATE_ENV_NUM
                            evaluator sumo env num for training
    --exp-name EXP_NAME   experiment name to save log and ckpt


Example of running DQN in wj3 env with default config.

.. note:: 

    Running with dynamic flow is only supported for arterial7 env currently.

.. code:: bash

    sumo_train -e smartcross/envs/sumo_wj3_default_config.yaml -d entry/config/sumo_wj3_dqn_default_config.py

evaluate existing policies
--------------------------------

We provide two eval policies: random and fixed-time. You can choose one to evaluate
as comparison. It is suggested to use the `eval_default_config` for each env.

.. code:: 

    usage: sumo_eval [-h] [-d DING_CFG] -e ENV_CFG [-s SEED]
                     [-p {random,fix,dqn,rainbow,ppo}] [--dynamic-flow]
                     [-n ENV_NUM] [--gui] [-c CKPT_PATH]

    DI-smartcross testing script

    optional arguments:
    -h, --help            show this help message and exit
    -d DING_CFG, --ding-cfg DING_CFG
                            DI-engine configuration path
    -e ENV_CFG, --env-cfg ENV_CFG
                            sumo environment configuration path
    -s SEED, --seed SEED  random seed for sumo
    -p {random,fix,dqn,rainbow,ppo}, --policy-type {random,fix,dqn,rainbow,ppo}
                            RL policy type
    --dynamic-flow        use dynamic route flow
    -n ENV_NUM, --env-num ENV_NUM
                            sumo env num for evaluation
    --gui                 open gui for visualize
    -c CKPT_PATH, --ckpt-path CKPT_PATH
                            model ckpt path


Example of running random policy in wj3 env.

.. code:: bash

    sumo_eval -p random -e smartcross/envs/sumo_wj3_default_config.yaml


CityFlow Entries
=================

**DI-smartcross** provides a simple DQN and Off-policy PPO demo for CityFlow env. Each
policy comes with a default **DI-engine** configs is provided for each policy. You can
check the document of DI-engine to get detail instructions of these configs.

train RL policies
--------------------

.. code::

    usage: cityflow_train [-h] -d DING_CFG -e ENV_CFG [-s SEED]
                          [-cn COLLECT_ENV_NUM] [-en EVALUATE_ENV_NUM]
                          [--exp-name EXP_NAME]

    DI-smartcross training script

    optional arguments:
    -h, --help            show this help message and exit
    -d DING_CFG, --ding-cfg DING_CFG
                            DI-engine configuration path
    -e ENV_CFG, --env-cfg ENV_CFG
                            cityflow json configuration path
    -s SEED, --seed SEED  random seed
    -cn COLLECT_ENV_NUM, --collect-env-num COLLECT_ENV_NUM
                            collector env num for training
    -en EVALUATE_ENV_NUM, --evaluate-env-num EVALUATE_ENV_NUM
                            evaluator env num for training
    --exp-name EXP_NAME   experiment name to save log and ckpt

evaluate existing policies
--------------------------------

Note that CityFlow will run in fixed-time mode by default when not in rl mode.
So the fix policy runs with an `auto_config.json`.

.. code::

    usage: cityflow_eval [-h] [-d DING_CFG] -e ENV_CFG [-s SEED]
                         [-p {fix,dqn,ppo}] [-n ENV_NUM] [-c CKPT_PATH]

    DI-smartcross training script

    optional arguments:
    -h, --help            show this help message and exit
    -d DING_CFG, --ding-cfg DING_CFG
                            DI-engine configuration path
    -e ENV_CFG, --env-cfg ENV_CFG
                            sumo environment configuration path
    -s SEED, --seed SEED  random seed for sumo
    -p {fix,dqn,ppo}, --policy-type {fix,dqn,ppo}
                            RL policy type
    -n ENV_NUM, --env-num ENV_NUM
                            sumo env num for evaluation
    -c CKPT_PATH, --ckpt-path CKPT_PATH
                            model ckpt path
