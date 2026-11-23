import discretisedfield as df
import micromagneticdata as mdata
import micromagneticmodel as mm
import pytest
from micromagneticdata.testing.drive import *  # noqa: F403

import mumax3c as mc


def rectangle(dirname, mode):
    """Simple rectangular ferromagnetic sample in external magnetic field."""
    print(">>> Running ferromagnetic rectangular cuboid")
    p1 = (-50e-9, -25e-9, 0)
    p2 = (50e-9, 25e-9, 20e-9)
    cell = (5e-9, 5e-9, 5e-9)

    region = df.Region(p1=p1, p2=p2)
    # use the region also as subregion: discretisedfield will create the additional
    # subregions json file and we can detect misalignment (translation) of the
    # region from the calculators (e.g. Mumax3 always defines pmin at the origin)
    mesh = df.Mesh(region=region, cell=cell, subregions={"total": region})

    Ms = 8e5
    A = 1.3e-11
    H = (1e6, 0.0, 2e5)
    alpha = 0.02

    system = mm.System(name="rectangle")
    system.energy = mm.Exchange(A=A) + mm.Zeeman(H=H)
    system.dynamics = mm.Precession(gamma0=mm.consts.gamma0) + mm.Damping(alpha=alpha)
    system.m = df.Field(mesh, nvdim=3, value=(0.0, 0.25, 0.1), norm=Ms)

    if mode == "time_drive":
        td = mc.TimeDriver()
        td.drive(system, t=25e-12, n=25, dirname=dirname)
    elif mode == "min_drive":
        md = mc.MinDriver()
        md.drive(system, dirname=dirname)
    elif mode == "relax_drive":
        rd = mc.RelaxDriver()
        rd.drive(system, output_step=True, dirname=dirname)
    else:
        raise NotImplementedError(mode)

    return system


@pytest.fixture(
    scope="session",
    params=[
        (rectangle, ("min_drive",), ("t", "mx", "minimize()")),
        (rectangle, ("relax_drive",), ("t", "mx", "relax()")),
        (
            rectangle,
            ("time_drive",),
            ("t", "mx", "run(1e-12)"),  # llg, 25 ps in 25 steps -> 1ps per iteration
        ),
    ],
)
def _compute(tmp_path_factory, request):
    # compute test data once and reuse for all tests; separate public fixtures to create
    # a new drive object per test/fixture call to ensure tests stay independent
    callback, args, reference = request.param
    dirname = tmp_path_factory.mktemp(callback.__name__ + args[0])
    system = callback(dirname, *args)
    return system.name, system.drive_number - 1, dirname, reference


@pytest.fixture
def drive_with_reference(_compute):
    name, number, dirname, reference = _compute
    return mdata.Drive(name=name, number=number, dirname=dirname), reference


@pytest.fixture
def drive(_compute):
    name, number, dirname, _ = _compute
    return mdata.Drive(name=name, number=number, dirname=dirname)


@pytest.fixture
def expected_field_type():
    return df.Field


def test_magnetisation_geometry(drive):
    """Magnetisation steps are aligned with the initial region and subregions."""
    assert drive[0].mesh.region.allclose(drive.m0.mesh.region)
    assert drive[0].mesh.subregions.keys() == drive.m0.mesh.subregions.keys()


def test_ovf2vtk(drive, tmp_path):
    drive.ovf2vtk(dirname=tmp_path)
