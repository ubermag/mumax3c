from .driver import Driver


class TimeTorqueDriver(Driver):
    """Time driver.

    Only attributes in ``_allowed_attributes`` can be defined. For details on
    possible values for individual attributes and their default values, please
    refer to ``Mumax3`` documentation (https://mumax.github.io).

    Examples
    --------
    1. Defining driver with a keyword argument.

    >>> import mumax3c as mc
    ...
    >>> td = mc.TimeTorqueDriver(MaxTorque=1e-3)

    2. Passing an argument which is not allowed.

    >>> import mumax3c as mc
    ...
    >>> td = mc.TimeTorqueDriver(myarg=1)
    Traceback (most recent call last):
       ...
    AttributeError: ...

    3. Getting the list of allowed attributes.

    >>> import mumax3c as mc
    ...
    >>> td = mc.TimeTorqueDriver()
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
        "maxtorque",
    ]

    def _checkargs(self, **kwargs):
        maxtorque = kwargs["maxtorque"]
        if maxtorque <= 0:
            msg = f"Cannot drive with {maxtorque=}."
            raise ValueError(msg)

    @property
    def _x(self):
        return "maxtorque"
