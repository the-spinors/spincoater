import pandas as pd
import sys
import os
import numpy as np
from uncertainties import ufloat
from uncertainties import umath


def calculate_refractive_index(m, m_alpha, wavelength_bounds, wavelength_bounds_alpha, alpha):
	min_wl, max_wl = wavelength_bounds[:, 0], wavelength_bounds[:, 1]
	min_wl_alpha, max_wl_alpha = wavelength_bounds_alpha[:, 0], wavelength_bounds_alpha[:, 1]

	wl_diff = (1 / min_wl) - (1 / max_wl)
	wl_diff_alpha = (1 / min_wl_alpha) - (1 / max_wl_alpha)
	numerator = -(m**2) * (wl_diff_alpha**2) * (np.sin(np.deg2rad(alpha))**2)
	denominator = (m_alpha**2) * (wl_diff**2) - (m**2) * (wl_diff_alpha**2)
	return np.sqrt(np.abs(numerator) / np.abs(denominator))


def u_calculate_refractive_index(m, m_alpha, wavelength_bounds, wavelength_bounds_alpha, alpha):
	min_wl, max_wl = wavelength_bounds[:, 0], wavelength_bounds[:, 1]
	min_wl_alpha, max_wl_alpha = wavelength_bounds_alpha[:, 0], wavelength_bounds_alpha[:, 1]

	wl_diff = (1 / min_wl) - (1 / max_wl)
	wl_diff_alpha = (1 / min_wl_alpha) - (1 / max_wl_alpha)
	numerator = -(m**2) * (wl_diff_alpha**2) * (umath.sin(umath.radians(alpha))**2)
	denominator = (m_alpha**2) * (wl_diff**2) - (m**2) * (wl_diff_alpha**2)
	refrac_ns = []
	for n, d in zip(numerator, denominator):
		try:
			refrac_ns.append(umath.sqrt(umath.fabs(n) / umath.fabs(d)))
		except ValueError:
			refrac_ns.append('nan')
	return refrac_ns


def main():
	sys.path.insert(0, '../Analyzers')
	import thickness_analyzer as ta

	filename = './Inclination angles/inclination_angles.txt'
	df = pd.read_csv(filename)

	alpha_mean = df['alpha1'].mean()
	alpha_std = df['alpha1'].std() / (len(df['alpha1'] - 1))
	ualpha = ufloat(alpha_mean, alpha_std)

	sys.path.insert(0, '../Analyzers')
	import thickness_analyzer as ta

	# PDMS made on 11-09-24 at alpha angle
	# Directory for transmitance vs wavelength.
	trans_directory = "./PDMS trans measured 24-09-24/11-09-24 PDMS trans/"
	listdir = os.listdir(trans_directory)
	listdir = [trans_directory + filename for filename in listdir]
	listdir = sorted(listdir, key = ta.extract_integer)

	# RPM
	RPM_df = pd.read_csv('../11-09-24 PDMS/11-09-24_RPM.CSV')
	RPM = RPM_df['RPM']
	RPM_std = [float(RPM_std) for RPM_std in RPM_df['RPM_std']]

	# Wavelength bounds
	default_min_wl = 440
	default_max_wl = 740

	# Default bounds
	wavelength_bounds = np.array([[default_min_wl, default_max_wl] for i in range(len(listdir))])
	# Max corrections adds value in list to calculation made by calculate_n_max
	max_corrections = np.zeros(len(listdir))

	# Modifying bounds and corrections for specific film
	max_corrections[1], wavelength_bounds[1, 0], wavelength_bounds[1, 1] = -1, 460, 687
	max_corrections[2], wavelength_bounds[2, 0], wavelength_bounds[2, 1] = 0, 493, 696
	max_corrections[3], wavelength_bounds[3, 0], wavelength_bounds[3, 1] = 0, 443, 647
	max_corrections[4], wavelength_bounds[4, 0], wavelength_bounds[4, 1] = 0, 533, 658
	max_corrections[5], wavelength_bounds[5, 0], wavelength_bounds[5, 1] = 0, 567, 633

	# We'll omit index 5 and 6 as they're not that clear
	remove_index = [5, 6]
	listdir = np.delete(listdir, remove_index)
	wavelength_bounds = np.delete(wavelength_bounds, remove_index, axis=0)
	max_corrections = np.delete(max_corrections, remove_index)
	RPM_df.drop(index = remove_index, inplace = True)
	RPM = RPM_df['RPM']
	RPM_std = [float(RPM_std) for RPM_std in RPM_df['RPM_std']]

	# Calculate number of maxima
	n_max = ta.calculate_n_max(listdir, wavelength_bounds, RPM, max_corrections, graph = False)

	# We'll rename as these are the arrays for 11-09-24 at an alpha angle
	n_max_11_alpha = np.array(n_max)
	wavelength_bounds_11_alpha = np.array(wavelength_bounds)


	# PDMS made on 19-09-24 at alpha angle
	# Directory for transmitance vs wavelength.
	trans_directory = "./PDMS trans measured 24-09-24/19-09-24 PDMS trans/"
	listdir = os.listdir(trans_directory)
	listdir = [trans_directory + filename for filename in listdir]
	listdir = sorted(listdir, key = ta.extract_integer)

	# RPM
	RPM_df = pd.read_csv('../19-09-24 PDMS/19-09-24_RPM.CSV', skiprows = [1, 10, 11])

	# Wavelength bounds
	default_min_wl = 440
	default_max_wl = 740

	# Default bounds
	wavelength_bounds = np.array([[default_min_wl, default_max_wl] for i in range(len(listdir))])
	# Max corrections adds value in list to calculation made by calculate_n_max
	max_corrections = np.zeros(len(listdir))

	# Modifying bounds and corrections for specific film
	max_corrections[0] = -5

	# I'll omit index 6, 7
	remove_index = [6, 7]
	listdir = np.delete(listdir, remove_index)
	wavelength_bounds = np.delete(wavelength_bounds, remove_index, axis=0)
	max_corrections = np.delete(max_corrections, remove_index)
	RPM_df.drop(index = remove_index, inplace = True)
	RPM = RPM_df['RPM']
	RPM_std = [float(RPM_std) for RPM_std in RPM_df['RPM_std']]

	# Calculate number of maxima
	n_max = ta.calculate_n_max(listdir, wavelength_bounds, RPM, max_corrections, graph = False)

	# We'll rename as these are the arrays for 19-09-24 at an alpha angle
	n_max_19_alpha = np.array(n_max)
	wavelength_bounds_19_alpha = np.array(wavelength_bounds)


	# Now get measurements at 0 angle from 11-09-24 and 19-09-24
	PDMS_11_df = pd.read_csv('../11-09-24 PDMS/PDMS_thickness_RPM_11-09-24.CSV', skiprows = [6, ])
	PDMS_19_df = pd.read_csv('../19-09-24 PDMS/PDMS_thickness_RPM_19-09-24.CSV',skiprows = [7, 8, 9])
	pd.set_option('display.max_rows', None, 'display.max_columns', None,
						  'display.width', 1000)

	n_max_11 = np.array(PDMS_11_df['n_max'])
	wavelength_bounds_11 = np.array([[min_wl, max_wl] for min_wl, max_wl in zip(PDMS_11_df['min_wavelength'], PDMS_11_df['max_wavelength'])])
	n_max_19 = np.array(PDMS_19_df['n_max'])
	wavelength_bounds_19 = np.array([[min_wl, max_wl] for min_wl, max_wl in zip(PDMS_19_df['min_wavelength'], PDMS_19_df['max_wavelength'])])


	# Calculate refractive indices
	n_max_alpha = np.append(n_max_11_alpha, n_max_19_alpha)
	wavelength_bounds_alpha = np.vstack((wavelength_bounds_11_alpha, wavelength_bounds_19_alpha))

	n_max = np.append(n_max_11, n_max_19)
	wavelength_bounds = np.vstack((wavelength_bounds_11, wavelength_bounds_19))

	refrac_ns = calculate_refractive_index(n_max, n_max_alpha, wavelength_bounds, wavelength_bounds_alpha, ualpha.n)
	# refrac_ns = np.delete(refrac_ns, [2,3,5,6])
	refrac_ns = np.delete(refrac_ns, [5])

	refrac_n_std = refrac_ns.std() / np.sqrt(len(refrac_ns))
	refrac_n = refrac_ns.mean()
	u_refrac_n = ufloat(refrac_n, refrac_n_std)
	print(f"Refractive index: {u_refrac_n}")


if __name__ == '__main__':
	main()
