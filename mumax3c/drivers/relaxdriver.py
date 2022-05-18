from .driver import Driver


class RelaxDriver(Driver):
    """Energy minimisation driver.

    Only attributes in ``_allowed_attributes`` can be defined. For details on
    possible values for individual attributes and their default values, please
    refer to ``Oxs_MinDriver`` documentation (https://math.nist.gov/oommf/).

    Examples
    --------
    1. Defining driver with a keyword argument.

    >>> import oommfc as oc
    ...
    >>> md = oc.MinDriver(stopping_mxHxm=0.01)

    2. Passing an argument which is not allowed.

    >>> import oommfc as oc
    ...
    >>> md = oc.MinDriver(myarg=1)
    Traceback (most recent call last):
       ...
    AttributeError: ...

    3. Getting the list of allowed attributes.

    >>> import oommfc as oc
    ...
    >>> md = oc.MinDriver()
    >>> md._allowed_attributes
    [...]

    """

    _allowed_attributes = ["MinimizerStop", "DemagAccuracy"]

    def _checkargs(self, **kwargs):
        pass  # no kwargs should be checked
