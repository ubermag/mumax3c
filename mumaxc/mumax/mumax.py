import os
import sys
import time
import datetime
import logging
import shutil
import mumaxc as mc
import subprocess as sp

log = logging.getLogger(__name__)


class MumaxRunner:
    """Base class for running mumax3.

    Don't use this directly. Use get_mumax_runner() to pick a subclass
    of this class.

    """
    def call(self, argstr, need_stderr=False):
        now = datetime.datetime.now()
        timestamp = '{}/{:02d}/{:02d} {:02d}:{:02d}'.format(now.year,
                                                            now.month,
                                                            now.day,
                                                            now.hour,
                                                            now.minute)
        print('{}: Running mumax3 ({}) ... '.format(timestamp, argstr), end='')

        tic = time.time()
        res = self._call(argstr=argstr, need_stderr=need_stderr)
        self._kill()
        toc = time.time()
        seconds = '({:0.1f} s)'.format(toc - tic)
        print(seconds)

        if res.returncode is not 0:
            if sys.platform != 'win32':
                # Only on Linux and MacOS - on Windows we do not get
                # stderr and stdout.
                stderr = res.stderr.decode('utf-8', 'replace')
                stdout = res.stdout.decode('utf-8', 'replace')
                cmdstr = ' '.join(res.args)
                print('mumax error:')
                print('\tcommand: {}'.format(cmdstr))
                print('\tstdout: {}'.format(stdout))
                print('\tstderr: {}'.format(stderr))
                print('\n')
            raise RuntimeError('Error in mumax run.')

        return res

    def _call(self, argstr, need_stderr=False):
        # This method should be implemented in subclass.
        raise NotImplementedError

    def _kill(self, targets=('all',)):
        # This method should be implemented in subclass.
        raise NotImplementedError
    
    def version(self):
        pass

    def platform(self):
        pass

    
class ExeMumaxRunner(MumaxRunner):
    """Using mumax executable on $PATH.

    """
    def __init__(self, mumax_exe='mumax3'):
        self.mumax_exe = mumax_exe

    def _call(self, argstr, need_stderr=False):
        cmd = [self.mumax_exe, argstr]
        return sp.run(cmd, stdout=sp.PIPE, stderr=sp.PIPE)

    def _kill(self, targets=['all']):
        pass
        #sp.run([self.oommf_exe, "killoommf"] + targets)


class OptirunMumaxRunner(MumaxRunner):
    """Using mumax executable on $PATH.

    """
    def __init__(self, mumax_exe='mumax3'):
        self.mumax_exe = mumax_exe

    def _call(self, argstr, need_stderr=False):
        cmd = ['optirun', self.mumax_exe, argstr]
        return sp.run(cmd, stdout=sp.PIPE, stderr=sp.PIPE)

    def _kill(self, targets=['all']):
        pass
        #sp.run([self.oommf_exe, "killoommf"] + targets)


def get_mumax_runner(use_cache=True, mumax_exe='mumax3'):
    """Find the best available way to run Mumax.

    Returns an MumaxRunner object, or raises EnvironmentError if no suitable
    method is found.

    Parameters
    ----------
    use_cache : bool
      The first call to this function will determine the best way to run OOMMF
      and cache it. Normally, subsequent calls will return the OOMMFRunner
      object from the cache. Setting this parameter to False will cause it to
      check for available methods again.
    envvar : str
      Name of the environment variable containing the path to oommf.tcl
    oommf_exe : str
      The name or path of the executable oommf command
    docker_exe : str
      The name or path of the docker command

    """
    optirun_exe = shutil.which('optirun')
    mumax_exe = shutil.which(mumax_exe)
    if optirun_exe:
        return OptirunMumaxRunner(mumax_exe)
    else:
        if mumax_exe:
            return ExeMumaxRunner(mumax_exe)
        else:
        
            raise EnvironmentError('mumax3 cannot be found.')

def status():
    """Run a macrospin example for 1 ps through oommfc and print the OOMMF
    status.

    """
    pass
    #try:
    #    system = oc.examples.macrospin()
    #    td = oc.TimeDriver()
    #    td.drive(system, t=1e-12, n=1, overwrite=True)
    #    print('OOMMF found and running.')
    #    shutil.rmtree('example-macrospin')
    #    return 0
    #except (EnvironmentError, RuntimeError):
    #    print("Cannot find OOMMF.")
    #    return 1

def overhead():
    """Run a macrospin example for 1 ps through oommfc and directly and
    return the difference in run times.

    Returns
    -------
    overhead : float
      The time difference (overhead) between running OOMMF though
      oommfc and directly

    """
    pass
    # Running OOMMF through oommfc.
    #system = oc.examples.macrospin()
    #td = oc.TimeDriver()
    #oommfc_start = time.time()
    #td.drive(system, t=1e-12, n=1, overwrite=True)
    #oommfc_stop = time.time()
    #oommfc_time = oommfc_stop - oommfc_start

    # Running OOMMF directly.
    #oommf_runner = get_oommf_runner()
    #mifpath = os.path.realpath(os.path.join('example-macrospin', 'drive-0',
    #                                        'example-macrospin.mif'))
    #oommf_start = time.time()
    #oommf_runner.call(mifpath)
    #oommf_stop = time.time()
    #oommf_time = oommf_stop - oommf_start
    #shutil.rmtree('example-macrospin')

    #return oommfc_time - oommf_time
