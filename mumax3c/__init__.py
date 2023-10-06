"""Mumax3 calculator."""
import importlib.metadata

import pytest

import mumax3c.mumax3
import mumax3c.scripts

# from .compute import compute  # compute is not yet supported
from .delete import delete
from .drivers import MinDriver, RelaxDriver, TimeDriver

runner = mumax3c.mumax3.Runner()
"""Controls the default runner.

``runner`` gives access to the default mumax3 runner used by ``mumxa3c``. For
details refer to ``mumax3c.mumax3.Runner``.

Examples
--------
``runner.runner``
    Returns the default runner; selects the best available runner if unset. A
    different ``Mumax3Runner`` can be passed to be used instead. The new runner
    is tested first.

``runner.autoselect_runner()``
    Lets ``mumax3c`` select the best runner. Can be used to reset the runner
    after overwriting it manually.

See Also
--------
:py:class:`~mumax3c.mumax3.Runner`

"""


def test():
    """Run all package tests.

    Examples
    --------
    1. Run all tests.

    >>> import mumax3c as mc
    ...
    >>> # mc.test()

    """
    return pytest.main(
        ["-m", "not travis and not docker", "-v", "--pyargs", "mumax3c"]
    )  # pragma: no cover


def test_docker():
    return pytest.main(
        ["-m", "docker", "-v", "--pyargs", "mumax3c"]
    )  # pragma: no cover


__version__ = importlib.metadata.version(__package__)
