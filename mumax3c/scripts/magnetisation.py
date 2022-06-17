import pathlib

import mumax3c as mc


def magnetisation_script(system, abspath=True):
    system.m.orientation.write("m0.omf")
    m0_path = pathlib.Path("m0.omf")
    if abspath:
        m0_path = m0_path.absolute().as_posix()  # '/' as path separator required
    mx3 = "// Magnetisation\n"
    mx3 += f'm.LoadFile("{m0_path}")\n'
    mx3 += mc.scripts.mumax3_regions(system, abspath)
    return mx3
