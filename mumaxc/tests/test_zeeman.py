import micromagneticmodel.tests as mmt

import mumaxc as mc


class TestZeeman(mmt.TestZeeman):
    def test_script(self):
        for H in self.valid_args:
            zeeman = mc.Zeeman(H=H)

            script = zeeman._script
            assert script.count("\n") == 3
            assert script[0:2] == "//"
            assert script[-1] == "\n"

            lines = script.split("\n")
            assert len(lines) == 4
            assert lines[0] == "// Zeeman"
            assert lines[1] == "B_ext=vector({}*mu0mm,{}*mu0mm,{}*mu0mm)".format(*H)
