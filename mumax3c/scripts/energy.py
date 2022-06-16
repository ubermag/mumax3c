import micromagneticmodel as mm
import numpy as np
import ubermagutil.typesystem as ts

import mumax3c as mc


def energy_script(system):
    mx3 = ""
    for term in system.energy:  # TODO: different terms of same class not allowed
        mx3 += globals()[f"{term.__class__.__name__.lower()}_script"](term, system)

    # Demagnetisation in mumax3 is enabled by default.
    if mm.Demag() not in system.energy:
        mx3 += "enabledemag = false\n\n"

    return mx3


def exchange_script(term, system):
    mx3 = "// Exchange energy\n"
    mx3 += mc.scripts.set_parameter(parameter=term.A, name="Aex", system=system)
    return mx3


def zeeman_script(term, system):
    # mx3 file takes B, not H.
    H = term.H
    if isinstance(H, dict):
        B = dict()
        for key, value in H.items():
            B[key] = np.multiply(value, mm.consts.mu0)
    else:
        B = np.multiply(H, mm.consts.mu0)

    mx3 = "// Zeeman\n"
    mx3 += mc.scripts.set_parameter(parameter=B, name="B_ext", system=system)
    return mx3


def uniaxialanisotropy_script(term, system):
    mx3 = "// UniaxialAnisotropy\n"
    if not isinstance(term.K, ts.descriptors.Parameter):
        mx3 += mc.scripts.set_parameter(parameter=term.K, name="Ku1", system=system)
    else:
        mx3 += mc.scripts.set_parameter(parameter=term.K1, name="Ku1", system=system)
        mx3 += mc.scripts.set_parameter(parameter=term.K2, name="Ku2", system=system)

    mx3 += mc.scripts.set_parameter(parameter=term.u, name="anisU", system=system)
    return mx3


def demag_script(term, system):
    mx3 = "// Demag\n"
    mx3 += "enabledemag = true\n\n"
    return mx3


def dmi_script(term, system):
    if not system.energy.get(type=mm.Exchange):
        raise RuntimeError(
            "In mumax3 DMI cannot be used without exchange. "
            "Solution: define exchange with a negligible A value."
        )
    elif term.crystalclass.lower() in ["t", "o"]:
        param_name = "Dbulk"
        param_val = term.D
    elif term.crystalclass.lower() in ["cnv_z", "cnv"]:
        param_name = "Dind"
        if isinstance(term, dict):
            param_val = {sub_reg: -val for sub_reg, val in term.items()}
        else:
            param_val = -term.D
        # In mumax3 D = -D for interfacial DMI
    else:
        msg = (
            f"The {system.energy.dmi.crystalclass} crystal class "
            "is not supported in mumax3."
        )
        raise ValueError(msg)

    mx3 = "// DMI\n"
    mx3 += mc.scripts.set_parameter(parameter=param_val, name=param_name, system=system)
    return mx3


def cubicanisotropy_script(term, system):
    mx3 = "// CubicAnisotropy\n"
    mx3 += mc.scripts.set_parameter(parameter=term.K, name="Kc1", system=system)
    mx3 += mc.scripts.set_parameter(parameter=term.u1, name="anisC1", system=system)
    mx3 += mc.scripts.set_parameter(parameter=term.u2, name="anisC2", system=system)

    return mx3


# def magnetoelastic_script(term):
#     B1mx3, B1name = mc.scripts.setup_scalar_parameter(term.B1, "mel_B1")
#     B2mx3, B2name = mc.scripts.setup_scalar_parameter(term.B2, "mel_B2")
#     ediagmx3, ediagname = mc.scripts.setup_vector_parameter(term.e_diag, "mel_ediag")
#     eoffdiagmx3, eoffdiagname = mc.scripts.setup_vector_parameter(
#         term.e_offdiag, "mel_eoffdiag"
#     )

#     mx3 = ""
#     mx3 += B1mx3
#     mx3 += B2mx3
#     mx3 += ediagmx3
#     mx3 += eoffdiagmx3
#     mx3 += "# MagnetoElastic\n"
#     mx3 += "Specify YY_FixedMEL {\n"
#     mx3 += f"  B1 {B1name}\n"
#     mx3 += f"  B2 {B2name}\n"
#     mx3 += f"  e_diag_field {ediagname}\n"
#     mx3 += f"  e_offdiag_field {eoffdiagname}\n"
#     mx3 += "}\n\n"

#     return mx3
