import micromagneticmodel.tests as mmt

import mumaxc as mc


class TestExchange(mmt.TestExchange):
    def test_script(self):
        for A in self.valid_args:
            exchange = mc.Exchange(A)

            script = exchange._script
            assert script.count("\n") == 3
            assert script[0:2] == "//"
            assert script[-1] == "\n"

            lines = script.split("\n")
            assert len(lines) == 4
            assert lines[0] == "// UniformExchange"
            assert lines[1] == "Aex={}".format(A)
