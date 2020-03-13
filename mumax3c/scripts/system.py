import mumax3c as mc


def system_script(system, **kwargs):
    # Mesh and energy scripts.
    mx3 = ''
    mx3 += mc.scripts.mesh_script(system.m.mesh)
    mx3 += mc.scripts.energy_script(system.energy)
    mx3 += mc.scripts.magnetisation_script(system.m)

    return mx3
