import mumax3c as mc


def test_version():
    assert isinstance(mc.__version__, str)
    assert "." in mc.__version__
