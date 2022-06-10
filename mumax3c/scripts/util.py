import numbers

import discretisedfield as df
import numpy as np


def identify_subregions(system):
    subregion_values = np.zeros_like(system.m.norm.array)
    if system.m.mesh.subregions:
        names = system.m.mesh.subregions.keys()
        subregions_dict = dict(zip(names, range(1, len(names) + 1)))
        # Reversed to get same functionality as oommf if subregions overlap
        for key in reversed(subregions_dict):
            # Extract the subregion
            subfield = system.m[key]
            # Add subregion values into region values
            slices = system.m.mesh.region2slices(subfield.mesh.region)
            subregion_values[slices] = subregions_dict[key]
    else:
        subregions_dict = dict()

    subregions_dict["ee"] = 0  # Everything else has values of 0
    return subregion_values, subregions_dict


def mumax3_regions(system):
    # Region refers to mumax3
    # subregion refers to ubermag
    system.m.orientation.write("m0.omf")
    mx3 = "// Magnetisation\n"
    mx3 += 'm.LoadFile("m0.omf")\n'
    # Array of all subregions and left over and dict relating names to subregion index
    subregion_arr, subregions_dict = identify_subregions(system)
    region_relators = {
        key: [] for key in subregions_dict
    }  # relates subregion to mumax3 region
    ms_arr = system.m.norm.array
    region_values = np.empty_like(ms_arr)

    next_uni_index = 0  # next unique index
    for key in region_relators:
        # Select subregion
        sub_region_val = subregions_dict[key]
        bool_arr = subregion_arr == sub_region_val

        # Find unique Ms within subregion
        uniq_arr = np.unique(ms_arr[bool_arr])
        if next_uni_index + uniq_arr.size > 255:
            msg = "mumax3 does not allow for than 255 seperate regions to be set. "
            msg += "The number of mumax3 regions is determined by the number of unique "
            msg += (
                "combinations of `discretisedfield` subregions and saturation"
                " magnetisation."
            )
            raise ValueError(msg)

        # Index all unique Ms within region
        for i, val in enumerate(uniq_arr, start=next_uni_index):
            region_values[(ms_arr == val) & bool_arr] = i
            region_relators[key].append(i)
            mx3 += f"Msat.setregion({i}, {val})\n"

        next_uni_index = i + 1  # next unique index

    m3_regions = df.Field(system.m.mesh, dim=1, value=region_values)
    system.region_relators = region_relators  # Add dict to relate subregions to regions
    m3_regions.write("subregions.omf")

    mx3 += "\n"
    mx3 += 'regions.LoadFile("subregions.omf")\n\n'
    return mx3


def set_parameter(parameter, name, system):
    mx3 = ""
    # Spatially constant scalar parameter.
    if isinstance(parameter, numbers.Real):
        mx3 += f"{name} = {parameter}\n"

    # Spatially constant vector parameter.
    elif isinstance(parameter, (list, tuple, np.ndarray)):
        mx3 += "{} = vector({}, {}, {})\n".format(name, *parameter)

    # Spatially varying parameter defined using subregions.
    elif isinstance(parameter, dict):
        names = system.m.mesh.subregions.keys()
        subregions_dict = dict(zip(names, range(len(names))))

        for key, value in parameter.items():
            if isinstance(value, numbers.Real):
                mx3 += f"{name}.setregion({subregions_dict[key]}, {value})\n"

            elif isinstance(value, (list, tuple, np.ndarray)):
                mx3 += (
                    f"{name}.setregion({subregions_dict[key]}, "
                    "vector({}, {}, {}))\n".format(*value)
                )

    else:
        # In mumax3, the parameter cannot be set using Field.
        msg = f"Cannot use {type(parameter)} to set parameter."
        raise TypeError(msg)

    return mx3
