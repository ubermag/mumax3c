from pathlib import Path

import micromagneticdata as mdata
import pytest
from micromagneticdata.testing.drive import *  # noqa: F403


@pytest.fixture(
    params=[
        (0, ("t", "mx", "minimize()")),
        (1, ("t", "mx", "relax()")),
        (2, ("t", "mx", "run(1e-12)")),  # llg, 25 ps in 25 steps
    ]
)
def drive_with_reference(request):
    number, reference = request.param
    dirname = Path(__file__).parent / "test_sample" / "micromagneticdata"
    return mdata.Drive(name="rectangle", number=number, dirname=dirname), reference


@pytest.fixture
def drive(drive_with_reference):
    return drive_with_reference[0]


def test_ovf2vtk(drive, tmp_path):
    drive.ovf2vtk(dirname=tmp_path)
