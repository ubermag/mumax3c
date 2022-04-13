import micromagneticmodel.tests as mmt

import mumaxc as mc


class TestCubicAnisotropy(mmt.TestCubicAnisotropy):
    def test_script(self):
        for K1, u1, u2 in self.valid_args:
            anisotropy = mc.CubicAnisotropy(K1=K1, u1=u1, u2=u2)
            script = anisotropy._script

            assert script.count("\n") == 5
            assert script[0:2] == "//"
            assert script[-1] == "\n"
            lines = script.split("\n")
            assert len(lines) == 6
            assert lines[0] == "// CubicAnisotropy"
            assert lines[1] == "Kc1={}".format(K1)
            assert lines[2] == "anisC1=vector({},{},{})".format(*u1)
            assert lines[3] == "anisC2=vector({},{},{})".format(*u2)
