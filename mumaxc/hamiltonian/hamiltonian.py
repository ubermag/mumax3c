import micromagneticmodel as mm


class Hamiltonian(mm.Hamiltonian):
    @property
    def _script(self):
        mx3 = ""
        for term in self.terms:
            mx3 += term._script
        return mx3
