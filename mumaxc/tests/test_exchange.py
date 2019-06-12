import mumaxc as mc
import micromagneticmodel.tests as mmt


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
            assert lines[0] == "// UniformExchange".format(A)
            assert lines[1] == "Aex={}".format(A)
