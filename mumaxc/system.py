import micromagneticmodel as mm


class System(mm.System):
    """Micromagnetic system oject.

    Parameters
    ----------
    name : str

    Examples
    --------
    Creating a simple system object.

    >>> import oommfc as oc
    >>> system = oc.System(name="my_system")

    """
    @property
    def _script(self):
        mx3 = "mu0mm:={}\n\n".format(mm.mu0)
        mx3 += self.m.mesh._script
        mx3 += self.hamiltonian._script
        return mx3

    #def total_energy(self):
    #    return self.dt.tail(1)["E"][0]
