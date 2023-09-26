import discretisedfield as df
import micromagneticmodel as mm
import numpy as np

import mumax3c as mc


def driver_script(driver, system, compute=None, ovf_format="bin4", **kwargs):
    mx3 = "tableadd(E_total)\n"
    mx3 += "tableadd(dt)\n"
    mx3 += "tableadd(maxtorque)\n"
    if isinstance(driver, mc.MinDriver):
        for attr, value in driver:
            if attr != "evolver":
                mx3 += f"{attr} = {value}\n"

        mx3 += "minimize()\n\n"
        mx3 += "save(m_full)\n"
        mx3 += "tablesave()\n\n"

    if isinstance(driver, mc.RelaxDriver):
        if not system.dynamics.get(type=mm.Damping):
            raise ValueError("A damping term is needed.")
        alpha = system.dynamics.get(type=mm.Damping)[0].alpha
        mx3 += f"alpha = {alpha}\n"

        for attr, value in driver:
            if attr != "evolver":
                mx3 += f"{attr} = {value}\n"

        mx3 += "relax()\n\n"
        mx3 += "save(m_full)\n"
        mx3 += "tablesave()\n\n"

    if isinstance(driver, mc.TimeDriver):
        # Extract dynamics equation parameters.
        gamma0 = (
            precession[0].gamma0
            if (precession := system.dynamics.get(type=mm.Precession))
            else 0
        )
        if system.dynamics.get(type=mm.Damping):
            alpha = system.dynamics.damping.alpha
        else:
            alpha = 0

        mx3 += f"alpha = {alpha}\n"
        if not gamma0:
            mx3 += "doprecess = false\n"
        else:
            mx3 += f"gammaLL = {gamma0/mm.consts.mu0}\n"
            mx3 += "doprecess = true\n"

        if system.dynamics.get(type=mm.ZhangLi):
            (zh_li_term,) = system.dynamics.get(type=mm.ZhangLi)
            u = (
                zh_li_term.u
                if isinstance(zh_li_term.u, df.Field)
                else df.Field(
                    mesh=system.m.mesh,
                    nvdim=3,
                    value=(1.0, 0.0, 0.0),
                    norm=zh_li_term.u,
                )
            )

            mu_B = mm.consts.e * mm.consts.hbar / (2.0 * mm.consts.me)

            j = -np.multiply(
                u * 2 * (1 + zh_li_term.beta**2) * mm.consts.e / (mm.consts.g * mu_B),
                system.m.norm,
            )
            j.to_file("j.ovf", representation=ovf_format)
            mx3 += f"Xi = {zh_li_term.beta}\n"
            mx3 += "Pol = 1\n"  # Current polarization is 1.
            mx3 += 'J.add(LoadFile("j.ovf"), 1)\n'  # 1 means constant in time.

        mx3 += "setsolver(5)\n"
        mx3 += "fixDt = 0\n\n"

        t, n = kwargs["t"], kwargs["n"]

        mx3 += f"for snap_counter:=0; snap_counter<{n}; snap_counter++{{\n"
        mx3 += f"    run({t/n})\n"
        mx3 += "    save(m_full)\n"
        mx3 += "    tablesave()\n"
        mx3 += "}"

    return mx3
