import argparse
import os
import sqlite3
from typing import List, Optional, Tuple

import requirements


def pkg_str_to_dict(pkg_str: str) -> dict:
    pkgs = pkg_str.split(', ')
    output = {}
    for item in pkgs:
        name, version = item.split(' ')
        output[name] = version
    return output


def pkg_dict_to_str(pkg_dict: dict) -> str:
    pkgs = [f'{name} {version}' for name, version in pkg_dict.items()]
    return ', '.join(pkgs)


def process_pkg_str(pkg_str: str) -> str:
    pkgs = sorted([item.split(' ')[0].lower().replace('-', '_') for item in pkg_str.split(', ')])
    return ', '.join(pkgs)


def parse_requirements(requirements_file: str) -> List[str]:
    requirements_file_list = requirements_file.split(',')
    pkgs = set()
    for file in requirements_file_list:
        print(f'Parsing requirements file: {file}')
        with open(file) as f:
            for req in requirements.parse(f):
                print(f'Adding package: {req.name}')
                if req.name:
                    pkgs.add(req.name.lower().replace('-', '_'))
    return sorted(pkgs)


def extract_core_pkg_str(pkg_str: str, core_pkgs: List[str]) -> str:
    pkg_dict = pkg_str_to_dict(pkg_str)
    core_pkg_dict = {}
    for core_pkg in core_pkgs:
        if core_pkg in pkg_dict:
            core_pkg_dict[core_pkg] = pkg_dict[core_pkg]
    return pkg_dict_to_str(core_pkg_dict)


def environment_exist(target: Tuple[str, str], environments: List[Tuple[str, str]], include_packages: Optional[List[str]] = None):
    if include_packages is not None:
        target = (extract_core_pkg_str(target[0], include_packages), target[1])
        environments = [(extract_core_pkg_str(env[0], include_packages), env[1]) for env in environments]
    target = (process_pkg_str(target[0]), target[1])
    environments = [(process_pkg_str(env[0]), env[1]) for env in environments]
    return target in environments
