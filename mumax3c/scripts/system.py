import mumax3c as mc


def system_script(system, ovf_format, abspath=True, **kwargs):
    if ovf_format in ["bin4", "bin8"]:
        ovf_format = "bin4"  # mumax3 uses single precision
        output_format = "OVF2_BINARY"
    elif ovf_format == "txt":
        output_format = "OVF2_TEXT"
    else:
        raise ValueError(f"Invalid {ovf_format=}.")

    mx3 = ""
    # Output options
    mx3 += f"OutputFormat = {output_format}\n\n"
    # Mesh and energy scripts.
    mx3 += mc.scripts.mesh_script(system)
    mx3 += mc.scripts.magnetisation_script(
        system, ovf_format=ovf_format, abspath=abspath
    )
    mx3 += mc.scripts.energy_script(system, ovf_format=ovf_format, abspath=abspath)

    return mx3
