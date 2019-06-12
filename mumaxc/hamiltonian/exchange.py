import micromagneticmodel as mm


class Exchange(mm.Exchange):
    @property
    def _script(self):
        mx3 = "// UniformExchange\n"
        mx3 += "Aex={}\n\n".format(self.A)

        return mx3
