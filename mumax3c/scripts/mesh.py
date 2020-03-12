import mumax3c as mc


def mesh_script(mesh):
    mx3 = '// Mesh'
    if mesh.pbc:
        repetitions = [0, 0, 0]
        for direction in mesh.pbc:
            # I need to figure the way of setting up the repetitions.
            repetitions[df.util.axesdict(direction)] = 1
        mx3 += 'SetPBC({}, {}, {})\n'.format(*repetitions)
    mx3 +=  'SetGridSize({}, {}, {})\n'.format(*mesh.n)
    mx3 += 'SetCellSize({}, {}, {})\n\n'.format(*mesh.cell)

    # Defining regions have to be added here.

    return mx3
