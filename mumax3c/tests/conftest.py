import pytest

import mumax3c as mc


@pytest.fixture(scope="module")
def calculator():
    return mc


@pytest.fixture  # (scope='module')
def skip_condition(calculator):
    if calculator.__name__ == "mumax3c":
        pytest.skip()
