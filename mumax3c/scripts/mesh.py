import mumax3c as calculator


def mesh_script(field):
    mx3 = '// Mesh\n'
    if field.mesh.pbc:
        repetitions = [0, 0, 0]
        for direction in field.mesh.pbc:
            # I need to figure the way of setting up the repetitions.
            repetitions[df.util.axesdict(direction)] = 1
        mx3 += 'SetPBC({}, {}, {})\n'.format(*repetitions)
    mx3 +=  'SetGridSize({}, {}, {})\n'.format(*field.mesh.n)
    mx3 += 'SetCellSize({}, {}, {})\n\n'.format(*field.mesh.cell)
    mx3 += calculator.scripts.set_subregions(field)

    return mx3
