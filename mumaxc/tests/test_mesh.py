import pytest
import re
import mumaxc as oc
import discretisedfield.tests as dft


fp_regex = "[-+]?[0-9]*.?[0-9]+([eE][-+]?[0-9]+)?"
coord_regex = f"\\({fp_regex}, {fp_regex}, {fp_regex}\\)"


class TestMesh(dft.TestMesh):
    def test_script_no_pbc(self):
        for p1, p2, cell in self.valid_args:
            name = "test_mesh"
            mesh = oc.Mesh(p1, p2, cell, name=name)
            script = mesh._script
            assert len(re.findall("SetGridSize" + coord_regex, script)) == 1
            assert len(re.findall("SetCellSize" + coord_regex, script)) == 1

    @pytest.mark.xfail
    def test_script_pbc(self):
        raise NotImplementedError
