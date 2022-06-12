import numbers

import discretisedfield as df
import numpy as np


def _identify_subregions(system):
    subregion_values = np.full(system.m.norm.array.shape, 255)
    if system.m.mesh.subregions:
        names = system.m.mesh.subregions.keys()
        subregions_dict = dict(zip(names, range(len(names))))
        # Reversed to get same functionality as oommf if subregions overlap
        for key in reversed(subregions_dict):
            # Extract the subregion
            subfield = system.m[key]
            # Add subregion values into region values
            slices = system.m.mesh.region2slices(subfield.mesh.region)
            subregion_values[slices] = subregions_dict[key]
    else:
        subregions_dict = dict(no_sub=255)

    #  subregions_dict["ee"] = 0  # Everything else has values of 0
    return subregion_values, subregions_dict


def mumax3_regions(system):
    # Region refers to mumax3
    # subregion refers to ubermag
    system.m.orientation.write("m0.omf")  # TODO: can be moved to drive script.
    mx3 = "// Magnetisation\n"  #
    mx3 += 'm.LoadFile("m0.omf")\n'  #

    ms_arr = system.m.norm.array
    if any(np.isnan(np.unique(ms_arr))):  # Not sure about this.
        raise ValueError("Ms values cannot be nan.")

    if 0.0 in np.unique(ms_arr):
        mx3 += "Msat.setRegion(255, 0.0)\n"  # Set Msat for region 255 to 0

    region_relators = dict()  # relates subregion to mumax3 region
    next_uni_index = 0  # next unique index
    # Array of all subregions and left over and dict relating names to subregion index
    subregion_values, subregions_dict = _identify_subregions(system)
    region_values = subregion_values

    for sub_reg, sub_reg_val in subregions_dict.items():
        # Select subregion
        bool_arr = subregion_values == sub_reg_val

        # Find unique Ms within subregion
        uniq_ms = np.unique(ms_arr[bool_arr])
        plus_regions = uniq_ms.size if 0.0 not in uniq_ms else uniq_ms.size - 1
        if next_uni_index + plus_regions > 255:
            msg = "mumax3 does not allow for than 255 seperate regions to be set. "
            msg += "The number of mumax3 regions is determined by the number of unique "
            msg += (
                "combinations of `discretisedfield` subregions and saturation"
                " magnetisation."
            )
            raise ValueError(msg)

        # Index all unique Ms != 0.0 within region
        for ms in uniq_ms:
            if ms == 0.0:
                mx3_reg_no = 255  # All 0.0 Ms values will pertain to region 255
            else:
                mx3_reg_no = next_uni_index
                next_uni_index += 1
                mx3 += f"Msat.setregion({mx3_reg_no}, {ms})\n"
                if sub_reg in region_relators:
                    region_relators[sub_reg].append(mx3_reg_no)
                else:
                    region_relators[sub_reg] = [mx3_reg_no]

            region_values[(ms_arr == ms) & bool_arr] = mx3_reg_no

    mx3_regions = df.Field(system.m.mesh, dim=1, value=region_values)
    system.region_relators = region_relators  # Add dict to relate subregions to regions
    mx3_regions.write("subregions.omf")

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
        for key, value in parameter.items():
            # TODO: what if the key is r1:r2?
            for region in system.region_relators[key]:
                if isinstance(value, numbers.Real):
                    mx3 += f"{name}.setregion({region}, {value})\n"
                elif isinstance(value, (list, tuple, np.ndarray)):
                    mx3 += (
                        f"{name}.setregion({region}, "
                        "vector({}, {}, {}))\n".format(*value)
                    )

    else:
        # In mumax3, the parameter cannot be set using Field.
        msg = f"Cannot use {type(parameter)} to set parameter."
        raise TypeError(msg)

    return mx3
