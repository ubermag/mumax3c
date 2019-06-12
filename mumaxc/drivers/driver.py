import os
import glob
import json
import shutil
import datetime
import mumaxc as mc
import oommfodt as oo
import discretisedfield as df
import micromagneticmodel as mm


class Driver(mm.Driver):
    def drive(self, system, overwrite=False, **kwargs):
        # This method is implemented in the derived class (TimeDriver,
        # MinDriver,...).
        self._checkargs(**kwargs)

        # Generate the necessary filenames.
        self.dirname = os.path.join(system.name,
                                    'drive-{}'.format(system.drive_number))
        self.omffilename = os.path.join(self.dirname, 'm0.omf')
        self.mx3filename = os.path.join(self.dirname,
                                        '{}.mx3'.format(system.name))
        self.jsonfilename = os.path.join(self.dirname, 'info.json')

        # Check whether a directory with the same name as system.name
        # already exists. If it does, warn the user and tell him that
        # he should pass overwrite=True to the drive method.
        self._checkdir(system, overwrite=overwrite)

        # Make a directory inside which OOMMF will be run.
        self._makedir()

        # Generate and save mx3 file.
        self._makemx3(system, **kwargs)

        # Save system's initial magnetisation m0.omf file.
        self._makeomf(system)

        # Create json info file.
        self._makejson(system, **kwargs)

        # Run OOMMF.
        self._runmumax()

        # Update system's m and dt attributes if the derivation of E,
        # Heff, or energy density was not asked.
        if 'derive' not in kwargs:
            self._update_m(system)
            self._update_dt(system)

        # Increase the system's drive_number counter.
        system.drive_number += 1

    def _checkargs(self, **kwargs):
        raise NotImplementedError('This method is defined in a derived class')

    def _checkdir(self, system, overwrite=False):
        if os.path.exists(self.dirname):
            if not overwrite:
                msg = ('Directory with name={} already exists. If you want '
                       'to overwrite it, pass overwrite=True to the drive '
                       'method. Otherwise, change the name of the system '
                       'or delete the directory by running '
                       'system.delete().'.format(self.dirname))
                raise FileExistsError(msg)
            else:
                shutil.rmtree(system.name)

    def _makedir(self):
        if not os.path.exists(self.dirname):
            os.makedirs(self.dirname)

    def _makemx3(self, system, **kwargs):
        mx3 = system._script
        mx3 += self._script(system, **kwargs)

        with open(self.mx3filename, 'w') as mx3file:
            mx3file.write(mx3)

    def _makeomf(self, system):
        system.m.write(self.omffilename)

    def _makejson(self, system, **kwargs):
        info = {}
        info['drive_number'] = system.drive_number
        info['date'] = datetime.datetime.now().strftime('%Y-%m-%d')
        info['time'] = datetime.datetime.now().strftime('%H:%M:%S')
        info['driver'] = self.__class__.__name__
        info['args'] = kwargs

        with open(self.jsonfilename, 'w') as jsonfile:
            jsonfile.write(json.dumps(info))

    def _runmumax(self):
        mumax = mc.mumax.get_mumax_runner()
        mumax.call(argstr=self.mx3filename)

    def _update_m(self, system):
        # An example .omf filename is:
        # test_sample-Oxs_TimeDriver-Magnetization-01-0000008.omf
        ovffiles = glob.iglob(os.path.join(self.dirname, f'{system.name}.out',
                                           'm*.ovf'))
        lastovffile = list(sorted(ovffiles))[-1]
        m_field = df.read(lastovffile)

        # This line exists because the mesh generated in df.read
        # method comes from the discrtisedfield module where the
        # _script method is not implemented.
        m_field.mesh = system.m.mesh

        system.m = m_field

    def _update_dt(self, system):
        pass
        #system.dt = oo.read(os.path.join(self.dirname,
        #                                 f'{system.name}.odt'))