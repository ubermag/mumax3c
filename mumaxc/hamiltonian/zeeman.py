import micromagneticmodel as mm


class Zeeman(mm.Zeeman):
    @property
    def _script(self):
        mx3 = '// Zeeman\n'
        mx3 += 'B_ext=vector({},{},{})\n\n'.format(*self.H)

        return mx3
