import pkg_resources
from micromagneticmodel.consts import e, g, gamma, gamma0, h, hbar, kB, me, mu0, muB

from .drivers import *
from .dynamics import *
from .hamiltonian import *
from .mesh import Mesh
from .mumax import *
from .system import System

__version__ = pkg_resources.get_distribution(__name__).version
__dependencies__ = pkg_resources.require(__name__)
