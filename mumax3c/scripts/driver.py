import mumax3c as mc
import micromagneticmodel as mm


def driver_script(driver, system, compute=None, **kwargs):
    mx3 = ''
    if isinstance(driver, mc.MinDriver):
        mx3 += f"Msat={system.m.norm.average}\n"

        mx3 += "tableadd(E_total)\n"
        mx3 += "tableadd(E_exch)\n"
        mx3 += "tableadd(E_demag)\n"
        mx3 += "tableadd(E_zeeman)\n"
        mx3 += "tableadd(E_anis)\n"
        mx3 += "tableadd(dt)\n"
        mx3 += "tableadd(maxtorque)\n"


        mx3 += "minimize()\n\n"
        mx3 += "save(m_full)\n"
        mx3 += "tablesave()\n\n"

    if isinstance(driver, mc.TimeDriver):
        # Extract dynamics equation parameters.
        if mm.Precession() in system.dynamics:
            gamma0 = system.dynamics.precession.gamma0
        else:
            gamma0 = 0
        if mm.Damping() in system.dynamics:
            alpha = system.dynamics.damping.alpha
        else:
            alpha = 0

        mx3 += f'alpha = {alpha}\n'
        if not gamma0:
            mx3 += f'gammaLL = {gamma0/mm.consts.mu0}\n'
        else:
            mx3 += f'doprecess = false\n'

        mx3 += f'Msat={system.m.norm.average}\n'

        mx3 += "setsolver(5)\n"
        mx3 += "fixDt = 0.\n\n"

        mx3 += "tableadd(E_total)\n"
        mx3 += "tableadd(E_exch)\n"
        mx3 += "tableadd(E_demag)\n"
        mx3 += "tableadd(E_zeeman)\n"
        mx3 += "tableadd(E_anis)\n"
        mx3 += "tableadd(dt)\n"
        mx3 += "tableadd(maxtorque)\n"

        t, n = kwargs['t'], kwargs['n']

        mx3 += f'for snap_counter:=0; snap_counter<{n};snap_counter++{{\n'
        mx3 += f"    run({t/n})\n"
        mx3 += "    save(m_full)\n"
        mx3 += "    tablesave()\n"
        mx3 += "}"

    return mx3
