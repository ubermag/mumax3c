from .driver import Driver


class TimeDriver(Driver):
    """Time driver.

    Only attributes in ``_allowed_attributes`` can be defined. For details on
    possible values for individual attributes and their default values, please
    refer to ``Mumax3`` documentation (https://mumax.github.io).

    Examples
    --------
    1. Defining driver with a keyword argument.

    >>> import mumax3c as mc
    ...
    >>> td = mc.TimeDriver(DemagAccuracy=6)

    2. Passing an argument which is not allowed.

    >>> import mumax3c as mc
    ...
    >>> td = mc.TimeDriver(myarg=1)
    Traceback (most recent call last):
       ...
    AttributeError: ...

    3. Getting the list of allowed attributes.

    >>> import mumax3c as mc
    ...
    >>> td = mc.TimeDriver()
    >>> td._allowed_attributes
    [...]

    """

    _allowed_attributes = [
        "DemagAccuracy",
        "dt",
        "FixDt",
        "Headroom",
        "LastErr",
        "MaxDt",
        "MaxErr",
        "MinDt",
        "NEval",
        "PeakErr",
        "step",
        "t",
    ]

    def _checkargs(self, **kwargs):
        t, n = kwargs["t"], kwargs["n"]
        if t <= 0:
            msg = f"Cannot drive with {t=}."
            raise ValueError(msg)
        if not isinstance(n, int):
            msg = f"Cannot drive with {type(n)=}."
            raise ValueError(msg)
        if n <= 0:
            msg = f"Cannot drive with {n=}."
            raise ValueError(msg)

    @property
    def _x(self):
        return "t"
