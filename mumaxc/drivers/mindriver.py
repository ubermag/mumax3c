from .driver import Driver


class MinDriver(Driver):
    def _script(self, system):
        meshname = system.m.mesh.name
        systemname = system.name

        mx3 = f"m.LoadFile(\"{self.omffilename}\")\n\n"
        mx3 += "minimize()\n\n"
        mx3 += "save(m)\n\n"
        return mx3

    def _checkargs(self, **kwargs):
        pass
