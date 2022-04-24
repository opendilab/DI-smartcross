from easydict import EasyDict

sumo_eval_default_config = dict(
    env=dict(
        manager=dict(
            # Whether to use shared memory. Only effective if manager type is 'subprocess'
            shared_memory=False,
            context='spawn',
            retry_type='renew',
        ),
        n_evaluator_episode=1,
        collector_env_num=1,
        evaluator_env_num=1,
        stop_value=99999,
    ),
    policy=dict(cuda=False, )
)

create_config = dict(
    env_manager=dict(type='subprocess', ),
    env=dict(
        # Must use the absolute path. All the following "import_names" should obey this too.
        import_names=['smartcross.envs.sumo_env'],
        type='sumo_env',
    ),
    policy=dict(),
)

create_config = EasyDict(create_config)
sumo_eval_default_config = EasyDict(sumo_eval_default_config)
main_config = sumo_eval_default_config
