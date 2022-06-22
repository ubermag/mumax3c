import os
import shutil

import mumax3c as calc


def check_runner(runner):
    # Testing mumax3c on an mx3 file to make it independent of mumax3c.
    dirname = os.path.join(os.path.dirname(__file__), "test_sample")
    os.chdir(dirname)
    argstr = "test_mumax3.mx3"

    res = runner.call(argstr)
    assert res.returncode == 0

    # Cleanup created files.
    for f in os.listdir(dirname):
        if f.endswith(".json"):
            os.remove(os.path.join(dirname, f))
        elif os.path.isdir(f) and f.endswith(".out"):
            shutil.rmtree(f)


def test_exemumax3runner():
    # ExeMumax3Runner runs when callable mumax3 exists ('mumax3').
    mumax3_exe = "mumax3"
    runner = calc.mumax3.ExeMumax3Runner(mumax3_exe)
    check_runner(runner)


def test_get_mumax3_runner():
    # Tclmumax3Runner
    runner = calc.runner.runner
    assert isinstance(runner, calc.mumax3.ExeMumax3Runner)
    check_runner(runner)


def test_status():
    assert calc.runner.runner.status == 0


def test_overhead():
    assert isinstance(calc.mumax3.overhead(), float)
