from pathlib import Path

import pytest
from ubermagtable.tests.test_table import *  # noqa: F401,F403

from mumax3c._output_collecting_util.read_table import table_from_file

llg_files = [
    "mumax3-file1.txt",
]

energy_minimisation_files = []

relaxation_files = []


def _read_table(filename):
    dirname = Path(__file__).parent / "test_sample" / "tables"

    def _inner(**kwargs):
        return table_from_file(dirname / filename, **kwargs)

    return _inner


@pytest.fixture(params=llg_files + energy_minimisation_files + relaxation_files)
def table_llg_factory(request):
    return _read_table(request.param)


@pytest.fixture(params=llg_files)
def table_factory(request):
    return _read_table(request.param)


@pytest.fixture
def table_llg_25ps():
    pytest.skip("no suitable data")


@pytest.fixture(params=energy_minimisation_files)
def table_minimisation_factory(request):
    pytest.skip("no data available")


@pytest.fixture
def table_hysteresis_factory():
    pytest.skip("Hysteresis simulations not supported by mumax3.")
