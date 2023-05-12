from functools import partial

import torch.multiprocessing as mp
from sample import Sample


def check_get_rank(rank: int, world_size: int) -> None:
    sample = Sample(rank, world_size)
    assert sample.get_rank() == rank


def check_get_world_size(rank: int, world_size: int) -> None:
    sample = Sample(rank, world_size)
    assert sample.get_world_size() == world_size


def test_get_rank():
    mp.spawn(partial(check_get_rank, world_size=2), nprocs=2)


def test_get_world_size():
    mp.spawn(partial(check_get_world_size, world_size=2), nprocs=2)
