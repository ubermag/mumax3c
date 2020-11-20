import abc
import os
import glob
import json
import shutil
import tempfile
import datetime
import contextlib
import numpy as np
import mumax3c as mc
import ubermagtable as ut
import discretisedfield as df
import micromagneticmodel as mm


@contextlib.contextmanager
def _changedir(dirname):
    """Context manager for changing directory.

    """
    cwd = os.getcwd()
    os.chdir(dirname)
    try:
        yield
    finally:
        os.chdir(cwd)


class Driver(mm.Driver):
    @abc.abstractmethod
    def _checkargs(self, **kwargs):
        """Abstract method defined in a derived driver class.

        """
        pass  # pragma: no cover

    def _drive(self, system, basedirname, overwrite=False,
               compute=None, runner=None, **kwargs):
        """Convenience function, which allows to drive in different Python
        contexts.

        """
        # This method is implemented in the derived driver class. It raises
        # exception if any of the arguments are not valid.
        self._checkargs(**kwargs)

        # Generate directory.
        if compute is None:
            subdir = f'drive-{system.drive_number}'
        else:
            subdir = f'compute-{system.drive_number}'

        dirname = os.path.join(basedirname, system.name, subdir)
        # Check whether a directory already exists.
        if os.path.exists(dirname):
            if overwrite:
                mc.delete(system)
            else:
                msg = (f'Directory {dirname} already exists. To overwrite '
                       'it, pass overwrite=True to the drive method.')
                raise FileExistsError(msg)

        # Make a directory inside which mumax3 will be run.
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        # Generate the necessary filenames.
        mx3filename = f'{system.name}.mx3'
        jsonfilename = 'info.json'

        # Change directory to dirname
        with _changedir(dirname):
            # Generate and save mx3 file.
            mx3 = mc.scripts.system_script(system)
            mx3 += mc.scripts.driver_script(self, system, compute=compute,
                                            **kwargs)
            with open(mx3filename, 'w') as mx3file:
                mx3file.write(mx3)

            # Generate and save json info file.
            info = {}
            info['drive_number'] = system.drive_number
            info['date'] = datetime.datetime.now().strftime('%Y-%m-%d')
            info['time'] = datetime.datetime.now().strftime('%H:%M:%S')
            info['driver'] = self.__class__.__name__
            info['args'] = kwargs
            with open(jsonfilename, 'w') as jsonfile:
                jsonfile.write(json.dumps(info))

            # Run mumax3.
            if runner is None:
                runner = mc.mumax3.get_mumax3_runner()
            runner.call(argstr=mx3filename)

            # Update system's m and datatable attributes if the derivation of
            # E, Heff, or energy density was not asked.
            if compute is None:
                # Update system's magnetisation. An example .omf filename:
                # test_sample-Oxs_TimeDriver-Magnetization-01-0000008.omf
                ovffiles = glob.iglob(os.path.join(f'{system.name}.out',
                                                   'm_full*.ovf'))
                lastovffile = sorted(ovffiles)[-1]
                # Read the resulting m
                result_m = df.Field.fromfile(lastovffile)

                # In mumax3 the minimum mesh point in the resulting ovf file is
                # always (0, 0, 0). Because of that, system.m must be changed
                # using a function.
                def result_m_fun(pos):
                    mumax3_coord = np.subtract(pos, system.m.mesh.region.pmin)
                    return result_m(mumax3_coord)
                system.m.value = result_m_fun

                # Update system's datatable.
                system.table = ut.Table.fromfile(os.path.join(f'{system.name}.out',
                                                    f'table.txt'))

        # Increment drive_number independent of whether the files are saved
        # or not.
        if compute is None:
            system.drive_number += 1

    def drive(self, system, save=False, overwrite=False, compute=None,
              runner=None, **kwargs):
        """Drives the system in phase space.

        Takes ``micromagneticmodel.System`` and drives it in the phase space.
        If ``save=True``, the resulting files obtained from the mumax3 run are
        saved in the current directory (in ``system.name`` directory). If
        ``overwrite=True`` is passed, the directory with all previously created
        files (if exists) will be deleted before the system is run. To save a
        specific value during an mumax3 run ``Schedule...`` line can be passed
        using ``compute``. To specify the way mumax3 is run, an
        ``mumax3c.mumax3.mumax3Runner`` can be passed using ``runner``.

        This method accepts any other arguments that could be required by the
        specific driver.

        Parameters
        ----------
        system : micromagneticmodel.System

          System to be driven.

        save : bool

            If ``True`` files created during an mumax3 run will be saved in the
            current directory. Defaults to ``False``.

        overwrite : bool

            If the directory from the previous drive already exists, it will be
            overwritten. Defaults to ``False``.

        compute : str

            ``Schedule...`` mx3 line which can be added to the mumax3 file to
            save additional data. Defaults to ``None``.

        runner : mumax3c.mumax3.mumax3Runner

            mumax3 Runner which is going to be used for running mumax3. If
            ``None``, mumax3 runner will be found automatically. Defaults to
            ``None``.

        Examples
        --------
        1. Drive system using minimisation driver (``MinDriver``).

        >>> import micromagneticmodel as mm
        >>> import discretisedfield as df
        >>> import mumax3c as oc
        ...
        >>> system = mm.System(name='my_cool_system')
        >>> system.energy = mm.Exchange(A=1e-12) + mm.Zeeman(H=(0, 0, 1e6))
        >>> mesh = df.Mesh(p1=(0, 0, 0), p2=(1e-9, 1e-9, 10e-9), n=(1, 1, 10))
        >>> system.m = df.Field(mesh, dim=3, value=(1, 1, 1), norm=1e6)
        ...
        >>> md = mc.MinDriver()
        >>> md.drive(system)
        Running mumax3...

        2. Drive system using time driver (``TimeDriver``).

        >>> system.energy.zeeman.H = (0, 1e6, 0)
        ...
        >>> td = mc.TimeDriver()
        >>> td.drive(system, t=0.1e-9, n=10)
        Running mumax3...

        """
        if save:
            self._drive(system=system, basedirname='', overwrite=overwrite,
                        compute=compute, runner=runner, **kwargs)
        else:
            with tempfile.TemporaryDirectory() as tmpdir:
                self._drive(system=system, basedirname=tmpdir,
                            overwrite=overwrite, compute=compute,
                            runner=runner, **kwargs)
