# DI-smartcross

<img src="./figs/di-smartcross_logo.png" width="200" alt="icon"/>

DI-smartcross - Decision Intelligence Platform for Traffic Crossing Signal Control.

DI-smartcross is application platform under [OpenDILab](http://opendilab.org/)

## Instruction

**DI-smartcross** is an open-source traffic crossing signal control platform. DI-smartcross applies several Reinforcement Learning policies training & evaluation for traffic signal control system in provided road nets.

DI-smartcross uses [**DI-engine**](https://github.com/opendilab/DI-engine), a Reinforcement Learning platform to build RL experiments. DI-smartcross uses [SUMO](https://www.eclipse.org/sumo/) (Simulation of Urban MObility) traffic simulator package to run signal control simulation.

DI-smartcross supports:

- **Single-Agent** and **Multi-Agent** Reinforcement Learning
- **Synthetic** and **Real** roadnet, **Arterial** and **Grid** network shape
- **Customizable** observation, action and reward types
- Easily achieve **Multi-Environment Parallel**, **Actor-Learner Asynchronous Parallel** when training with DI-engine

## Installation

DI-smartcross supports SUMO version >= 1.6.0. You can refer to 
[SUMO documentation](https://sumo.dlr.de/docs/Installing/index.html) or follow our installation guidance in 
[documents](https://opendilab.github.io/DI-smartcross/installation.html).

Then, DI-smartcross is able to be installed from source code.
Simply run `pip install` in the root folder of this repository.
This will automatically insall [DI-engine](https://github.com/opendilab/DI-engine) as well.

```bash
pip install -e . --user
```

## Quick Start

DI-smartcross provides simple entry for RL training and evaluation. DI-smartcross supports DQN, Off-policy PPO
and Rainbow DQN RL methods with multi-discrete actions for each crossing, as well as multi-agent RL policies
in which each crossing is handled by a individual agent. A set of default DI-engine configs is provided for 
each policy. You can check the document of DI-engine to get detail instructions of these configs.

- train RL policies

Example of running DQN in wj3 env with default config.

```bash
sumo_train -e smartcross/envs/sumo_wj3_default_config.yaml -d entry/config/sumo_wj3_dqn_default_config.py
```

- evaluate existing policies

Example of running random policy in wj3 env.

```bash
sumo_eval -p random -e smartcross/envs/sumo_wj3_default_config.yaml     
```

It is rerecommended to refer to [documation](https://opendilab.github.io/DI-smartcross/index.html)
for detail information.

## Contributing

We appreciate all contributions to improve DI-smartcross, both algorithms and system designs.

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

