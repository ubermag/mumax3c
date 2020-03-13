import os
import abc
import sys
import time
import datetime
import logging
import shutil
import mumax3c as mc
import subprocess as sp
import ubermagutil as uu
import micromagneticmodel as mm

log = logging.getLogger(__name__)
_cached_mumax3_runner = None


class Mumax3Runner(metaclass=abc.ABCMeta):
    """Abstract class for running OOMMF.

    """
    def call(self, argstr, need_stderr=False):
        """Calls mumax3 by passing ``argstr`` to mumax3.

        Parameters
        ----------
        argstr : str

            Argument string passed to mumax3.

        need_stderr : bool

            If ``need_stderr=True``, standard error is captured. Defaults to
            ``False``.

        Raises
        ------
        RuntimeError

            If an error occured.

        Returns
        -------
        int

            When the mumax3 run was successful, ``0`` is returned.

        Examples
        --------
        1. Getting mumax3 runner automatically and calling it.

        >>> import mumax3c as mc
        ...
        >>> runner = oc.mumax3.get_mumax3_runner()
        >>> runner.call(argstr='')
        Running mumax3...
        CompletedProcess(...)

        """
        now = datetime.datetime.now()
        timestamp = '{}/{:02d}/{:02d} {:02d}:{:02d}'.format(now.year,
                                                            now.month,
                                                            now.day,
                                                            now.hour,
                                                            now.minute)
        print(f'Running mumax3 ({self.__class__.__name__}) [{timestamp}]... ',
              end='')

        tic = time.time()
        res = self._call(argstr=argstr, need_stderr=need_stderr)
        toc = time.time()
        seconds = '({:0.1f} s)'.format(toc - tic)
        print(seconds)  # append seconds to the previous print.

        if res.returncode != 0:
            if sys.platform != 'win32':
                # Only on Linux and MacOS - on Windows we do not get stderr and
                # stdout.
                stderr = res.stderr.decode('utf-8', 'replace')
                stdout = res.stdout.decode('utf-8', 'replace')
                cmdstr = ' '.join(res.args)
                print('mumax3 error:')
                print(f'\tcommand: {cmdstr}')
                print(f'\tstdout: {cmdstr}')
                print(f'\tstderr: {stderr}')
                print('\n')
            raise RuntimeError('Error in OOMMF run.')

        return res

    @abc.abstractmethod
    def _call(self, argstr, need_stderr=False):
        """This method should be implemented in subclass.

        """
        pass  # pragma: no cover


@uu.inherit_docs
class ExeMumax3Runner(Mumax3Runner):
    """mumax3 runner using mumax3 executable, which can be found on $PATH.

    Parameters
    ----------
    mumax3_exe: str

        Name or path of the mumax3 executable. Defaults to
        ``mumax3``.

    """
    def __init__(self, mumax3_exe='mumax3'):
        self.mumax3_exe = mumax3_exe

    def _call(self, argstr, need_stderr=False):
        cmd = [self.mumax3_exe, argstr]
        return sp.run(cmd, stdout=sp.PIPE, stderr=sp.PIPE)


def get_mumax3_runner(use_cache=True, mumax3_exe='mumax3',
                      optirun_exe='optirun'):
    """Find the best available way to run mumax3.

    Returns a ``mumax3c.mumax3.Mumax3Runner`` object, or raises
    ``EnvironmentError`` if no suitable method is found.

    Parameters
    ----------
    use_cache : bool

        The first call to this function will determine the best way to run
        mumax3 and cache it. Normally, subsequent calls will return the
        ``Mumax3Runner`` object from the cache. Setting this parameter to
        ``False`` will cause it to check for available methods again. Defaults
        to ``True``.

    mumax3_exe : str

        The name or path of the executable ``mumax3`` command. Defaults to
        ``mumax3``.

    optirun_exe : str

        The name or path of the executable ``optirun`` command. Defaults to
        ``optirun``.

    Returns
    -------
    mumax3c.mumax3.Mumax3Runner

        A mumax3 runner.

    Raises
    ------
    EnvironmentError

        If mumax3 cannot be found on host.

    Examples
    --------
    1. Getting mumax3 Runner.

    >>> import mumax3c as mc
    ...
    >>> runner = mc.mumax3.get_mumax3_runner()
    >>> isinstance(runner, mc.mumax3.Mumax3Runner)
    True

    """
    global _cached_mumax3_runner
    if use_cache and (_cached_mumax3_runner is not None):
        return _cached_mumax3_runner

    if shutil.which(optirun_exe):
        cmd = 'optirun mumax3'
    elif shutil.which(mumax3_exe):
        cmd = 'mumax3'
    else:
        msg = 'mumax3 cannot be found'
        raise EnvironmentError(msg)

    _cached_mumax3_runner = ExeMumax3Runner(mumax3_exe=cmd)
    return _cached_mumax3_runner


def status():
    """Run a macrospin example for 1 ps through mumax3c and print the mumax3
    status.

    Returns
    -------
    int

        If ``0``, the mumax3 is found and running. Otherwise, ``1`` is
        returned.

    Examples
    --------
    1. Checking the mumax3 status.

    >>> import mumax3c as mc
    ...
    >>> mc.mumax3c.status()
    Running mumax3...
    mumax3 found and running.
    0

    """
    system = mm.examples.macrospin()
    try:
        td = mc.TimeDriver()
        td.drive(system, t=1e-12, n=1)
        print('mumax3 found and running.')
        return 0
    except (EnvironmentError, RuntimeError):
        print('Cannot find mumax3.')
        return 1


def overhead():
    """Run a macrospin example for 1 ps through ``mumax3c`` and directly and
    return the difference in run times.

    Returns
    -------
    float

      The time difference (overhead) between running mumax3 though ``mumax3c``
      and directly.

    Examples
    --------
    1. Getting the overhead time.

    >>> import mumax3c as mc
    ...
    >>> isinstance(mc.muamx3.overhead(), float)
    Running mumax3...
    True

    """
    # Running mumax3 through mumax3c.
    system = mm.examples.macrospin()
    td = mc.TimeDriver()
    mumax3c_start = time.time()
    td.drive(system, t=1e-12, n=1, save=True, overwrite=True)
    mumax3c_stop = time.time()
    mumax3c_time = mumax3c_stop - mumax3c_start

    # Running OOMMF directly.
    mumax3_runner = get_mumax3_runner()
    mx3path = os.path.realpath(os.path.join(system.name,
                                            'drive-0',
                                            'macrospin.mif'))
    mumax3_start = time.time()
    mumax3_runner.call(mx3path)
    mumax3_stop = time.time()
    mumax3_time = mumax3_stop - mumax3_start
    mc.delete(system)

    return mumax3c_time - mumax3_time
