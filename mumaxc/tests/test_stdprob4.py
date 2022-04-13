import glob
import os
import shutil

import discretisedfield as df
import pytest

import mumaxc as mc


@pytest.mark.oommf
def test_stdprob4():
    name = "stdprob4"

    # Remove any previous simulation directories.
    if os.path.exists(name):
        shutil.rmtree(name)

    L, d, th = 500e-9, 125e-9, 3e-9  # (m)
    cellsize = (5e-9, 5e-9, 3e-9)  # (m)
    mesh = mc.Mesh((0, 0, 0), (L, d, th), cellsize)

    system = mc.System(name=name)

    A = 1.3e-11  # (J/m)
    system.hamiltonian = mc.Exchange(A) + mc.Demag()

    gamma = 2.211e5  # (m/As)
    alpha = 0.02
    system.dynamics = mc.Precession(gamma) + mc.Damping(alpha)

    Ms = 8e5  # (A/m)
    system.m = df.Field(mesh, value=(1, 0.25, 0.1), norm=Ms)

    md = mc.MinDriver()
    md.drive(system)  # updates system.m in-place

    dirname = os.path.join(name, "drive-{}".format(system.drive_number - 1))
    mx3filename = os.path.join(dirname, "{}.mx3".format(name))
    assert os.path.exists(dirname)
    assert os.path.isfile(mx3filename)

    omf_files = list(glob.iglob("{}/**/*.o*f".format(dirname), recursive=True))
    txt_files = list(glob.iglob("{}/**/*.txt".format(dirname), recursive=True))

    assert len(omf_files) == 3
    omffilename = os.path.join(dirname, "m0.omf")
    assert omffilename in omf_files

    assert len(txt_files) == 2
    shutil.rmtree(name)

    H = (-24.6e-3 / mc.mu0, 4.3e-3 / mc.mu0, 0)
    system.hamiltonian += mc.Zeeman(H)

    td = mc.TimeDriver()
    td.drive(system, t=1e-9, n=200)

    dirname = os.path.join(name, "drive-{}".format(system.drive_number - 1))
    mx3filename = os.path.join(dirname, "{}.mx3".format(name))
    assert os.path.exists(dirname)
    assert os.path.isfile(mx3filename)

    omf_files = list(glob.iglob("{}/**/*.o*f".format(dirname), recursive=True))
    txt_files = list(glob.iglob("{}/**/*.txt".format(dirname), recursive=True))

    assert len(omf_files) == 202
    omffilename = os.path.join(dirname, "m0.omf")
    assert omffilename in omf_files

    assert len(txt_files) == 2

    t = system.dt["t"].values
    my = system.dt["my"].values

    assert abs(min(t) - 5e-12) < 1e-20
    assert abs(max(t) - 1e-9) < 1e-20

    # Eye-norm test.
    assert 0.7 < max(my) < 0.8
    assert -0.5 < min(my) < -0.4

    shutil.rmtree(name)
