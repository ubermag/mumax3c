import oommfc as mc
#import mumaxc as mc
import discretisedfield as df
import numpy as np


# Material Parameters
mu0 = 4*np.pi*1e-7
H = 0
Ms = 8e5  # saturation magnetisation (A/m)
A = 1.3e-11  # exchange energy constant (J/m)
l_ex = np.sqrt(2*A / (4*np.pi*1e-7 * Ms**2)) # Exchange Length

# Geometry parameters
d = 0.1*l_ex
L = 5.0*d
t = 0.1 * d
h = d/20


assert h < (l_ex / 3.0)
print(f"Exchange Length = {l_ex}")
print(f"d / l_ex = {d/l_ex}")
print(f"H = {H}")

H_field = H * np.array([1, 1, 1]) / np.sqrt(3)  # external magnetic field in the x-direction (A/m)
gamma = 2.211e5  # gamma parameter (m/As)
alpha = 1.0  # Gilbert damping

mesh = mc.Mesh(p1=(0, 0, 0), p2=(L, d, t), cell=(h, h, h))
system = mc.System(name='stdprob2')
system.hamiltonian = mc.Exchange(A=A) + mc.Demag() + mc.Zeeman(H=H_field)
system.dynamics = mc.Precession(gamma=gamma) + mc.Damping(alpha=alpha)
system.m = df.Field(mesh, value=(0, 0, 1), norm=Ms)

md = mc.MinDriver()
md.drive(system, overwrite=True)

mx, my, mz = system.m.average

system.m.plot_plane("z")
