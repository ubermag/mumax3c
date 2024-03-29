# import glob
# import os
# import re
# import shutil

# import discretisedfield as df
# import micromagneticmodel as mm
# import ubermagtable as ut

# import mumax3c as mc


# def oxs_class(term):
#     """Extract the OOMMF ``Oxs_`` class name of an individual term."""
#     mif = getattr(mc.scripts.energy, f"{term.name}_script")(term)
#     return re.search(r"Oxs_([\w_]+)", mif).group(1)


# def schedule_script(func):
#     """Generate OOMMF ``Schedule...`` line for saving an individual value."""
#     if func.__name__ == "energy":
#         return ""  # Datatable with energies is saved by default.
#     elif func.__name__ == "effective_field":
#         if isinstance(func.__self__, mm.Energy):
#             output = "Oxs_RungeKuttaEvolve:evolver:Total field"
#         else:
#             output = f"Oxs_{oxs_class(func.__self__)}::Field"
#     elif func.__name__ == "density":
#         if isinstance(func.__self__, mm.Energy):
#             output = "Oxs_RungeKuttaEvolve:evolver:Total energy density"
#         else:
#             output = f"Oxs_{oxs_class(func.__self__)}::Energy density"
#     else:
#         msg = f"Computing the value of {func} is not supported."
#         raise ValueError(msg)

#     return 'Schedule "{}" archive Step 1\n'.format(output)


def compute(func, system):
    raise NotImplementedError()
    # """Computes a particular value of an energy term or energy container
    # (``energy``, ``density``, or ``effective_field``).

    # Parameters
    # ----------
    # func : callable

    #     A property of an energy term or an energy container.

    # system : micromagneticmodel.System

    #     Micromagnetic system for which the property is calculated.

    # Returns
    # -------
    # numbers.Real, discretisedfield.Field

    #     Resulting value.

    # Examples
    # --------
    # 1. Computing values of energy terms.

    # >>> import micromagneticmodel as mm
    # >>> import oommfc as oc
    # ...
    # >>> system = mm.examples.macrospin()
    # >>> mc.compute(system.energy.zeeman.energy, system)
    # Running OOMMF...
    # -8.8...e-22
    # >>> mc.compute(system.energy.effective_field, system)
    # Running OOMMF...
    # Field(...)
    # >>> mc.compute(system.energy.density, system)
    # Running OOMMF...
    # Field(...)

    # """
    # td = mc.TimeDriver(total_iteration_limit=1)
    # td.drive(
    #     system, t=1e-25, n=1, save=True, overwrite=True, compute=schedule_script(func)
    # )

    # if func.__name__ == "energy":
    #     extension = "*.odt"
    # elif func.__name__ == "effective_field":
    #     extension = "*.ohf"
    # elif func.__name__ == "density":
    #     extension = "*.oef"

    # dirname = os.path.join(system.name, f"compute-{system.drive_number}")
    # output_file = max(
    #     glob.iglob(os.path.join(dirname, extension)), key=os.path.getctime
    # )

    # if func.__name__ == "energy":
    #     table = ut.read(output_file, rename=False)
    #     if isinstance(func.__self__, mm.Energy):
    #         output = table["RungeKuttaEvolve:evolver:Total energy"][0]
    #     else:
    #         output = table[f"{oxs_class(func.__self__)}::Energy"][0]
    # else:
    #     output = df.Field.fromfile(output_file)

    # # Delete "compute" directory after the data is extracted.
    # shutil.rmtree(dirname)

    # # Delete the parent directory if it remains empty after deleting "compute"
    # # directory.
    # if not os.listdir(system.name):
    #     shutil.rmtree(system.name)

    # return output
