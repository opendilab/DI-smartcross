from easydict import EasyDict
from torch import nn

sumo_mdppo_default_config = dict(
    exp_name='sumo_wj3_md_ppo',
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
        # (bool) Whether to use cuda for network.
        cuda=True,
        # (bool) Whether to use priority(priority sample, IS weight, update priority)
        priority=False,
        # ()
        continuous=False,
        model=dict(
            obs_shape=442,
            action_shape=[4, 4, 4],
            activation=nn.Tanh(),
        ),
        learn=dict(
            epoch_per_collect=10,
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
        eval=dict(evaluator=dict(eval_freq=1000, )),
        other=dict()
    ),
)

create_config = dict(
    env_manager=dict(
        type='subprocess',
    ),
    env=dict(
        import_names=['smartcross.envs.sumo_env'],
        type='sumo_env',
    ),
    policy=dict(
        import_names=['dizoo.common.policy.md_ppo'],
        type='md_ppo',
    ),
)

create_config = EasyDict(create_config)
sumo_mdppo_default_config = EasyDict(sumo_mdppo_default_config)
main_config = sumo_mdppo_default_config
