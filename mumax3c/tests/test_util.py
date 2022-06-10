import mumax3c as mc
import discretisedfield as df
import micromagneticmodel as mm
import numpy as np
import pytest


def test_identify_subregions_no_subregions():
    mesh = df.Mesh(p1=(0, 0, 0), p2=(2, 2, 2), cell=(1, 1, 1))
    system = mm.System(name='test')
    system.m = df.Field(mesh, dim=3, value=(0, 0, 1), norm=1)
    subregion_values, subregions_dict = mc.scripts.util.identify_subregions(system)
    assert np.allclose(subregion_values, 0)
    assert len(subregions_dict) == 1


def test_identify_subregions_two_subregions_gap():
    subregions = {'r1': df.Region(p1=(0, 0, 0), p2=(2, 2, 1)),
                  'r2': df.Region(p1=(0, 0, 2), p2=(2, 2, 3))}
    mesh = df.Mesh(p1=(0, 0, 0), p2=(2, 2, 3), cell=(1, 1, 1), subregions=subregions)
    system = mm.System(name='test')
    system.m = df.Field(mesh, dim=3, value=(0, 0, 1), norm=1)
    subregion_values, subregions_dict = mc.scripts.util.identify_subregions(system)
    assert subregion_values[0, 0, 0, 0] == 1
    assert subregion_values[1, 1, 1, 0] == 0
    assert subregion_values[1, 1, 2, 0] == 2
    assert len(subregions_dict) == 3


def test_identify_subregions_two_distinct_subregions():
    subregions = {'r1': df.Region(p1=(0, 0, 0), p2=(2, 2, 1)),
                  'r2': df.Region(p1=(0, 0, 1), p2=(2, 2, 2))}
    mesh = df.Mesh(p1=(0, 0, 0), p2=(2, 2, 2), cell=(1, 1, 1), subregions=subregions)
    system = mm.System(name='test')
    system.m = df.Field(mesh, dim=3, value=(0, 0, 1), norm=1)
    subregion_values, subregions_dict = mc.scripts.util.identify_subregions(system)
    assert subregion_values[0, 0, 0, 0] == 1
    assert subregion_values[1, 1, 1, 0] == 2
    assert len(subregions_dict) == 3


def test_identify_subregions_two_overlaping_subregions():
    subregions = {'r1': df.Region(p1=(0, 0, 0), p2=(2, 2, 1)),
                  'r2': df.Region(p1=(0, 0, 0), p2=(2, 2, 2))}
    mesh = df.Mesh(p1=(0, 0, 0), p2=(2, 2, 2), cell=(1, 1, 1), subregions=subregions)
    system = mm.System(name='test')
    system.m = df.Field(mesh, dim=3, value=(0, 0, 1), norm=1)
    subregion_values, subregions_dict = mc.scripts.util.identify_subregions(system)
    assert subregion_values[0, 0, 0, 0] == 1
    assert subregion_values[1, 1, 1, 0] == 2
    assert len(subregions_dict) == 3

    subregions = {'r1': df.Region(p1=(0, 0, 0), p2=(2, 2, 2)),
                  'r2': df.Region(p1=(0, 0, 0), p2=(2, 2, 1))}
    mesh = df.Mesh(p1=(0, 0, 0), p2=(2, 2, 2), cell=(1, 1, 1), subregions=subregions)
    system = mm.System(name='test')
    system.m = df.Field(mesh, dim=3, value=(0, 0, 1), norm=1)
    subregion_values, subregions_dict = mc.scripts.util.identify_subregions(system)
    assert subregion_values[0, 0, 0, 0] == 1
    assert subregion_values[1, 1, 1, 0] == 1
    assert len(subregions_dict) == 3


def test_identify_subregions_three_subregions():
    subregions = {'r1': df.Region(p1=(0, 0, 0), p2=(2, 2, 1)),
                  'r2': df.Region(p1=(0, 0, 1), p2=(2, 2, 2)),
                  'r3': df.Region(p1=(0, 0, 2), p2=(2, 2, 3))}
    mesh = df.Mesh(p1=(0, 0, 0), p2=(2, 2, 3), cell=(1, 1, 1), subregions=subregions)
    system = mm.System(name='test')
    system.m = df.Field(mesh, dim=3, value=(0, 0, 1), norm=1)
    subregion_values, subregions_dict = mc.scripts.util.identify_subregions(system)
    assert subregion_values[0, 0, 0, 0] == 1
    assert subregion_values[1, 1, 1, 0] == 2
    assert subregion_values[1, 1, 2, 0] == 3
    assert len(subregions_dict) == 4


def test_mumax3_no_subregion():
    mesh = df.Mesh(p1=(0, 0, 0), p2=(2, 2, 2), cell=(1, 1, 1))
    system = mm.System(name='test')
    system.m = df.Field(mesh, dim=3, value=(0, 0, 1), norm=1)
    _ = mc.scripts.util.mumax3_regions(system)
    subregions = df.Field.fromfile("subregions.omf")
    assert np.allclose(np.unique(subregions.array), 0.)
    assert hasattr(system, 'region_relators')
    assert system.region_relators == {'ee': [0]}


def test_mumax3_two_subregions():
    subregions = {'r1': df.Region(p1=(0, 0, 0), p2=(2, 2, 1)),
                  'r2': df.Region(p1=(0, 0, 1), p2=(2, 2, 2))}
    mesh = df.Mesh(p1=(0, 0, 0), p2=(2, 2, 2), cell=(1, 1, 1), subregions=subregions)
    system = mm.System(name='test')
    system.m = df.Field(mesh, dim=3, value=(0, 0, 1), norm=1)
    _ = mc.scripts.util.mumax3_regions(system)
    subregions = df.Field.fromfile("subregions.omf")
    assert np.allclose(np.unique(subregions.array), [0., 1.])
    assert hasattr(system, 'region_relators')
    assert system.region_relators == {'r1': [0], 'r2': [1], 'ee': []}


def test_mumax3_two_subregions_gap_ms():
    subregions = {'r1': df.Region(p1=(0, 0, 0), p2=(2, 2, 1)),
                  'r2': df.Region(p1=(0, 0, 2), p2=(2, 2, 3))}
    mesh = df.Mesh(p1=(0, 0, 0), p2=(2, 2, 3), cell=(1, 1, 1), subregions=subregions)
    system = mm.System(name='test')

    def ms_fun(pos):
        x, y, z = pos
        return x
    system.m = df.Field(mesh, dim=3, value=(0, 0, 1), norm=ms_fun)
    _ = mc.scripts.util.mumax3_regions(system)
    subregions = df.Field.fromfile("subregions.omf")
    assert np.allclose(np.unique(subregions.array), [0., 1., 2., 3., 4., 5.])
    assert hasattr(system, 'region_relators')
    assert system.region_relators == {'r1': [0, 1], 'r2': [2, 3], 'ee': [4, 5]}


def test_mumax3_too_many_ms():
    subregions = {'r1': df.Region(p1=(0, 0, 0), p2=(200, 2, 1)),
                  'r2': df.Region(p1=(0, 0, 2), p2=(200, 2, 3))}
    mesh = df.Mesh(p1=(0, 0, 0), p2=(200, 2, 3), cell=(1, 1, 1), subregions=subregions)
    system = mm.System(name='test')

    def ms_fun(pos):
        x, y, z = pos
        return x
    system.m = df.Field(mesh, dim=3, value=(0, 0, 1), norm=ms_fun)
    with pytest.raises(ValueError):
        _ = mc.scripts.util.mumax3_regions(system)
