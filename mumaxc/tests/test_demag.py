import mumaxc as mc
import micromagneticmodel.tests as mmt


class TestDemag(mmt.TestDemag):
    def test_script(self):
        demag = mc.Demag()

        script = demag._script
        assert script.count("\n") == 3
        assert script[0:2] == "//"
        assert script[-1] == "\n"

        lines = script.split("\n")
        assert len(lines) == 4
        assert lines[0] == "// Demag"
        assert lines[1] == "enabledemag=true"
