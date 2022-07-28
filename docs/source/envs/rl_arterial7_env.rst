SUMO RL Arterial 7 Crossings Env
#################################

This is a synthetic arterial roadmap with 7 crossings in SUMO. The main purpose of this env
is to deploy RL signal control policy in real **dynamic traffic flows**. Each crossing has 4
directions and 3-5 lanes at each direction, and the lane is flared (widen near crossing) to
enable greater traffic flow. The env has different traffic flow density, together with 200
randomly generated traffic flows for each density value. The shape of the road network is as
follows.


.. figure:: ../../figs/rl_arterial.png
    :alt: arterial


Configuration
================

The roadmap files and SUMO configs are stored in ``smartcross/envs/sumo_arterial_7roads``.
By defalut, the env uses a fixed density of 1100 and a single flow file. Additional traffic
flow files are needed if users want to enable `dynamic flow`. Simply put it into 
``smartcross/envs/sumo_arterial_7roads/route``, and set ``dynamic_flow`` to ``true`` to enable
a randomly dynamic flow range of [900, 2000] for each episode.

a standard RL env config in ``smartcross/envs/sumo_arterial7_default_config.yaml``. Users can
modify RL env according to the instructions of SUMO env configs.
