import micromagneticmodel.tests as mmt

import mumaxc as mc


class TestUniaxialAnisotropy(mmt.TestUniaxialAnisotropy):
    def test_script(self):
        for K1, K2, u in self.valid_args:
            anisotropy = mc.UniaxialAnisotropy(K1=K1, K2=K2, u=u)
            script = anisotropy._script

            assert script[0:2] == "//"
            assert script[-1] == "\n"
            lines = script.split("\n")
            assert lines[0] == "// UniaxialAnisotropy"
            assert lines[1] == "Ku1={}".format(K1)
            assert lines[2] == "Ku2={}".format(K2)
            assert lines[3] == "anisu=vector({},{},{})".format(*u)

            assert script.count("\n") == 5
            assert len(lines) == 6
