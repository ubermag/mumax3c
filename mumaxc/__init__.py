import pkg_resources
from .hamiltonian import *
from .dynamics import *
from .mesh import Mesh
from .system import System
from .drivers import *
from .mumax import *
from micromagneticmodel.consts import mu0, e, me, kB, h, g, \
    hbar, gamma, muB, gamma0

__version__ = pkg_resources.get_distribution(__name__).version
__dependencies__ = pkg_resources.require(__name__)
