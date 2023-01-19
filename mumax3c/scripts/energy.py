import discretisedfield as df
import micromagneticmodel as mm
import numpy as np
import ubermagutil.typesystem as ts

import mumax3c as mc


def energy_script(system, ovf_format, abspath):
    mx3 = ""
    for term in system.energy:
        if isinstance(term, mm.Zeeman):  # Handled separately
            continue
        elif len(system.energy.get(type=type(term))) > 1:
            raise RuntimeError(
                "Mumax3 does not allow more than one energy term of the same class "
                "except for the Zeeman term."
            )
        else:
            mx3 += globals()[f"{term.__class__.__name__.lower()}_script"](
                term, system, ovf_format, abspath
            )

    if zeeman_terms := system.energy.get(type=mm.Zeeman):
        for term in zeeman_terms:
            if isinstance(term.H, (tuple, list, dict, np.ndarray)):
                H_field = df.Field(mesh=system.m.mesh, nvdim=3, value=term.H)
                mx3 += zeeman_script(mm.Zeeman(H=H_field), system, ovf_format, abspath)
            else:
                mx3 += zeeman_script(term, system, ovf_format, abspath)

        mx3 += "tableadd(E_Zeeman)\n"

    # Demagnetisation in mumax3 is enabled by default.
    if mm.Demag() not in system.energy:
        mx3 += "enabledemag = false\n\n"

    return mx3


def exchange_script(term, system, ovf_format, abspath):
    mx3 = "// Exchange energy\n"
    mx3 += mc.scripts.set_parameter(
        parameter=term.A,
        name="Aex",
        system=system,
        ovf_format=ovf_format,
        abspath=abspath,
    )
    mx3 += "tableadd(E_exch)\n"
    return mx3


def zeeman_script(term, system, ovf_format, abspath):
    # mx3 file takes B, not H.
    H = term.H
    if isinstance(H, dict):
        B = dict()
        for key, value in H.items():
            B[key] = np.multiply(value, mm.consts.mu0)
    else:
        B = np.multiply(H, mm.consts.mu0)

    mx3 = "// Zeeman\n"
    mx3 += mc.scripts.set_parameter(
        parameter=B, name="B_ext", system=system, ovf_format=ovf_format, abspath=abspath
    )
    return mx3


def uniaxialanisotropy_script(term, system, ovf_format, abspath):
    mx3 = "// UniaxialAnisotropy\n"
    if not isinstance(term.K, ts.descriptors.Parameter):
        mx3 += mc.scripts.set_parameter(
            parameter=term.K,
            name="Ku1",
            system=system,
            ovf_format=ovf_format,
            abspath=abspath,
        )
    else:
        mx3 += mc.scripts.set_parameter(
            parameter=term.K1,
            name="Ku1",
            system=system,
            ovf_format=ovf_format,
            abspath=abspath,
        )
        mx3 += mc.scripts.set_parameter(
            parameter=term.K2,
            name="Ku2",
            system=system,
            ovf_format=ovf_format,
            abspath=abspath,
        )

    mx3 += mc.scripts.set_parameter(
        parameter=term.u,
        name="anisU",
        system=system,
        ovf_format=ovf_format,
        abspath=abspath,
    )
    mx3 += "tableadd(E_anis)\n"
    return mx3


def demag_script(term, system, ovf_format, abspath):
    # all energy terms must have the same signature
    mx3 = "// Demag\n"
    mx3 += "enabledemag = true\n"
    mx3 += "tableadd(E_demag)\n"
    return mx3


def dmi_script(term, system, ovf_format, abspath):
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
        if isinstance(term.D, dict):
            param_val = {sub_reg: -val for sub_reg, val in term.D.items()}
        else:
            param_val = -term.D
        # In mumax3 D = -D for interfacial DMI
    else:
        raise ValueError(
            f"The {term.crystalclass} crystal class is not supported in mumax3."
        )

    mx3 = "// DMI\n"
    mx3 += mc.scripts.set_parameter(
        parameter=param_val,
        name=param_name,
        system=system,
        ovf_format=ovf_format,
        abspath=abspath,
    )
    # In mumax DMI energy is combined with exchange energy
    return mx3


def cubicanisotropy_script(term, system, ovf_format, abspath):
    mx3 = "// CubicAnisotropy\n"
    mx3 += mc.scripts.set_parameter(
        parameter=term.K,
        name="Kc1",
        system=system,
        ovf_format=ovf_format,
        abspath=abspath,
    )
    mx3 += mc.scripts.set_parameter(
        parameter=term.u1,
        name="anisC1",
        system=system,
        ovf_format=ovf_format,
        abspath=abspath,
    )
    mx3 += mc.scripts.set_parameter(
        parameter=term.u2,
        name="anisC2",
        system=system,
        ovf_format=ovf_format,
        abspath=abspath,
    )
    mx3 += "tableadd(E_anis)\n"

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
