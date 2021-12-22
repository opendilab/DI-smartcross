import os
import yaml
import logging
from easydict import EasyDict
from importlib import import_module
import xml.etree.ElementTree as ET
import random

from ding.utils import deep_merge_dicts


def read_ding_config(cfg_path):
    suffix = cfg_path.split('.')[-1]
    if suffix == 'py':
        cfg_module = os.path.splitext(cfg_path)[0]
        cfg_module = cfg_module.replace('/', '.')
        module = import_module(cfg_module)
        cfg_dict = {k: v for k, v in module.__dict__.items() if not k.startswith('_')}
    elif suffix == 'yaml':
        with open(cfg_path, 'r') as f:
            cfg_dict = yaml.safe_load(f)
        cfg_dict = EasyDict(cfg_dict)
    else:
        raise KeyError("invalid config file suffix: {}".format(suffix))

    assert "main_config" in cfg_dict, "Please make sure a 'main_config' variable is declared in config python file!"
    assert "create_config" in cfg_dict, "Please make sure a 'create_config' variable is declared in config python file!"
    return cfg_dict['main_config'], cfg_dict['create_config']


def get_sumo_config(args):
    ding_cfg = args.ding_cfg
    main_cfg, create_config = read_ding_config(ding_cfg)

    with open(args.env_cfg, 'r') as f:
        sumoenv_cfg = yaml.safe_load(f)
    sumoenv_cfg = EasyDict(sumoenv_cfg)
    main_cfg = deep_merge_dicts(sumoenv_cfg, main_cfg)

    return main_cfg, create_config
