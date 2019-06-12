import micromagneticmodel as mm


class Demag(mm.Demag):
    @property
    def _script(self):
        mx3 = "// Demag\n"
        mx3 += "enabledemag=true\n\n"

        return mx3
