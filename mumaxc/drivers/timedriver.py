from .driver import Driver

class TimeDriver(Driver):
    def _script(self, system, **kwargs):
        try:
            alpha = system.dynamics.damping.alpha
        except AttributeError:
            alpha = 0
        try:
            gamma = system.dynamics.precession.gamma
        except AttributeError:
            gamma = 0
        mx3 = f"alpha={alpha}\n"
        mx3 += f"gammaLL={gamma}/mu0\n"
        if gamma == 0:
            mx3 += f"doprecess = false\n"
        else:
            mx3 += f"doprecess = true\n"

        mx3 += f"m.LoadFile(\"{self.omffilename}\")\n"
        mx3 += f"regions.LoadFile(\"{self.omfregionsfilename}\")\n"
        mx3 += f"Msat={self.Ms}\n"
        mx3 += "Msat.setregion(255, 0)\n"
        mx3 += "setsolver(5)\n"
        mx3 += "fixdt=0.\n\n"
        mx3 += self._defineoutput
        mx3 += "for snap_counter:=0;snap_counter<{};snap_counter++{{\n".format(kwargs["n"])
        mx3 += "    run({}/{})\n".format(kwargs["t"], kwargs["n"])
        mx3 += "    save(m_full)\n"
        mx3 += "    tablesave()\n"
        mx3 += "}"

        return mx3

    def _checkargs(self, **kwargs):
        if "derive" in kwargs:
            pass
        else:
            if kwargs["t"] <= 0:
                raise ValueError("Expected t > 0.")
            if kwargs["n"] <= 0 or not isinstance(kwargs["n"], int):
                raise ValueError("Expected n > 0.")
