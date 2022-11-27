import os
import yaml
from typing import Dict


def make_sure_dir_exists(filepath: str) -> None:
    filedir = os.path.dirname(filepath)
    if not os.path.exists(filedir):
        os.makedirs(filedir)


def load_yaml(filepath: str) -> Dict:
    with open(filepath, 'r', encoding='utf-8') as f:
        res = yaml.load(f.read(), Loader=yaml.FullLoader)
    return res


def dump_yaml(data: Dict, filepath: str) -> None:
    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(data, f)