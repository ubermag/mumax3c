import discretisedfield as df

import mumax3c as calculator


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
