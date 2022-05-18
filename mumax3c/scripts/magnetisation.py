import discretisedfield as df
import numpy as np


def find_Ms(m):
    tol = 1e-3
    norm = m.norm
    for coord, value in norm:
        if value > tol:
            return value


def magnetisation_script(system):
    system.m.orientation.write("m0.omf")

    mx3 = "// Magnetisation\n"
    mx3 += 'm.LoadFile("m0.omf")\n'
    mx3 += f"Msat = {find_Ms(system.m)}\n"
    mx3 += "Msat.setregion(255, 0)\n\n"

    return mx3


def magnetisation_subregions(system):
    system.m.orientation.write("m0.omf")
    mx3 = 'regions.LoadFile("subregions.omf")\n'
    mx3 += "// Magnetisation\n"
    mx3 += 'm.LoadFile("m0.omf")\n'

    test_field = system.m.norm.array
    sub_region_values = np.empty_like(test_field)
    uniq_arr = np.unique(test_field)
    if uniq_arr.size > 255:
        raise ValueError("Cannot have more than 255 seperate Ms.")

    for i, val in enumerate(uniq_arr):
        sub_region_values[test_field == val] = i
        mx3 += f"Msat.setregion({i}, {val})\n\n"

    rf = df.Field(system.m.mesh, dim=1, value=sub_region_values)
    rf.write("subregions.omf")

    return mx3
