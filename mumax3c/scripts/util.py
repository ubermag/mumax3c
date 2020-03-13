import numbers
import numpy as np
import discretisedfield as df


def set_subregions(field):
    # Region field. Where the value is 255, Ms=0. In other regions Ms is const.
    # Other regions are annotated with 0, 1, 2,... according to the subregions
    # in field.mesh.
    rf = df.Field(field.mesh, dim=1, value=0)

    subregion_names = field.mesh.subregions.keys()
    dictionary = dict(zip(subregion_names, range(len(subregion_names))))

    norm = field.norm
    max_region_number = 256
    def value_fun(pos):
        tol = 1e-3
        if norm(pos) < tol:
            # At this point Ms=0.
            return max_region_number - 1
        else:
            for name, region in field.mesh.subregions.items():
                if pos in region:
                    return dictionary[name]
            else:
                msg = f'Point {pos} does not belong to any region.'

    rf.value = value_fun
    rf.write('regions.omf')

    return 'regions.LoadFile("regions.omf")\n'


def set_value(name, value, system):
    subregion_names = system.m.mesh.subregions.keys()
    dictionary = dict(zip(subregion_names, range(len(subregion_names))))

    mx3 = ''
    if isinstance(value, numbers.Real):
        mx3 += f'{name} = {value}\n'

    elif isinstance(value, (list, tuple, np.ndarray)):
        mx3 += '{} = vector({}, {}, {})\n'.format(name, value[0], value[1], value[2])

    elif isinstance(value, dict):
        for key, val in value.items():
            if isinstance(val, numbers.Real):
                mx3 += f'{name}.setregion({dictionary[key]}, {val})\n'

            elif isinstance(val, (list, tuple, np.ndarray)):
                mx3 += (f'{name}.setregion({dictionary[key]}, '
                        f'vector({val[0]}, {val[1]}, {val[2]}))\n')

    else:
        msg = f'Cannot use {type(value)} to set parameter.'
        raise TypeError(msg)

    return mx3
