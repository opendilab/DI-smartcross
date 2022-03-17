from typing import Dict, List


def squeeze_obs(obs: Dict) -> List:
    assert obs is not None
    if isinstance(obs, dict):
        return [value for key in sorted(obs) for value in squeeze_obs(obs[key])]
    elif isinstance(obs, (tuple, list, set)):
        return [value for item in obs for value in squeeze_obs(item)]
    elif isinstance(obs, (int, float, str)):
        return (obs, )
    else:
        raise ValueError('Cannot process type: {}, {}'.format(type(obs), obs))


def get_suffix_num(input: str) -> List:
    tmp = input.split('_')
    res = [int(t) for t in tmp[1:]]
    return res


def get_onehot_obs(obs: List, length: int) -> List:
    res = []
    for item in obs:
        onehot = [0] * length
        onehot[item] = 1
        res += onehot
    return res


