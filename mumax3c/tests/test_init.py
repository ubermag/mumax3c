import mumax3c as mc


def test_version():
    assert isinstance(mc.__version__, str)
    assert "." in mc.__version__


def test_dependencies():
    assert isinstance(mc.__dependencies__, list)
    assert len(mc.__dependencies__) > 0
