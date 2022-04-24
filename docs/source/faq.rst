FAQ
##############

.. toctree::
    :maxdepth: 2


Q1: SUMO environment always showing `Retrying in 1 seconds`
------------------------------------------------------------------

:A1:
    SUMO environments and `traci` lib is slow to reset when running with large roadnets.
    It only check the collection after reset for 1 sec. DI-smartcross provides an easy way
    to change the retry timeout for `traci`. You can run `modify_traci_connect_timeout.sh`
    file. It will automatically
