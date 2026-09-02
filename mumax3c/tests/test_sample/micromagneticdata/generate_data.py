"""This module can be used to recompute the sample data for micromagneticdata tests.

oommfc supports three types of drives: MinDriver, TimeDriver, HysteresisDriver; this
script creates sample data for each type.
"""

import os
import shutil

import discretisedfield as df
import micromagneticmodel as mm

import mumax3c as mc


def clean(system_name):
    """Remove any previous simulation directories."""
    if os.path.exists(system_name):
        print(">>> Removing old test samples")
        shutil.rmtree(system_name)


def rectangle(mode):
    """Simple rectangular ferromagnetic sample in external magnetic field."""
    print(">>> Running ferromagnetic rectangular cuboid")
    p1 = (-50e-9, -25e-9, 0)
    p2 = (50e-9, 25e-9, 20e-9)
    cell = (5e-9, 5e-9, 5e-9)

    region = df.Region(p1=p1, p2=p2)
    # use the region also as subregion: discretisedfield will create the additional
    # subregions json file and we can detect misalignment (translation) of the
    # region from the calculators (e.g. Mumax3 always defines pmin at the origin)
    mesh = df.Mesh(region=region, cell=cell, subregions={"total": region})

    Ms = 8e5
    A = 1.3e-11
    H = (1e6, 0.0, 2e5)
    alpha = 0.02

    system = mm.System(name="rectangle")
    system.energy = mm.Exchange(A=A) + mm.Zeeman(H=H)
    system.dynamics = mm.Precession(gamma0=mm.consts.gamma0) + mm.Damping(alpha=alpha)
    system.m = df.Field(mesh, nvdim=3, value=(0.0, 0.25, 0.1), norm=Ms)

    if mode == "time_drive":
        td = mc.TimeDriver()
        td.drive(system, t=25e-12, n=25)
    elif mode == "min_drive":
        md = mc.MinDriver()
        md.drive(system)
    elif mode == "relax_driver":
        rd = mc.RelaxDriver()
        rd.drive(system, output_step=True)
    else:
        raise NotImplementedError(mode)


if __name__ == "__main__":
    clean("rectangle")
    rectangle("min_drive")
    rectangle("relax_driver")
    rectangle("time_drive")
