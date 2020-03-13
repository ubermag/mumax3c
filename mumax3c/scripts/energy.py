import sys
import numbers
import numpy as np
import mumax3c as mc
import discretisedfield as df
import micromagneticmodel as mm


def energy_script(container):
    mx3 = ''
    for term in container:
        mx3 += globals()[f'{term.name}_script'](term)

    return mx3


def exchange_script(term):
    if isinstance(term.A, numbers.Real):
        mx3 = '// Exchange energy\n'
        mx3 += f'Aex = {term.A}\n'
        mx3 += '}\n\n'

    elif isinstance(term.A, dict):
        raise NotImplementedError

    elif isinstance(term.A, df.Field):
        raise NotImplementedError

    return mx3


def zeeman_script(term):
    mx3 = '// Zeeman\n'
    Bext = np.multiply(term.H, mm.consts.mu0)
    mx3 += 'B_ext=vector({}, {}, {})\n\n'.format(*Bext)

    return mx3


def demag_script(term):
    mx3 = "// Demag\n"
    mx3 += "enabledemag=true\n\n"

    return mx3


def dmi_script(term):
    mx3 = ''
    if isinstance(term.D, numbers.Real):
        if term.crystalclass in ['t', 'o']:
            mx3 += '// DMI of crystallographic class T(O)\n'
            mx3 += f'Dbulk={term.D}\n\n'
        elif self.crystalclass == 'cnv':
            mx3 = '// DMI of crystallographic class Cnv\n'
            # DMI in mumax3 is negative of the one in micromagneticmodel
            mx3 += f'Dind={-term.D}\n\n'
        else:
            msg = (f'The {self.crystalclass} crystal class '
                   'is not supported in mumax3.')
            raise ValueError(msg)

    elif isinstance(term.D, dict):
        raise NotImplementedError

    elif isinstance(term.D, df.Field):
        raise NotImplementedError

    return mx3


def uniaxialanisotropy_script(term):
    mx3 = "// UniaxialAnisotropy\n"
    mx3 += f"Ku1 = {term.K1}\n"
    #mx3 += "Ku2={}\n".format(self.K2)
    mx3 += "anisu = vector({}, {}, {})\n\n".format(*term.u)

    return mx3


def cubicanisotropy_script(term):
    mx3 = "// CubicAnisotropy\n"
    mx3 += f"Kc1 = {term.K1}\n"
    mx3 += "anisC1 = vector({}, {}, {})\n".format(*self.u1)
    mx3 += "anisC2 = vector({}, {}, {})\n\n".format(*self.u2)

    return mx3


def magnetoelastic_script(term):
    B1mx3, B1name = oc.scripts.setup_scalar_parameter(term.B1, 'mel_B1')
    B2mx3, B2name = oc.scripts.setup_scalar_parameter(term.B2, 'mel_B2')
    ediagmx3, ediagname = oc.scripts.setup_vector_parameter(
        term.e_diag, 'mel_ediag')
    eoffdiagmx3, eoffdiagname = oc.scripts.setup_vector_parameter(
        term.e_offdiag, 'mel_eoffdiag')

    mx3 = ''
    mx3 += B1mx3
    mx3 += B2mx3
    mx3 += ediagmx3
    mx3 += eoffdiagmx3
    mx3 += '# MagnetoElastic\n'
    mx3 += 'Specify YY_FixedMEL {\n'
    mx3 += f'  B1 {B1name}\n'
    mx3 += f'  B2 {B2name}\n'
    mx3 += f'  e_diag_field {ediagname}\n'
    mx3 += f'  e_offdiag_field {eoffdiagname}\n'
    mx3 += '}\n\n'

    return mx3
