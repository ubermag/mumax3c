import mumax3c as mc
import micromagneticmodel as mm


def driver_script(driver, system, compute=None, **kwargs):
    mif = ''
    if isinstance(driver, mc.MinDriver):
        mx3 = ''

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
        pass

    return mx3
