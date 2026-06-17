import pytest
from micromagneticdata.testing.drive import *  # noqa: F403

# Additional mumax3 specific tests


@pytest.fixture
def calculator_script_content():
    return "tableadd"
