import discretisedfield as df
import micromagneticmodel as mm
import numpy as np

import mumax3c as mc


def driver_script(driver, system, compute=None, **kwargs):
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
        alpha = system.dynamics.damping.alpha
        mx3 += f"alpha = {alpha}\n"

        for attr, value in driver:
            if attr != "evolver":
                mx3 += f"{attr} = {value}\n"

        mx3 += "relax()\n\n"
        mx3 += "save(m_full)\n"
        mx3 += "tablesave()\n\n"

    if isinstance(driver, mc.TimeDriver):
        # Extract dynamics equation parameters.
        if system.dynamics.get(type=mm.Precession):
            gamma0 = system.dynamics.precession.gamma0
        else:
            gamma0 = 0
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

        zh_li_terms = system.dynamics.get(type=mm.ZhangLi)
        if zh_li_terms:
            u = (
                zh_li_terms[0].u
                if isinstance(zh_li_terms[0].u, df.Field)
                else df.Field(
                    mesh=system.m.mesh, dim=3, value=(1, 0, 0), norm=zh_li_terms[0].u
                )
            )

            j = np.multiply(u * (mm.consts.e / mm.consts.muB), system.m.norm)
            j.write("j.ovf")
            mx3 += f"Xi = {system.dynamics.get(type=mm.ZhangLi)[0].beta}"
            mx3 += "Pol = 1"  # Current polarization is 1.
            mx3 += 'J.add("j.ovf")'

        mx3 += "setsolver(5)\n"
        mx3 += "fixDt = 0\n\n"

        t, n = kwargs["t"], kwargs["n"]

        mx3 += f"for snap_counter:=0; snap_counter<{n}; snap_counter++{{\n"
        mx3 += f"    run({t/n})\n"
        mx3 += "    save(m_full)\n"
        mx3 += "    tablesave()\n"
        mx3 += "}"

    return mx3
