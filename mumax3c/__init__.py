import pkg_resources
import pytest

import mumax3c.mumax3
import mumax3c.scripts

from .compute import compute
from .delete import delete
from .drivers import MinDriver, TimeDriver, RelaxDriver


def test():
    return pytest.main(
        ["-m", "not travis and not docker", "-v", "--pyargs", "mumax3c"]
    )  # pragma: no cover


def test_docker():
    return pytest.main(
        ["-m", "docker", "-v", "--pyargs", "mumax3c"]
    )  # pragma: no cover


__version__ = pkg_resources.get_distribution(__name__).version
__dependencies__ = pkg_resources.require(__name__)
