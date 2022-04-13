import pytest

import mumax3c as calc


@pytest.fixture(scope="module")
def calculator():
    return calc


@pytest.fixture  # (scope='module')
def skip_condition(calculator):
    if calculator.__name__ == "mumax3c":
        pytest.skip()
