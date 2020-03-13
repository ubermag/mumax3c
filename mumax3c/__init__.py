import pytest
import pkg_resources
import mumax3c.mumax3
import mumax3c.scripts
from .delete import delete
from .compute import compute
from .drivers import MinDriver, TimeDriver


def test():
    return pytest.main(['-m', 'not travis and not docker',
                        '-v', '--pyargs', 'mumax3c'])  # pragma: no cover


def test_docker():
    return pytest.main(['-m', 'docker', '-v',
                        '--pyargs', 'mumax3c'])  # pragma: no cover


__version__ = pkg_resources.get_distribution(__name__).version
__dependencies__ = pkg_resources.require(__name__)
