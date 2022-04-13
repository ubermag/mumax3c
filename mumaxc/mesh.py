import textwrap

import discretisedfield as df


class Mesh(df.Mesh):
    @property
    def _script(self):
        mx3 = "SetGridSize({}, {}, {})\n".format(self.n[0], self.n[1], self.n[2])
        mx3 += "SetCellSize({}, {}, {})\n\n".format(
            self.cell[0], self.cell[1], self.cell[2]
        )

        return mx3
