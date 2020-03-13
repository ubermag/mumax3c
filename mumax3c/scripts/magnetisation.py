import discretisedfield as df


def region_field(field):
    rf = df.Field(field.mesh, dim=1, value=0)

    norm = field.norm
    max_region_number = 256
    def value_fun(pos):
        tol = 1e-3
        if norm(pos) < tol:
            return max_region_number - 1
        else:
            return 0

    rf.value = value_fun
    return rf


def find_Ms(m):
    tol = 1e-3
    norm = m.norm
    for coord, value in norm:
        if value > tol:
            return value


def magnetisation_script(m):
    m.orientation.write('m0.omf')
    region_field(m.orientation).write('regions.omf')

    mx3 = '// Magnetisation\n'
    mx3 += 'm.LoadFile("m0.omf")\n'
    mx3 += 'regions.LoadFile("regions.omf")\n'
    mx3 += f'Msat = {find_Ms(m)}\n'
    mx3 += 'Msat.setregion(255, 0)\n\n'

    return mx3
