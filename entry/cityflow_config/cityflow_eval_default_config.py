from easydict import EasyDict

cityflow_eval_default_config = dict(
    env=dict(
        manager=dict(
            # Whether to use shared memory. Only effective if manager type is 'subprocess'
            shared_memory=False,
            context='spawn',
            retry_type='renew',
        ),
        obs_type=['phase'],
        n_evaluator_episode=1,
        max_episode_duration=1000,
        green_duration=30,
        yellow_duration=5,
        red_duration=0,
        stop_value=0,
        collector_env_num=1,
        evaluator_env_num=1,
    ),
    policy=dict(cuda=False, )
)

create_config = dict(
    env_manager=dict(type='subprocess', ),
    env=dict(
        # Must use the absolute path. All the following "import_names" should obey this too.
        import_names=['smartcross.envs.cityflow_env'],
        type='cityflow_env',
    ),
    policy=dict(),
)

create_config = EasyDict(create_config)
cityflow_eval_default_config = EasyDict(cityflow_eval_default_config)
main_config = cityflow_eval_default_config
