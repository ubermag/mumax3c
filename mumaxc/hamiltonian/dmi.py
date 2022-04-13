import sys

import micromagneticmodel as mm


class DMI(mm.DMI):
    @property
    def _script(self):

        if self.crystalclass in ["t", "o"]:
            mx3 = "// DMI of crystallographic class T(O)\n"
            mx3 += "Dbulk={}\n\n".format(self.D)
        elif self.crystalclass == "cnv":
            D = (
                -self.D
            )  # DMI in mumax3 is the opposite of the one in micromagneticmodel
            mx3 = "// DMI of crystallographic class Cnv\n"
            mx3 += "Dind={}\n\n".format(D)
        else:
            raise ValueError(
                "The {} crystal class is not supported                     in mumax3."
                .format(self.crystalclass)
            )

        return mx3
