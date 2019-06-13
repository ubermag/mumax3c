from .driver import Driver


class MinDriver(Driver):
    def _script(self, system):
        meshname = system.m.mesh.name
        systemname = system.name

        mx3 = f"m.LoadFile(\"{self.omffilename}\")\n"
        mx3 += f"regions.LoadFile(\"{self.omfregionsfilename}\")\n"
        mx3 += f"Msat={self.Ms}\n"
        mx3 += "Msat.setregion(255, 0)\n"
        mx3 += self._defineoutput
        mx3 += "minimize()\n\n"
        mx3 += "save(m_full)\n"
        mx3 += "tablesave()\n\n"
        return mx3

    def _checkargs(self, **kwargs):
        pass
