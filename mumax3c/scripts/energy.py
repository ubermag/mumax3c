import micromagneticmodel as mm
import numpy as np

import mumax3c as mc


def energy_script(system):
    mx3 = ""
    for term in system.energy:
        mx3 += globals()[f"{term.name}_script"](system)

    # Demagnetisation in mumax3 is enabled by default.
    if mm.Demag() not in system.energy:
        mx3 += "enabledemag = false\n\n"

    return mx3


def exchange_script(system):
    mx3 = "// Exchange energy\n"
    mx3 += mc.scripts.set_parameter(
        parameter=system.energy.exchange.A, name="Aex", system=system
    )
    return mx3


def zeeman_script(system):
    # mx3 file takes B, not H.
    H = system.energy.zeeman.H
    if isinstance(H, dict):
        B = dict()
        for key, value in H.items():
            B[key] = np.multiply(value, mm.consts.mu0)
    else:
        B = np.multiply(H, mm.consts.mu0)

    mx3 = "// Zeeman\n"
    mx3 += mc.scripts.set_parameter(parameter=B, name="B_ext", system=system)
    return mx3


# Needs to be tidied up
def uniaxialanisotropy_script(system):
    mx3 = "// UniaxialAnisotropy\n"
    mx3 += f"Ku1 = {system.energy.uniaxialanisotropy.K1}\n"
    # K2 to be added
    mx3 += "anisu = vector({}, {}, {})\n\n".format(*system.energy.uniaxialanisotropy.u)

    return mx3


def demag_script(system):
    mx3 = "// Demag\n"
    mx3 += "enabledemag = true\n\n"
    return mx3


def dmi_script(system):
    mx3 = ""
    if system.energy.dmi.crystalclass.lower() in ["t", "o"]:
        name = "Dbulk"
    elif system.energy.dmi.crystalclass.lower() in ["cnv", "cnv_z"]:
        name = "Dind"
        # In mumax3 D = -D for interfacial DMI
    else:
        msg = (
            f"The {system.energy.dmi.crystalclass} crystal class "
            "is not supported in mumax3."
        )
        raise ValueError(msg)

    # In mumax3 DMI cannot be used without exchange
    # TODO Martin thinks this should show a warning to the user
    if mm.Exchange() not in system.energy:
        mx3 += "Aex = 1e-25\n"
    mx3 += "// DMI\n"
    mx3 += mc.scripts.set_parameter(
        parameter=system.energy.dmi.D, name=name, system=system
    )
    return mx3


def cubicanisotropy_script(term):
    mx3 = "// CubicAnisotropy\n"
    mx3 += f"Kc1 = {term.K1}\n"
    mx3 += "anisC1 = vector({}, {}, {})\n".format(*term.u1)
    mx3 += "anisC2 = vector({}, {}, {})\n\n".format(*term.u2)

    return mx3


def magnetoelastic_script(term):
    B1mx3, B1name = mc.scripts.setup_scalar_parameter(term.B1, "mel_B1")
    B2mx3, B2name = mc.scripts.setup_scalar_parameter(term.B2, "mel_B2")
    ediagmx3, ediagname = mc.scripts.setup_vector_parameter(term.e_diag, "mel_ediag")
    eoffdiagmx3, eoffdiagname = mc.scripts.setup_vector_parameter(
        term.e_offdiag, "mel_eoffdiag"
    )

    mx3 = ""
    mx3 += B1mx3
    mx3 += B2mx3
    mx3 += ediagmx3
    mx3 += eoffdiagmx3
    mx3 += "# MagnetoElastic\n"
    mx3 += "Specify YY_FixedMEL {\n"
    mx3 += f"  B1 {B1name}\n"
    mx3 += f"  B2 {B2name}\n"
    mx3 += f"  e_diag_field {ediagname}\n"
    mx3 += f"  e_offdiag_field {eoffdiagname}\n"
    mx3 += "}\n\n"

    return mx3
