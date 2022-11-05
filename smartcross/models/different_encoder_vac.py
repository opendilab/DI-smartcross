from typing import Union, Dict, Optional
from easydict import EasyDict
import torch
import torch.nn as nn
from copy import deepcopy
from ding.utils import SequenceType, squeeze, MODEL_REGISTRY
from ding.model.common import ReparameterizationHead, RegressionHead, DiscreteHead, MultiHead, \
    FCEncoder, ConvEncoder, IMPALAConvEncoder
from ding.utils import lists_to_dicts


class DEVAC(nn.Module):
    r"""
    Overview:
        The DEVAC model.
    Interfaces:
        ``__init__``, ``forward``, ``compute_actor``, ``compute_critic``
    """
    mode = ['compute_actor', 'compute_critic', 'compute_actor_critic']

    def __init__(
        self,
        obs_shape: Union[int, SequenceType],
        action_shape: Union[int, SequenceType, EasyDict],
        action_space: str = 'discrete',
        share_encoder: bool = True,
        encoder_hidden_size_list: SequenceType = [128, 128, 64],
        actor_head_hidden_size: int = 64,
        actor_head_layer_num: int = 1,
        critic_head_hidden_size: int = 64,
        critic_head_layer_num: int = 1,
        activation: Optional[nn.Module] = nn.ReLU(),
        norm_type: Optional[str] = None,
        encoder: Optional[torch.nn.Module] = None,
        impala_cnn_encoder: bool = False,
    ) -> None:
        r"""
        Overview:
            Init the VAC Model according to arguments.
        Arguments:
            - obs_shape (:obj:`Union[int, SequenceType]`): Observation's space.
            - action_shape (:obj:`Union[int, SequenceType]`): Action's space.
            - action_space (:obj:`str`): Choose action head in ['discrete', 'continuous', 'hybrid']
            - share_encoder (:obj:`bool`): Whether share encoder.
            - encoder_hidden_size_list (:obj:`SequenceType`): Collection of ``hidden_size`` to pass to ``Encoder``
            - actor_head_hidden_size (:obj:`Optional[int]`): The ``hidden_size`` to pass to actor-nn's ``Head``.
            - actor_head_layer_num (:obj:`int`):
                The num of layers used in the network to compute Q value output for actor's nn.
            - critic_head_hidden_size (:obj:`Optional[int]`): The ``hidden_size`` to pass to critic-nn's ``Head``.
            - critic_head_layer_num (:obj:`int`):
                The num of layers used in the network to compute Q value output for critic's nn.
            - activation (:obj:`Optional[nn.Module]`):
                The type of activation function to use in ``MLP`` the after ``layer_fn``,
                if ``None`` then default set to ``nn.ReLU()``
            - norm_type (:obj:`Optional[str]`):
                The type of normalization to use, see ``ding.torch_utils.fc_block`` for more details`
        """
        super(DEVAC, self).__init__()
        obs_shape: int = squeeze(obs_shape)
        action_shape = squeeze(action_shape)
        self.obs_shape, self.action_shape = obs_shape, action_shape
        self.impala_cnn_encoder = impala_cnn_encoder
        self.share_encoder = share_encoder

        # Encoder Type
        def new_encoder(outsize):
            if impala_cnn_encoder:
                return IMPALAConvEncoder(obs_shape=obs_shape, channels=encoder_hidden_size_list, outsize=outsize)
            else:
                if isinstance(obs_shape, int) or len(obs_shape) == 1:
                    return FCEncoder(
                        obs_shape=obs_shape,
                        hidden_size_list=encoder_hidden_size_list,
                        activation=activation,
                        norm_type=norm_type
                    )
                elif len(obs_shape) == 3:
                    return ConvEncoder(
                        obs_shape=obs_shape,
                        hidden_size_list=encoder_hidden_size_list,
                        activation=activation,
                        norm_type=norm_type
                    )
                else:
                    raise RuntimeError(
                        "not support obs_shape for pre-defined encoder: {}, please customize your own encoder".
                        format(obs_shape)
                    )

        if encoder:
            raise NotImplementedError()
        else:
            self.actor_encoder = nn.ModuleList([new_encoder(actor_head_hidden_size) for _ in range(len(action_shape))])
            self.critic_encoder = new_encoder(critic_head_hidden_size)

        # Head Type
        self.critic_head = RegressionHead(
            critic_head_hidden_size, 1, critic_head_layer_num, activation=activation, norm_type=norm_type
        )
        self.action_space = action_space

        if self.action_space == 'discrete':
            actor_head_cls = DiscreteHead
            multi_head = not isinstance(action_shape, int)
            self.multi_head = multi_head
            assert multi_head
            self.actor_head = nn.ModuleList(
                [
                    actor_head_cls(
                        actor_head_hidden_size, i, actor_head_layer_num, activation=activation, norm_type=norm_type
                    ) for i in action_shape
                ]
            )
        else:
            raise NotImplementedError()

        # must use list, not nn.ModuleList
        self.actor = [self.actor_encoder, self.actor_head]
        self.critic = [self.critic_encoder, self.critic_head]
        # Convenient for calling some apis (e.g. self.critic.parameters()),
        # but may cause misunderstanding when `print(self)`
        self.actor = nn.ModuleList(self.actor)
        self.critic = nn.ModuleList(self.critic)

    def forward(self, inputs: Union[torch.Tensor, Dict], mode: str) -> Dict:
        assert mode in self.mode, "not support forward mode: {}/{}".format(mode, self.mode)
        return getattr(self, mode)(inputs)

    def compute_actor(self, x: torch.Tensor) -> Dict:
        return lists_to_dicts([self.actor_head[i](self.actor_encoder[i](x)) for i in range(len(self.action_shape))])

    def compute_critic(self, x: torch.Tensor) -> Dict:
        x = self.critic_encoder(x)
        x = self.critic_head(x)
        return {'value': x['pred']}

    def compute_actor_critic(self, x: torch.Tensor) -> Dict:
        critic_embedding = self.critic_encoder(x)
        value = self.critic_head(critic_embedding)['pred']

        logit = lists_to_dicts([self.actor_head[i](self.actor_encoder[i](x))
                                for i in range(len(self.action_shape))])['logit']
        return {'logit': logit, 'value': value}
