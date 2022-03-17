from easydict import EasyDict
from torch import nn

nstep = 1
sumo_off_mdppo_default_config = dict(
    exp_name='sumo_arterial7_off_md_ppo',
    env=dict(
        manager=dict(
            shared_memory=False,
            context='spawn',
            retry_type='renew',
            max_retry=5,
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
        # (bool) Whether to use priority(priority sample, IS weight, update priority)
        priority=False,
        # ()
        continuous=False,
        model=dict(
            obs_shape=224,
            action_shape=[4] * 7,
            activation=nn.Tanh(),
        ),
        # learn_mode config
        learn=dict(
            update_per_collect=100,
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
            ignore_done=True,
        ),
        # collect_mode config
        collect=dict(
            unroll_len=1,
            discount_factor=0.99,
            gae_lambda=0.95,
            n_sample=600,
            collector=dict(
                transform_obs=True,
                collect_print_freq=1000,
            )
        ),
        eval=dict(
            evaluator=dict(
                # Evaluate every "eval_freq" training steps.
                eval_freq=1000,
            )
        ),
        # command_mode config
        other=dict(
            replay_buffer=dict(
                replay_buffer_size=400000,
                max_use=10000,
                monitor=dict(
                    sampled_data_attr=dict(print_freq=300, ),
                    periodic_thruput=dict(seconds=300, ),
                ),
            ),
        ),
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
        import_names=['dizoo.common.policy.md_ppo'],
        type='md_ppo_offpolicy',
    ),
)

create_config = EasyDict(create_config)
sumo_off_mdppo_default_config = EasyDict(sumo_off_mdppo_default_config)
main_config = sumo_off_mdppo_default_config
