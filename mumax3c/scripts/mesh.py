# import mumax3c as mc


def mesh_script(system):
    mx3 = "// Mesh\n"
    if any(i in system.m.mesh.bc for i in "xyz"):  # are there PBC?
        repetitions = [0, 0, 0]  # should be generalised in the future
        for direction in system.m.mesh.bc:
            # Need to figure out the way of setting up the repetitions.
            repetitions[system.m.mesh.region._dim2index(direction)] = 1
        mx3 += "SetPBC({}, {}, {})\n".format(*repetitions)
    mx3 += "SetGridSize({}, {}, {})\n".format(*system.m.mesh.n)
    mx3 += "SetCellSize({}, {}, {})\n\n".format(*system.m.mesh.cell)
    # mx3 += mc.scripts.set_subregions(system)

    return mx3
