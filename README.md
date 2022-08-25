# DI-smartcross

<img src="./docs/figs/di-smartcross_banner.png" alt="icon"/>

[![Twitter](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Ftwitter.com%2Fopendilab)](https://twitter.com/opendilab)
[![Style](https://github.com/opendilab/DI-smartcross/actions/workflows/style.yml/badge.svg)](https://github.com/opendilab/DI-smartcross/actions/workflows/style.yml?query=workflow%3A%22Style%22)
[![Docs](https://github.com/opendilab/DI-smartcross/actions/workflows/doc.yml/badge.svg)](https://github.com/opendilab/DI-smartcross/actions/workflows/doc.yml?query=workflow%3A%22Docs+Deploy%22)
[![Code test](https://github.com/opendilab/DI-smartcross/actions/workflows/test.yml/badge.svg)](https://github.com/opendilab/DI-smartcross/actions/workflows/test.yml?query=workflow%3A%22Code+Test%22)
[![codecov](https://img.shields.io/codecov/c/github/opendilab/di-smartcross)](https://img.shields.io/codecov/c/github/opendilab/di-smartcross)

![GitHub Org's stars](https://img.shields.io/github/stars/opendilab)
[![GitHub stars](https://img.shields.io/github/stars/opendilab/DI-smartcross)](https://github.com/opendilab/DI-smartcross/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/opendilab/DI-smartcross)](https://github.com/opendilab/DI-smartcross/network)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/opendilab/DI-smartcross)
[![GitHub license](https://img.shields.io/github/license/opendilab/DI-smartcross)](https://github.com/opendilab/DI-smartcross/blob/master/LICENSE)

## Introduction

[DI-smartcross doc](https://opendilab.github.io/DI-smartcross/index.html)

**DI-smartcross** is an open-source Decision Intelligence platform for Traffic Crossing Signal Control task. DI-smartcross applies several Reinforcement Learning policies training & evaluation for the traffic signal control system in provided road nets. DI-smartcross is application platform under [OpenDILab](http://opendilab.org/).

DI-smartcross uses [**DI-engine**](https://github.com/opendilab/DI-engine), a Reinforcement Learning platform, to build RL experiments. DI-smartcross uses [SUMO](https://www.eclipse.org/sumo/) (Simulation of Urban MObility) and [CityFlow](https://cityflow-project.github.io) traffic simulator packages to run signal control simulation.

DI-smartcross supports:

- **Single-Agent** and **Multi-Agent** Reinforcement Learning
- **Synthetic** and **Real** roadnet, **Arterial** and **Grid** network shape
- **Customizable** observation, action and reward types
- Easily achieve **Multi-Environment Parallel**, **Actor-Learner Asynchronous Parallel** when training with DI-engine

## Outline

  - [Introduction](#introduction)
  - [Outline](#outline)
  - [Installation](#installation)
  - [Quick Start](#quick-start)
  - [File Structure](#file-structure)
  - [Contributing](#contributing)
  - [License](#license)
  - [Citation](#citation)

## Installation

DI-smartcross supports SUMO version >= 1.6.0. You can refer to 
[SUMO documentation](https://sumo.dlr.de/docs/Installing/index.html) or follow our installation guidance in 
[documents](https://opendilab.github.io/DI-smartcross/installation.html).
CityFlow can be installed and compiled from source code. You can clone their repo and run `pip install .`

Then, DI-smartcross is able to be installed from the source code.
Simply run `pip install .` in the root folder of this repository.
This will automatically install [DI-engine](https://github.com/opendilab/DI-engine) as well.

```bash
pip install -e . --user
```

## Quick Start

DI-smartcross provides simple entry for RL training and evaluation. DI-smartcross supports DQN, Off-policy PPO
and Rainbow DQN RL methods with multi-discrete actions for each crossing, as well as multi-agent RL policies
in which each crossing is handled by a individual agent. A set of default DI-engine configs is provided for 
each policy. You can check the document of DI-engine to get detailed instructions on these configs.

Here we show RL training sript for sumo envs, same with cityflow env.

- train RL policies

Example of running DQN in sumo wj3 env with default config.

```bash
sumo_train -e smartcross/envs/sumo_wj3_default_config.yaml -d entry/config/sumo_wj3_dqn_default_config.py
```

Example of running PPO in cityflow grid env with default config.

```bash
cityflow_train -e ./smartcross/envs/cityflow_grid/cityflow_grid_config.json -d entry/cityflow_config/cityflow_grid_ppo_default_config.py 
```

- evaluate existing policies

Example of running random policy in wj3 env.


```bash
sumo_eval -p random -e smartcross/envs/sumo_wj3_default_config.yaml     
```

Example of running fix policy in cityflow grid env.

```bash
cityflow_eval -e smartcross/envs/cityflow_grid/cityflow_auto_grid_config.json -d entry/cityflow_config/cityflow_eval_default_config.py -p fix
```

It is rerecommended to refer to [documation](https://opendilab.github.io/DI-smartcross/index.html)
for detailed information.

## File Structure

```
DI-smartcross
|-- .flake8
|-- .gitignore
|-- .style.yapf
|-- LICENSE
|-- README.md
|-- format.sh
|-- modify_traci_connect_timeout.sh
|-- setup.py
|-- docs
|   |-- .gitignore
|   |-- Makefile
|   |-- figs
|   |-- source
|-- entry
|   |-- cityflow_eval
|   |-- cityflow_train
|   |-- sumo_eval
|   |-- sumo_train
|   |-- cityflow_config
|   |-- sumo_config
|-- smartcross
    |-- __init__.py
    |-- envs
    |   |-- __init__.py
    |   |-- cityflow_env.py
    |   |-- crossing.py
    |   |-- sumo_arterial7_default_config.yaml
    |   |-- sumo_arterial7_multi_agent_config.yaml
    |   |-- sumo_env.py
    |   |-- sumo_wj3_default_config.yaml
    |   |-- sumo_wj3_multi_agent_config.yaml
    |   |-- action
    |   |-- cityflow_grid
    |   |-- obs
    |   |-- reward
    |   |-- sumo_arterial_7roads
    |   |-- sumo_wj3
    |   |-- tests
    |       |-- test_cityflow_env.py
    |       |-- test_sumo_env.py
    |-- policy
    |   |-- __init__.py
    |   |-- default_policy.py
    |   |-- tests
    |       |-- test_policy.py
    |-- utils
        |-- config_utils.py
        |-- env_utils.py
```

## Join and Contribute

We appreciate all contributions to improve DI-smartcross, both algorithms and system designs. Welcome to OpenDILab community! Scan the QR code and add us on Wechat:

<div align=center><img width="250" height="250" src="./docs/figs/qr.png" alt="qr"/></div>

Or you can contact us with [slack](https://opendilab.slack.com/join/shared_invite/zt-v9tmv4fp-nUBAQEH1_Kuyu_q4plBssQ#/shared-invite/email) or email (opendilab.contact@gmail.com).

## License

DI-smartcross released under the Apache 2.0 license.

## Citation

```latex
@misc{smartcross,
    title={{DI-smartcross: OpenDILab} Decision Intelligence platform for Traffic Crossing Signal Control},
    author={DI-smartcross Contributors},
    publisher = {GitHub},
    howpublished = {\url{`https://github.com/opendilab/DI-smartcross`}},
    year={2021},
}
```
