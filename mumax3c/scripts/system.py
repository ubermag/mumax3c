import mumax3c as mc


def system_script(system, **kwargs):
    # Mesh and energy scripts.
    mx3 += mc.scripts.mesh_script(system.m.mesh)
    mx3 += mc.scripts.energy_script(system.energy)

    # Magnetisation script.
    m0mif, _, _ = oc.scripts.setup_m0(system.m, 'm0')
    mif += m0mif

    return mif
