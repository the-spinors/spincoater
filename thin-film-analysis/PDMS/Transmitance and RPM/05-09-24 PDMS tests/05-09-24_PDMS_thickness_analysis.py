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
	trans_directory = "./trans/"
	listdir = os.listdir(trans_directory)
	listdir = [trans_directory + filename for filename in listdir]
	listdir = sorted(listdir)

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

	# Modifying for specific film
	pass

	# We're using the RPM calculated for other rounds with the same nominal RPM
	RPM = [3726.713825413873, 5523.750090442081]
	RPM_std = [1.8899683829480904, 3.3705773483277386]

	# Calculate number of maxima
	n_max, wavelength_bounds = ta.calculate_n_max(listdir, wavelength_bounds, RPM, max_corrections, graph = False)

	# Calculate thickness
	uthickness = ta.calculate_thickness(refrac_n, n_max, wavelength_bounds[:, 0], wavelength_bounds[:, 1])
	uthickness = uthickness / 1000
	thickness = [t.n for t in uthickness]
	thickness_std = [t.s for t in uthickness]

	# Data to df and CSV
	short_filenames = [filename.split('/')[-1] for filename in listdir]
	thickness_RPM_df = pd.DataFrame({'transmitance_filename': short_filenames, 'PDMS #': ['test1', 'test2'],
									'RPM': RPM_std, 'RPM_std': RPM_std, 'thickness (um)': thickness,
									'thickness_std': thickness_std})


	filename = '../../Thickness vs RPM/Data/PDMS_thickness_RPM_05-09-24.CSV'
	thickness_RPM_df.to_csv(filename)
	pd.set_option('display.max_rows', None, 'display.max_columns', None,
						  'display.width', 1000)
	print(thickness_RPM_df)

	ta.graph_thickness(RPM, RPM_std, thickness, thickness_std, "PDMS - Thickness vs RPM\n05-09-24")


if __name__ == '__main__':
	main()
