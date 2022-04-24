import smartcross

if 'sumo' in smartcross.SIMULATORS:
    from .sumo_env import SumoEnv
if 'cityflow' in smartcross.SIMULATORS:
    from .cityflow_env import CityflowEnv
