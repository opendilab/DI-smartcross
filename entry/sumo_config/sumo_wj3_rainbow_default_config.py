from easydict import EasyDict
from torch import nn

nstep = 3
sumo_rainbow_default_config = dict(
    exp_name='sumo_wj3_md_rainbow_dqn',
    env=dict(
        manager=dict(
            # Whether to use shared memory. Only effective if manager type is 'subprocess'
            shared_memory=False,
            context='spawn',
            retry_type='renew',
            max_retry=2,
        ),
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
        priority=True,
        priority_IS_weight=True,
        # Reward's future discount facotr, aka. gamma.
        discount_factor=0.99,
        # How many steps in td error.
        nstep=nstep,
        # Model config used for model creating. Remember to change "obs_shape" and "action_shape" according to env.
        model=dict(
            obs_shape=442,
            action_shape=[4, 4, 4],
            v_max=10,
            v_min=-10,
            n_atom=51,
            activation=nn.Tanh(),
        ),
        # learn_mode config
        learn=dict(
            # How many steps to train after one collection. Bigger "update_per_collect" means bigger off-policy.
            # collect data -> train fixed steps -> collect data -> ...
            update_per_collect=200,
            batch_size=64,
            learning_rate=1e-4,
            target_update_freq=100,
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
            # You can use either "n_sample" or "n_episode" in collector.collect.
            # Get "n_sample" samples per collect.
            n_sample=600,
            # Get "n_episode" complete episodic trajectories per collect.
            # n_episode=8,
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
        other=dict(
            # Epsilon greedy with decay.
            eps=dict(
                # Decay type. Support ['exp', 'linear'].
                type='exp',
                start=0.95,
                end=0.1,
                decay=50000,
            ),
            replay_buffer=dict(
                replay_buffer_size=400000,
                max_use=10000,
                monitor=dict(
                    sampled_data_attr=dict(print_freq=300, ),
                    periodic_thruput=dict(seconds=300, ),
                ),
            ),
        )
    ),
)

create_config = dict(
    env_manager=dict(type='subprocess', ),
    env=dict(
        # Must use the absolute path. All the following "import_names" should obey this too.
        import_names=['smartcross.envs.sumo_env'],
        type='sumo_env',
    ),
    # RL policy register name (refer to function "register_policy").
    policy=dict(
        import_names=['dizoo.common.policy.md_rainbow_dqn'],
        type='md_rainbow_dqn',
    ),
)

create_config = EasyDict(create_config)
sumo_rainbow_default_config = EasyDict(sumo_rainbow_default_config)
main_config = sumo_rainbow_default_config
