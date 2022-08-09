CityFlow Grid Env
#####################

This is a synthetic roadmap with a shape of 2x3 grid in CityFlow. Unlike the standard grid
roadmap provided by CityFlow and mainly used in academic works, we made the roadmap with
different number of lanes in the rows and columns. Also, we add more complicated vehicle
routes for the original traffic flow is not enough to simulate real driving situations in 
a grid roadmap. In general, this is a more challenging and realistic roadmap for RL traffic
signal control policies. The shape of the road network is as follows.

.. figure:: ../../figs/grid2x3.gif
    :alt: grid2x3


Configuration
=================

The roadmap files and CityFlow configs are stored in ``smartcross/envs/cityflow_grid``. We
provide RL env configs in this path as well, ``smartcross/envs/cityflow_grid/cityflow_grid_config.json``.
Note that the ``auto`` config is for the default control method (fixed-time) to be compared with.

The roadmap files and CityFlow configs are stored in ``smartcross/envs/cityflow_grid``. We
provide RL env configs in this path as well, ``smartcross/envs/cityflow_grid/cityflow_grid_config.json``.
Note that the ``auto`` config is for the default control method (fixed-time) to be compared with.


.. note:: 

    The might be ``replay_auto.txt`` and ``replay_auto_roadnet.json`` files  arose in this path.
    They are used for replay in a web page, and they will not be auto-cleared in a new episode,
    so that they will grow larger and larger. It is recommended to manually delete these files
    regularly to save storage.