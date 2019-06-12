import micromagneticmodel as mm


class UniaxialAnisotropy(mm.UniaxialAnisotropy):
    @property
    def _script(self):
        mx3 = "// UniaxialAnisotropy\n"
        mx3 += "Ku1={}\n".format(self.K1)
        mx3 += "Ku2={}\n".format(self.K2)
        mx3 += "anisu=vector({},{},{})\n\n".format(*self.u)

        return mx3
