import mumax3c as mc


def magnetisation_script(system):
    system.m.orientation.write("m0.omf")
    mx3 = "// Magnetisation\n"
    mx3 += 'm.LoadFile("m0.omf")\n'
    mx3 += mc.scripts.mumax3_regions(system)
    return mx3
