import mumax3c as calc


def test_version():
    assert isinstance(calc.__version__, str)
    assert '.' in calc.__version__


def test_dependencies():
    assert isinstance(calc.__dependencies__, list)
    assert len(calc.__dependencies__) > 0
