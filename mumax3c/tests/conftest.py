import pytest
import mumax3c as calc


@pytest.fixture(scope='module')
def calculator():
    return calc
