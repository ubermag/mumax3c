import sys
import pytest
import mumaxc as mc
import micromagneticmodel.tests as mmt

class TestDMI(mmt.TestDMI):

    def test_script_cnv(self):
        for D in self.valid_args:
            dmi = mc.DMI(D, crystalclass='cnv')

            script = dmi._script
            assert script.count("\n") == 3
            assert script[0:2] == "//"
            assert script[-1] == "\n"

            lines = script.split("\n")
            assert len(lines) == 4
            assert lines[0] == "// DMI of crystallographic class Cnv"
            assert lines[1] == "Dind={}".format(-D)

    def test_valueerror(self):
        with pytest.raises(ValueError):
            dmi = mc.DMI(D=1, crystalclass='pluto')
            dmi._script
