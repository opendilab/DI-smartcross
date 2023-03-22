from easydict import EasyDict

cityflow_mdppo_default_config = dict(
    exp_name='cityflow_grid22_discrete_ppo',
    env=dict(
        config_path='path_to_di-smartcross/smartcross/envs/cityflow_grid/cityflow_grid_22_config.json',
        manager=dict(
            shared_memory=False,
            context='spawn',
            retry_type='renew',
            max_retry=5,
        ),
        from_discrete=True,
        obs_type=['phase', 'lane_vehicle_num', 'lane_waiting_vehicle_num'],
        max_episode_duration=1000,
        green_duration=30,
        yellow_duration=5,
        red_duration=0,
        # Episode number for evaluation.
        n_evaluator_episode=1,
        # Once evaluation reward reaches "stop_value", which means the policy converges, the training can end.
        stop_value=0,
        collector_env_num=15,
        evaluator_env_num=1,
    ),
    policy=dict(
        # Whether to use cuda for network.
        cuda=True,
        # Whether use priority
        priority=False,
        continuous=False,
        # Model config used for model creating. Remember to change "obs_shape" and "action_shape" according to env.
        model=dict(
            obs_shape=176,
            action_shape=[4 ** 4],
        ),
        # learn_mode config
        learn=dict(
            # How many steps to train after one collection. Bigger "update_per_collect" means bigger off-policy.
            # collect data -> train fixed steps -> collect data -> ...
            train_epoch=60000,
            epoch_per_collect=4,
            batch_size=64,
            learning_rate=1e-4,
            value_weight=0.5,
            entropy_weight=0.01,
            clip_ratio=0.2,
            learner=dict(
                hook=dict(
                    save_ckpt_after_iter=1000,
                    log_show_after_iter=1000,
                ),
            ),
        ),
        # collect_mode config
        collect=dict(
            # Cut trajectories into pieces with length "unrol_len".
            unroll_len=1,
            discount_factor=0.99,
            gae_lambda=0.95,
            # You can use either "n_sample" or "n_episode" in collector.collect.
            # Get "n_sample" samples per collect.
            n_sample=600,
            collector=dict(
                # Get "n_episode" complete episodic trajectories per collect.
                # n_episode=8,
                transform_obs=True,
                collect_print_freq=1000,
            ),
        ),
        eval=dict(
            evaluator=dict(
                # Evaluate every "eval_freq" training steps.
                eval_freq=1000,
            )
        ),
        # command_mode config
        other=dict(replay_buffer=dict(replay_buffer_size=2000, ), ),
    ),
)

create_config = dict(
    env_manager=dict(
        type='subprocess',
    ),
    env=dict(
        import_names=['smartcross.envs.cityflow_env'],
        type='cityflow_env',
    ),
    policy=dict(
        import_names=['ding.policy.ppo'],
        type='ppo',
    ),
)

create_config = EasyDict(create_config)
cityflow_mdppo_default_config = EasyDict(cityflow_mdppo_default_config)
main_config = cityflow_mdppo_default_config

# You can run the following command to execute this config file.
# cityflow_train -e ./smartcross/envs/cityflow_grid/cityflow_grid_22_config.json -d entry/cityflow_config/cityflow_ppo_22_discrete_config.py -cn 8
