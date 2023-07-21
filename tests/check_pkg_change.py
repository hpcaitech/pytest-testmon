import tempfile

from testmon.utils import environment_exist, parse_requirements


def check_parse_requirements() -> None:
    with tempfile.NamedTemporaryFile(mode='w') as f:
        f.write('torch\ntorchx-nightly\nSentencePiece\n')
        f.flush()
        pkgs = parse_requirements(f.name)
        assert pkgs == ['sentencepiece', 'torch', 'torchx_nightly'], pkgs
        with tempfile.NamedTemporaryFile(mode='w') as f2:
            f2.write('torch\nflash-attn\n')
            f2.flush()
            pkgs = parse_requirements(f.name + ',' + f2.name)
            assert pkgs == ['flash_attn', 'sentencepiece', 'torch', 'torchx_nightly'], pkgs


def check_environment_exist():
    core_pkgs = ['flash_attn', 'sentencepiece', 'torch', 'torchx_nightly']
    target = ('flash_attn 0.0.1, sentencepiece 0.1.9, torch 1.9.0, torchx_nightly 0.0.1, urllib3 1.26.12', '3.8.5')
    environments = [
        ('flash_attn 0.0.1, sentencepiece 0.1.9, torch 1.9.0, torchx_nightly 0.0.1, urllib3 1.26.11', '3.8.5'),
        ('flash_attn 0.0.1, sentencepiece 0.1.9, torch 1.9.0, torchx_nightly 0.0.1, urllib3 1.26.11', '3.9.5'),
        ('flash_attn 0.0.1, sentencepiece 0.1.9, torch 1.9.0, torchx_nightly 0.0.1, urllib3 1.26.11', '3.8.5'),
        ('flash_attn 0.0.1, torch 1.9.0, torchx_nightly 0.0.1', '3.8.5'),
    ]
    assert environment_exist(target, environments, core_pkgs)
    environments.pop(0)
    assert environment_exist(target, environments, core_pkgs)
    environments.pop(1)
    assert not environment_exist(target, environments, core_pkgs)


if __name__ == '__main__':
    check_parse_requirements()
    check_environment_exist()
