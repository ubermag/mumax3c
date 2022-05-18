import abc
import datetime
import logging
import os
import shutil
import subprocess as sp
import sys
import time

import micromagneticmodel as mm
import ubermagutil as uu

import mumax3c as mc

log = logging.getLogger(__name__)
_cached_mumax3_runner = None


class Mumax3Runner(metaclass=abc.ABCMeta):
    """Abstract class for running mumax3."""

    def call(self, argstr, need_stderr=False, verbose=1):
        """Calls mumax3 by passing ``argstr`` to mumax3.

        Parameters
        ----------
        argstr : str

            Argument string passed to mumax3.

        need_stderr : bool

            If ``need_stderr=True``, standard error is captured. Defaults to
            ``False``.

        verbose : int, optional

            If ``verbose=0``, no output is printed. For ``verbose>=1``
            information about the OOMMF runner and the runtime is printed to
            stdout. Defaults is ``verbose=1``.

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
        >>> runner = mc.runner.runner
        >>> runner.call(argstr='')
        Running mumax3...
        CompletedProcess(...)

        """
        if verbose >= 1:
            now = datetime.datetime.now()
            timestamp = "{}/{:02d}/{:02d} {:02d}:{:02d}".format(
                now.year, now.month, now.day, now.hour, now.minute
            )
            print(
                f"Running mumax3 ({self.__class__.__name__}) [{timestamp}]... ", end=""
            )
            tic = time.time()

        res = self._call(argstr=argstr, need_stderr=need_stderr)
        if verbose >= 1:
            toc = time.time()
            seconds = "({:0.1f} s)".format(toc - tic)
            print(seconds)  # append seconds to the previous print.

        if res.returncode != 0:
            msg = "Error in mumax3 run.\n"
            cmdstr = " ".join(res.args)
            msg += f"command: {cmdstr}\n"
            if sys.platform != "win32":
                # Only on Linux and MacOS - on Windows we do not get stderr and
                # stdout.
                stderr = res.stderr.decode("utf-8", "replace")
                stdout = res.stdout.decode("utf-8", "replace")
                msg += f"stdout: {stdout}\n"
                msg += f"stderr: {stderr}\n"
            raise RuntimeError(msg)

        return res

    @abc.abstractmethod
    def _call(self, argstr, need_stderr=False):
        """This method should be implemented in subclass."""
        pass  # pragma: no cover

    def status(self):
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
            td.drive(system, t=1e-12, n=1, runner=self)
            print("mumax3 found and running.")
            return 0
        except (EnvironmentError, RuntimeError):
            print("Cannot find mumax3.")
            return 1


@uu.inherit_docs
class ExeMumax3Runner(Mumax3Runner):
    """mumax3 runner using mumax3 executable, which can be found on $PATH.

    Parameters
    ----------
    mumax3_exe: str

        Name or path of the mumax3 executable. Defaults to
        ``mumax3``.

    """

    def __init__(self, mumax3_exe="mumax3"):
        if isinstance(mumax3_exe, str):
            mumax3_exe = [mumax3_exe]
        self.mumax3_exe = mumax3_exe

    def _call(self, argstr, need_stderr=False):
        cmd = self.mumax3_exe + [argstr]
        return sp.run(cmd, stdout=sp.PIPE, stderr=sp.PIPE)


class Runner:
    """Control the default runner.

    Parameters
    ----------
    cache_runner : bool
        If ``True`` the best way to run mumax3 is only determined once and the
        result is cached. Subsequent calls to the property ``runner`` will
        return the ``Mumax3Runner`` object from the cache. Setting this
        parameter to ``False`` will cause it to check for available methods
        again. Defaults to ``True``.

    mumax3_exe : str

        The name or path of the executable ``mumax3`` command. Defaults to
        ``mumax3``.

    optirun_exe : str

        The name or path of the executable ``optirun`` command. Defaults to
        ``optirun``.

    """

    def __init__(self):
        self.cache_runner = True
        self.mumax3_exe = "mumax3"
        self.optirun_exe = "optirun"
        self._runner = None

    @property
    def runner(self):
        """Return the default mumax3 runner.

        The default runner is determined using ``autoselect_runner()``. If
        ``cache_runner`` is ``True`` the runner is cached during the first call
        and the same runner is returned in subsequent calls to this property.

        This property also allows to set a specific ``Mumax3Runner``. Before
        setting, a new runner is first checked to be functional by calling
        ``runner.status``.

        Examples
        --------
        1. Getting mumax3 Runner.

        >>> import mumax3c as mc
        ...
        >>> runner = mc.runner.runner
        >>> isinstance(runner, mc.mumax3.Mumax3Runner)
        True
        """
        if self.cache_runner and self._runner is not None:
            log.debug("Returning cached runner.")
            return self._runner
        self.autoselect_runner()
        return self._runner

    @runner.setter
    def runner(self, runner):
        if runner.status != 0:
            raise ValueError(f"{runner=} cannot be used.")
        self._runner = runner

    def autoselect_runner(self):
        """Find the best available way to run mumax3.

        The method tries to find a suitable runner by checking the availability of
        ``optirun`` and ``mumax3`` in this order. If no runner can be found an
        ``EnvironmentError`` is raised.

        Raises
        ------
        EnvironmentError

            If mumax3 cannot be found on host.

        Examples
        --------
        1. Getting mumax3 Runner.

        >>> import mumax3c as mc
        ...
        >>> mc.runner.autoselect_runner()
        >>> runner = mc.runner.runner
        >>> isinstance(runner, mc.mumax3.Mumax3Runner)
        True

        """
        log.debug(
            "Starting autoselect_runner: cache_runner=%(cache_runner)s, "
            "mumax3_exe=%(mumax3_exe)s, optirun_exe=%(optirun_exe)s, ",
            {
                "cache_runner": self.cache_runner,
                "mumax3_exe": self.mumax3_exe,
                "optirun_exe": self.optirun_exe,
            },
        )

        cmd = []
        log.debug("Step 1: Checking for optirun.")
        optirun_exe = shutil.which(self.optirun_exe)
        log.debug(
            "Output from 'which optirun_exe=%(optirun_exe)s",
            {"optirun_exe": optirun_exe},
        )
        if optirun_exe:
            cmd.append("optirun")

        log.debug("Step 2: Checking for mumax3")
        mumax3_exe = shutil.which(self.mumax3_exe)
        log.debug(
            "Output from 'which mumax3_exe=%(mumax3_exe)s", {"mumax3_exe", mumax3_exe}
        )
        if mumax3_exe:
            cmd.append("mumax3")
            self._runner = ExeMumax3Runner(cmd)
        else:
            msg = "mumax3 cannot be found"
            raise EnvironmentError(msg)


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

    # Running mumax3 directly.
    mumax3_runner = mc.runner.runner
    mx3path = os.path.realpath(os.path.join(system.name, "drive-0", "macrospin.mx3"))
    mumax3_start = time.time()
    mumax3_runner.call(mx3path)
    mumax3_stop = time.time()
    mumax3_time = mumax3_stop - mumax3_start
    mc.delete(system)

    return mumax3c_time - mumax3_time
