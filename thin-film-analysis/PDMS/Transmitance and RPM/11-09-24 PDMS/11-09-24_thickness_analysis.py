import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
from uncertainties import ufloat


def main():
	sys.path.insert(0, '../../../Analyzers')
	import thickness_analyzer as ta

	# Directory for transmitance vs wavelength.
	trans_directory = "./trans/PDMS/"
	listdir = os.listdir(trans_directory)
	listdir = [trans_directory + filename for filename in listdir]
	listdir = sorted(listdir, key = ta.extract_integer)
	
	# Refractive index
	# refrac_n = ufloat(1.76, 0.13) # Measured with microscope
	# refrac_n = ufloat(1.4235, 0) # Internet
	refrac_n = ufloat(1.4230060554603676,0.03977302172611098) # Pfund

	# Wavelength bounds
	default_min_wl = 440
	default_max_wl = 740

	# Default bounds
	wavelength_bounds = np.array([[default_min_wl, default_max_wl] for i in range(len(listdir))])
	# Max corrections adds value in list to calculation made by calculate_n_max
	max_corrections = np.zeros(len(listdir))

	# Modifying bounds and corrections for specific film
	max_corrections[2], wavelength_bounds[2, 0], wavelength_bounds[2, 1] = -1, 576, 653
	max_corrections[4], wavelength_bounds[4, 0], wavelength_bounds[4, 1] = -2, 512, 706
	max_corrections[5], wavelength_bounds[5, 0], wavelength_bounds[5, 1] = -1, 561, 654
	# max_corrections[6], wavelength_bounds[6, 0], wavelength_bounds[6, 1] = 4, 473, 548

	# RPM
	RPM_df = pd.read_csv('./11-09-24_RPM.CSV')
	
	RPM = RPM_df['RPM']

	# Calculate number of maxima
	n_max, wavelength_bounds = ta.calculate_n_max(listdir, wavelength_bounds, RPM,
												  max_corrections, graph=False)
	
	# Remove damaged (4) or unclear (6) PDMS
	remove_index = [4, 6]
	listdir = np.delete(listdir, remove_index)
	wavelength_bounds = np.delete(wavelength_bounds, remove_index, axis=0)
	max_corrections = np.delete(max_corrections, remove_index)
	n_max = np.delete(n_max, remove_index)
	RPM_df.drop(index = remove_index, inplace = True)
	RPM = RPM_df['RPM']

	# Calculate thickness
	uthickness = ta.calculate_thickness(refrac_n, n_max, wavelength_bounds[:, 0], wavelength_bounds[:, 1])
	uthickness = uthickness / 1000
	thickness = [t.n for t in uthickness]
	thickness_std = [t.s for t in uthickness]

	df_filename = '../../Thickness vs RPM/Data/PDMS_thickness_RPM_11-09-24.CSV'
	ta.export_df(RPM_df, thickness, thickness_std, wavelength_bounds, n_max, listdir, df_filename, show = True)
	ta.graph_thickness(RPM, thickness, thickness_std, "PDMS - Thickness vs RPM\n11-09-24")


if __name__ == '__main__':
	main()