import os

import mumax3c as mc


def magnetisation_script(system, abspath):
    system.m.orientation.write("m0.omf")
    m0_path = 'm0.omf'
    if abspath:
        m0_path = os.path.abspath(m0_path)
    mx3 = "// Magnetisation\n"
    mx3 += f'm.LoadFile("{m0_path}")\n'
    mx3 += mc.scripts.mumax3_regions(system, abspath)
    return mx3
