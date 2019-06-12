import micromagneticmodel as mm


class CubicAnisotropy(mm.CubicAnisotropy):
    @property
    def _script(self):
        mx3 = "// CubicAnisotropy\n"
        mx3 += "Kc1={}\n".format(self.K1)
        mx3 += "anisC1=vector({},{},{})\n".format(*self.u1)
        mx3 += "anisC2=vector({},{},{})\n\n".format(*self.u2)

        return mx3
