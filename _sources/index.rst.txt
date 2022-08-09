.. DI-smartcross documentation master file, created by
   sphinx-quickstart on Mon Jan 25 13:49:15 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

DI-smartcross Documentation
##############################

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: First steps

   installation
   quick_start
   rl_environments
   faq

.. figure:: ../figs/di-smartcross_banner.png
   :alt: DI-smartcross

Decision Intelligence Platform for Traffic Crossing Signal Control.

Last updated on 2022.08.09

-----

**DI-smartcross** is an open-source application platform under **OpenDILab**.
**DI-smartcross** uses Reinforcement Learning in precise control of traffic crossing signals in order
to optimize transportation time cost by coordinating vehicles' movements at crosses.
**DI-smartcross** applies training & evaluation for various RL policies using `DI-engine <https://github.com/opendilab/DI-engine>`_
in provided road nets.
**DI-smartcross** supports `SUMO <https://www.eclipse.org/sumo/>`_  and 
`CityFlow <https://github.com/cityflow-project/CityFlow>`_ simulators to enable 
traffic flow simulation with different granularity. 


Main Features
=================

- Design easy-to-use crossing signal control environments, with various State, Action, and Reward options.

- Build a variety of road networks of different scales, ideal or from the real world.

- Adapting several Reinforcement Learning strategies using **DI-engine**, including discrete or continuous space, multi-agent etc.


Content
==============

`Installation <installation.html>`_
------------------------------------------

`Quick Start <quickstart.html>`_
-------------------------------------

`RL Environments <rl_environments.html>`_
-------------------------------------------------

`FAQ <faq.html>`_
--------------------
