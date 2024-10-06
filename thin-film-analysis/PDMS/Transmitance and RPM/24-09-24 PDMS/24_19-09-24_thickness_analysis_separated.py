import pandas as pd
import sys
import os
import numpy as np
from uncertainties import ufloat


def main():
	sys.path.insert(0, '../../../Analyzers')
	import thickness_analyzer as ta

	filename = './inclination_angles.txt'
	df = pd.read_csv(filename)

	alpha_mean = df['alpha1'].mean()
	alpha_std = df['alpha1'].std() / (len(df['alpha1'] - 1))
	ualpha = ufloat(alpha_mean, alpha_std)

	# Refractive index
	# refrac_n = ufloat(1.76, 0.13) # Measured with microscope
	# refrac_n = ufloat(1.4235, 0) # Internet
	refrac_n = ufloat(1.4230060554603676, 0.03977302172611098) # Pfund

	sys.path.insert(0, '../Analyzers')
	import thickness_analyzer as ta

	# PDMS made on 19-09-24 at alpha angle
	# Directory for transmitance vs wavelength.
	trans_directory = "./PDMS trans measured 24-09-24/19-09-24 PDMS trans/"
	listdir = os.listdir(trans_directory)
	listdir = [trans_directory + filename for filename in listdir]
	listdir = sorted(listdir, key = ta.extract_integer)

	# RPM
	RPM_df = pd.read_csv('../19-09-24 PDMS/19-09-24_RPM.CSV', skiprows = [1, 10, 11])
	RPM = RPM_df['RPM']

	# Wavelength bounds
	default_min_wl = 440
	default_max_wl = 740

	# Default bounds
	wavelength_bounds = np.array([[default_min_wl, default_max_wl] for i in range(len(listdir))])
	# Max corrections adds value in list to calculation made by calculate_n_max
	max_corrections = np.zeros(len(listdir))

	# Modifying bounds and corrections for specific film
	max_corrections[0] = -5

	# Calculate number of maxima
	n_max, wavelength_bounds = ta.calculate_n_max(listdir, wavelength_bounds, RPM, max_corrections, graph = False)

	# I'll omit index 6, 7 and the damaged films
	remove_index = [1, 6, 7]
	listdir = np.delete(listdir, remove_index)
	wavelength_bounds = np.delete(wavelength_bounds, remove_index, axis=0)
	max_corrections = np.delete(max_corrections, remove_index)
	n_max = np.delete(n_max, remove_index)
	RPM_df.drop(index = remove_index, inplace = True)
	RPM = RPM_df['RPM']

	# Calculate thickness
	uthickness = ta.calculate_thickness(refrac_n, n_max, wavelength_bounds[:, 0], wavelength_bounds[:, 1], alpha = ualpha)
	uthickness = uthickness / 1000
	thickness = [t.n for t in uthickness]
	thickness_std = [t.s for t in uthickness]

	# Films with less PDMS
	df_filename = '../../Thickness vs RPM/Data/less_PDMS_thickness_RPM_alpha_24_19-09-24.CSV'
	ta.export_df(RPM_df[:5], thickness[:5], thickness_std[:5], wavelength_bounds[:5], 
				 n_max[:5], listdir[:5], df_filename, show = True)
	# ta.graph_thickness(RPM[:5], RPM_std[:5], thickness[:5], thickness_std[:5],
	#				   "Less PDMS - Thickness vs RPM\n19-09-24")

	# Films with more PDMS
	df_filename = '../../Thickness vs RPM/Data/more_PDMS_thickness_RPM_alpha_24_19-09-24.CSV'
	ta.export_df(RPM_df[5:], thickness[5:], thickness_std[5:], wavelength_bounds[5:], 
				 n_max[5:], listdir[5:], df_filename, show = True)
	# ta.graph_thickness(RPM[5:], RPM_std[5:], thickness[5:], thickness_std[5:],
	#				   "More PDMS - Thickness vs RPM\n19-09-24")

if __name__ == '__main__':
	main()