'''.py to calculate required PDMS mass for measurable Pfund.'''

import numpy as np


def pfund_thickness(D, n):
	return D * np.sqrt(n**2 - 1) / 4


# Diameter of darkness
D = 2 # cm
# Sidelengths of stamp
L = 2 # cm
# PDMS density
rho = 0.965	# g/cm³


# Refractive indices
# Literature
n_lit = 1.41
# Maximum predicted
n_max = 1.86

# Required thickness
t_lit = pfund_thickness(D, n_lit)
t_max = pfund_thickness(D, n_max)

print(f"Required thickness for lit: {t_lit:.2f}")
print(f"Required thickness for max index: {t_max:.2f}")

# Required volume
V_lit = t_lit * L**2
V_max = t_max * L**2

# Required mass
m_lit = V_lit * rho
m_max = V_max * rho

print(f"Required mass for lit: {m_lit:.2f}")
print(f"Required mass for max index: {m_max:.2f}")
