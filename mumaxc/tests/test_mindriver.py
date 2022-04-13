import glob
import os
import shutil

import pytest

import mumaxc as oc

from .test_driver import TestDriver


class TestMinDriver(TestDriver):
    @pytest.mark.xfail
    def test_script(self):
        if os.path.exists("tds"):
            shutil.rmtree("tds")
        md = oc.MinDriver()

        #  XFAIL here: driver has not been initialised completely because that code is currently in the drive() method
        script = md._script(self.system)

        assert script[0] == "#"
        assert script[-1] == "1"
        assert script.count("#") == 5
        assert script.count("Specify") == 3
        assert script.count("Destination") == 2
        assert script.count("Schedule") == 2
        assert script.count("mmArchive") == 2
        assert script.count("Stage") == 2

        assert "Oxs_CGEvolve" in script
        assert "Oxs_MinDriver" in script
        assert "Oxs_FileVectorField" in script

        if os.path.exists("tds"):
            shutil.rmtree("tds")

    @pytest.mark.mumax
    def test_drive(self):
        # in case of previous test failure
        if os.path.exists("tds"):
            shutil.rmtree("tds")

        md = oc.MinDriver()

        drive_number = self.system.drive_number

        md.drive(self.system)

        dirname = os.path.join("tds", f"drive-{drive_number}")
        assert os.path.exists(dirname)

        expect_input_files = [
            os.path.join(dirname, "tds.mx3"),
            md.omffilename,
            md.omfregionsfilename,
        ]
        for ef in expect_input_files:
            assert os.path.isfile(ef)

        out_dirname = os.path.join(dirname, "tds.out")

        expect_output_files = ["table.txt"]
        for ef in expect_output_files:
            full_path = os.path.join(out_dirname, ef)
            assert os.path.isfile(full_path)

        assert len(list(glob.iglob(os.path.join(out_dirname, "*.o*f")))) == 1

        if os.path.exists("tds"):
            shutil.rmtree("tds")
