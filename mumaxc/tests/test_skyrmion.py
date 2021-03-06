import os
import shutil
import pytest
import mumaxc as mc
import discretisedfield as df


@pytest.mark.mumax
def test_skyrmion():
    name = "skyrmion"

    # Remove any previous simulation directories.
    if os.path.exists(name):
        shutil.rmtree(name)

    mesh = mc.Mesh(p1=(-50e-9, -50e-9, 0),
                   p2=(50e-9, 50e-9, 10e-9),
                   cell=(5e-9, 5e-9, 5e-9))

    system = mc.System(name="skyrmion")
    system.hamiltonian = mc.Exchange(A=1.6e-11) + \
        mc.DMI(D=4e-3, crystalclass="cnv") + \
        mc.UniaxialAnisotropy(K1=0.51e6, K2=0.1, u=(0, 0, 1)) + \
        mc.Demag() + \
        mc.Zeeman(H=(0, 0, 2e5))

    Ms = 1.1e6

    def Ms_fun(pos):
        x, y, z = pos
        if (x**2 + y**2)**0.5 < 50e-9:
            return Ms
        else:
            return 0

    def m_init(pos):
        x, y, z = pos
        if (x**2 + y**2)**0.5 < 10e-9:
            return (0, 0.1, -1)
        else:
            return (0, 0.1, 1)

    system.m = df.Field(mesh, value=m_init, norm=Ms_fun)

    md = mc.MinDriver()
    md.drive(system)

    # Check the magnetisation at the sample centre.
    assert system.m((0, 0, 0))[2]/Ms < -0.97

    # Check the magnetisation at the sample edge.
    assert system.m((50e-9, 0, 0))[2]/Ms > 0

    shutil.rmtree(name)
