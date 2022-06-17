import mumax3c as mc


def system_script(system, abspath=True, **kwargs):
    # Mesh and energy scripts.
    mx3 = ""
    mx3 += mc.scripts.mesh_script(system)
    mx3 += mc.scripts.magnetisation_script(system, abspath)
    mx3 += mc.scripts.energy_script(system)

    return mx3
