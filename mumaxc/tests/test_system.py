import discretisedfield as df
import pytest

import mumaxc as mc


class TestSystem:
    @pytest.mark.mumax
    def test_script(self):
        system = mc.System(name="test_system")

        system.hamiltonian += mc.Exchange(1e-12)
        system.hamiltonian += mc.Demag()
        system.hamiltonian += mc.UniaxialAnisotropy(1e3, (0, 1, 0))
        system.hamiltonian += mc.Zeeman((0, 1e6, 0))

        system.dynamics += mc.Precession(2.211e5)
        system.dynamics += mc.Damping(0.1)

        mesh = mc.Mesh((0, 0, 0), (5, 5, 5), (1, 1, 1))

        system.m = df.Field(mesh, dim=3, value=(0, 1, 0), norm=1)

        script = system._script

        assert script[-1] == "\n"
        assert "mu0mm" in script
        assert "SetGridSize(5, 5, 5)" in script
        assert "SetCellSize(1, 1, 1)" in script
        assert "Aex=1e-12" in script
        assert "enabledemag=true" in script
        assert "B_ext=vector(0*mu0mm,1000000.0*mu0mm,0*mu0mm)" in script
        assert "Ku1=1000.0" in script
        assert "Ku2=0" in script
        assert "anisu=vector(0,1,0)" in script

        return None

    @pytest.mark.mumax
    def test_total_energy(self):
        system = mc.System(name="test_system")

        system.hamiltonian += mc.Exchange(1e-12)
        system.hamiltonian += mc.UniaxialAnisotropy(1e3, (0, 1, 0))
        system.hamiltonian += mc.Zeeman((0, 1e6, 0))

        system.dynamics += mc.Precession(2.211e5)
        system.dynamics += mc.Damping(0.1)

        mesh = mc.Mesh((0, 0, 0), (5, 5, 5), (1, 1, 1))

        system.m = df.Field(mesh, dim=3, value=(0, 1, 0), norm=1)

        with pytest.raises(AttributeError):
            system.total_energy()

        return None
