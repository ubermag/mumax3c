from .driver import Driver


class RelaxDriver(Driver):
    """Energy minimisation driver.

    Only attributes in ``_allowed_attributes`` can be defined. For details on
    possible values for individual attributes and their default values, please
    refer to ``Mumax3`` documentation (https://mumax.github.io).

    Examples
    --------
    1. Defining driver with a keyword argument.

    >>> import mumax3c as mc
    ...
    >>> rd = mc.RelaxDriver(DemagAccuracy=6)

    2. Passing an argument which is not allowed.

    >>> import mumax3c as mc
    ...
    >>> rd = mc.RelaxDriver(myarg=1)
    Traceback (most recent call last):
       ...
    AttributeError: ...

    3. Getting the list of allowed attributes.

    >>> import mumax3c as mc
    ...
    >>> rd = mc.RelaxDriver()
    >>> rd._allowed_attributes
    [...]

    """

    _allowed_attributes = [
        "MinimizerStop",
        "DemagAccuracy",
        "Headroom",
        "LastErr",
        "MaxErr",
        "RelaxTorqueThreshold",
        "NEval",
        "PeakErr",
    ]

    def _checkargs(self, **kwargs):
        pass  # no kwargs should be checked

    @property
    def _x(self):
        return "t"  # TODO correct iteration
