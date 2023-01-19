import discretisedfield as df
import micromagneticmodel as mm
import numpy as np
import pytest

import mumax3c as mc


def test_mumax3_regions__no_subregion():
    mesh = df.Mesh(p1=(0, 0, 0), p2=(2, 2, 2), cell=(1, 1, 1))
    system = mm.System(name="test")
    system.m = df.Field(mesh, nvdim=3, value=(0, 0, 1), norm=1)

    subregion_values, subregions_dict = mc.scripts.util._identify_subregions(system)
    assert np.allclose(subregion_values, 0)
    assert len(subregions_dict) == 1

    mc.scripts.mumax3_regions(system)
    subregions = df.Field.from_file("mumax3_regions.omf")
    assert np.allclose(subregions.array, 0.0)
    assert hasattr(system, "region_relator")
    assert system.region_relator == {"": [0]}


def test_mumax3_regions__two_subregions():
    subregions = {
        "r1": df.Region(p1=(0, 0, 0), p2=(2, 2, 1)),
        "r2": df.Region(p1=(0, 0, 1), p2=(2, 2, 2)),
    }
    mesh = df.Mesh(p1=(0, 0, 0), p2=(2, 2, 2), cell=(1, 1, 1), subregions=subregions)
    system = mm.System(name="test")
    system.m = df.Field(mesh, nvdim=3, value=(0, 0, 1), norm=1)

    subregion_values, subregions_dict = mc.scripts.util._identify_subregions(system)
    assert subregion_values[0, 0, 0, 0] == 1
    assert subregion_values[1, 1, 1, 0] == 2
    assert len(subregions_dict) == 3
    assert subregions_dict == {0: "", 1: "r1", 2: "r2"}

    mc.scripts.util.mumax3_regions(system)
    subregions = df.Field.from_file("mumax3_regions.omf")
    assert np.allclose(np.unique(subregions.array), [0.0, 1.0])
    assert hasattr(system, "region_relator")
    assert system.region_relator == {"": [], "r1": [0], "r2": [1]}


def test_mumax3_regions__two_subregions_gap_ms():
    subregions = {
        "r1": df.Region(p1=(0, 0, 0), p2=(2, 2, 1)),
        "r2": df.Region(p1=(0, 0, 2), p2=(2, 2, 3)),
    }
    mesh = df.Mesh(p1=(0, 0, 0), p2=(2, 2, 3), cell=(1, 1, 1), subregions=subregions)
    system = mm.System(name="test")

    def ms_fun(pos):
        x, _, _ = pos
        return x

    system.m = df.Field(mesh, nvdim=3, value=(0, 0, 1), norm=ms_fun)

    subregion_values, subregions_dict = mc.scripts.util._identify_subregions(system)
    assert subregion_values[0, 0, 0, 0] == 1
    assert subregion_values[1, 1, 1, 0] == 0
    assert subregion_values[1, 1, 2, 0] == 2
    assert len(subregions_dict) == 3
    assert subregions_dict == {0: "", 1: "r1", 2: "r2"}

    mc.scripts.util.mumax3_regions(system)
    subregions = df.Field.from_file("mumax3_regions.omf")
    assert np.allclose(np.unique(subregions.array), [0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
    assert hasattr(system, "region_relator")
    assert system.region_relator == {"": [0, 1], "r1": [2, 3], "r2": [4, 5]}

    def ms_fun(pos):
        x, _, _ = pos
        if x < 1:
            return 0
        return 1

    system.m = df.Field(mesh, nvdim=3, value=(0, 0, 1), norm=ms_fun)

    mc.scripts.util.mumax3_regions(system)
    subregions = df.Field.from_file("mumax3_regions.omf")
    assert np.allclose(np.unique(subregions.array), [0, 1, 2, 255])
    assert hasattr(system, "region_relator")
    assert system.region_relator == {"": [0], "r1": [1], "r2": [2]}


def test_identify_subregions__two_overlaping_subregions():
    subregions = {
        "r1": df.Region(p1=(0, 0, 0), p2=(2, 2, 1)),
        "r2": df.Region(p1=(0, 0, 0), p2=(2, 2, 2)),
    }
    mesh = df.Mesh(p1=(0, 0, 0), p2=(2, 2, 2), cell=(1, 1, 1), subregions=subregions)
    system = mm.System(name="test")
    system.m = df.Field(mesh, nvdim=3, value=(0, 0, 1), norm=1)

    subregion_values, subregions_dict = mc.scripts.util._identify_subregions(system)
    assert subregion_values[0, 0, 0, 0] == 1
    assert subregion_values[1, 1, 1, 0] == 2
    assert len(subregions_dict) == 3

    mc.scripts.util.mumax3_regions(system)
    subregions = df.Field.from_file("mumax3_regions.omf")
    assert np.allclose(np.unique(subregions.array), [0, 1])
    assert hasattr(system, "region_relator")
    assert system.region_relator == {"": [], "r1": [0], "r2": [1]}

    subregions = {
        "r1": df.Region(p1=(0, 0, 0), p2=(2, 2, 2)),
        "r2": df.Region(p1=(0, 0, 0), p2=(2, 2, 1)),
    }
    mesh = df.Mesh(p1=(0, 0, 0), p2=(2, 2, 2), cell=(1, 1, 1), subregions=subregions)
    system = mm.System(name="test")
    system.m = df.Field(mesh, nvdim=3, value=(0, 0, 1), norm=1)

    subregion_values, subregions_dict = mc.scripts.util._identify_subregions(system)
    assert subregion_values[0, 0, 0, 0] == 1
    assert subregion_values[1, 1, 1, 0] == 1
    assert len(subregions_dict) == 3

    mc.scripts.util.mumax3_regions(system)
    subregions = df.Field.from_file("mumax3_regions.omf")
    assert np.allclose(np.unique(subregions.array), [0])
    assert hasattr(system, "region_relator")
    assert system.region_relator == {"": [], "r1": [0], "r2": []}


def test_identify_subregions__three_subregions():
    subregions = {
        "r1": df.Region(p1=(0, 0, 0), p2=(2, 2, 1)),
        "r2": df.Region(p1=(0, 0, 1), p2=(2, 2, 2)),
        "r3": df.Region(p1=(0, 0, 2), p2=(2, 2, 3)),
    }
    mesh = df.Mesh(p1=(0, 0, 0), p2=(2, 2, 3), cell=(1, 1, 1), subregions=subregions)
    system = mm.System(name="test")
    system.m = df.Field(mesh, nvdim=3, value=(0, 0, 1), norm=1)

    subregion_values, subregions_dict = mc.scripts.util._identify_subregions(system)
    assert subregion_values[0, 0, 0, 0] == 1
    assert subregion_values[1, 1, 1, 0] == 2
    assert subregion_values[1, 1, 2, 0] == 3
    assert len(subregions_dict) == 4

    mc.scripts.util.mumax3_regions(system)
    subregions = df.Field.from_file("mumax3_regions.omf")
    assert np.allclose(np.unique(subregions.array), [0, 1, 2])
    assert hasattr(system, "region_relator")
    assert system.region_relator == {"": [], "r1": [0], "r2": [1], "r3": [2]}


def test_mumax3_regions__too_many_ms():
    subregions = {
        "r1": df.Region(p1=(0, 0, 0), p2=(200, 2, 1)),
        "r2": df.Region(p1=(0, 0, 2), p2=(200, 2, 3)),
    }
    mesh = df.Mesh(p1=(0, 0, 0), p2=(200, 2, 3), cell=(1, 1, 1), subregions=subregions)
    system = mm.System(name="test")

    def ms_fun(pos):
        x, y, z = pos
        return x

    system.m = df.Field(mesh, nvdim=3, value=(0, 0, 1), norm=ms_fun)
    with pytest.raises(ValueError):
        mc.scripts.mumax3_regions(system)
