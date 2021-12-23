# DI-smartcross

<img src="./figs/di-smartcross_logo.png" width="200" alt="icon"/>

DI-smartcross - Decision Intelligence Platform for Traffic Crossing Signal Control.

DI-smartcross is application platform under [OpenDILab](http://opendilab.org/)

## Instruction

**DI-smartcross** is an open-source traffic crossing signal control platform. DI-smartcross applies several Reinforcement Learning policies training & evaluation for traffic signal control system in provided road nets.

DI-smartcross uses [**DI-engine**](https://github.com/opendilab/DI-engine), a Reinforcement Learning platform to build RL experiments. DI-smartcross uses [SUMO](https://www.eclipse.org/sumo/) (Simulation of Urban MObility) traffic simulator package to run signal control simulation.

## Installation

DI-smartcross supports SUMO version >= 1.6.0. Here we show an easy guide of installation with SUMO 1.8.0 on Linux.

### Install sumo

1. install required libraries and dependencies

```bash
sudo apt-get install cmake python g++ libxerces-c-dev libfox-1.6-dev libgdal-dev libproj-dev libgl2ps-dev swig
```

2. download and unzip the installation package

```bash
tar xzf sumo-src-1.8.0.tar.gz
cd sumo-1.8.0
pwd 
```

3. compile sumo

```bash
mkdir build/cmake-build
cd build/cmake-build
cmake ../..
make -j $(nproc)
```

4. environment variables

```bash
echo 'export PATH=$HOME/sumo-1.8.0/bin:$PATH
export SUMO_HOME=$HOME/sumo-1.8.0' | tee -a $HOME/.bashrc
source ~/.bashrc
```

5. check install

```bash
sumo
```

### Install DI-smartcross

To install DI-smartcross, simply run `pip install` in the root folder of this repository. This will automatically insall [DI-engine](https://github.com/opendilab/DI-engine) as well.

```bash
pip install -e . --user
```

## Quick Start

### Run training and evaluation

DI-smartcross supports DQN, Off-policy PPO and Rainbow DQN RL methods with multi-discrete actions for each crossing. A set of default DI-engine configs is provided for each policy. You can check the document of DI-engine to get detail instructions of these configs.

- train RL policies

```bash
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
```

- evaluate existing policies

```bash
usage: sumo_eval [-h] [-d DING_CFG] -e ENV_CFG [-s SEED]
                 [-p {random,fix,dqn,rainbow,ppo}] [--dynamic-flow]
                 [-n ENV_NUM] [--gui] [-c CKPT_PATH]

DI-smartcross training script

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
```

## Environments

### sumo env configuration

The configuration of sumo env is stored in a config *.yaml* file. You can take a look at the default config file to see how to modify env settings.

``` python
import yaml
from easy_dict import EasyDict
from smartcross.env import SumoEnv

with open('smartcross/envs/sumo_arterial_wj3_default_config.yaml') as f:
    cfg = yaml.safe_load(f)
cfg = EasyDict(cfg)
env = SumoEnv(config=cfg.env)
```

The env configuration consists of basic definition and observation\action\reward settings. The basic definition includes the cumo config file, episode length and light duration. The obs\action\reward define the detail setting of each contains.

```yaml
env:
    sumocfg_path: 'arterial_wj3/rl_wj.sumocfg'
    max_episode_steps: 1500
    green_duration: 10
    yellow_duration: 3
    obs:
        ...
    action:
        ...
    reward:
        ...
```

### Observation

We provide several types of observations of a traffic cross. If `use_centrolized_obs` is set `True`, the observation of each cross will be concatenated into one vector. The contents of observation can me modified by setting `obs_type`. The following observation is supported now.

- phase: One-hot phase vector of current cross signal
- lane_pos_vec: Lane occupancy in each grid position. The grid num can be set with `lane_grid_num`
- traffic_volumn: Traffic volumn of each lane. Vehicle num / lane length * volumn ratio
- queue_len: Vehicle waiting queue length of each lane. Waiting num / lane length * volumn ratio

### Action

Sumo environment supports changing cross signal to target phase. The action space is set to multi-discrete for each cross to reduce action num.

### Reward

Reward can be set with `reward_type`. Reward is calculated cross by cross. If `use_centrolized_obs` is set True, the reward of each cross will be summed up.

- queue_len: Vehicle waiting queue num of each lane
- wait_time: Wait time increment of vehicles in each lane
- delay_time: Delay time of all vahicles in incomming and outgoing lanes
- pressure: Pressure of a cross

## Contributing

We appreciate all contributions to improve DI-smartcross, both algorithms and system designs.

## License

DI-smartcross released under the Apache 2.0 license.

## Citation

@misc{smartcross,
    title={{DI-smartcross: OpenDILab} Decision Intelligence platform for Traffic Crossing Signal Control},
    author={DI-smartcross Contributors},
    publisher = {GitHub},
    howpublished = {\url{`https://github.com/opendilab/DI-smartcross`}},
    year={2021},
}

