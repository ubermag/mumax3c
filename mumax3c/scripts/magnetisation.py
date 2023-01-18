import pathlib

import mumax3c as mc


def magnetisation_script(system, ovf_format="bin4", abspath=True):
    system.m.orientation.to_file("m0.omf", representation=ovf_format)
    m0_path = pathlib.Path("m0.omf")
    if abspath:
        m0_path = m0_path.absolute().as_posix()  # '/' as path separator required
    mx3 = "// Magnetisation\n"
    mx3 += f'm.LoadFile("{m0_path}")\n'
    mx3 += mc.scripts.mumax3_regions(system, ovf_format=ovf_format, abspath=abspath)
    return mx3
