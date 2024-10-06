'''Calculation of refractive index of PDMS by Pfund method.'''
import pandas as pd
import numpy as np
from uncertainties import unumpy as un
from uncertainties import ufloat


def calculate_diameter_cm(reference_cm, reference_pixel, diameter_pixel):
	return diameter_pixel * reference_cm / reference_pixel


def calculate_refrac_n(h, D):
	return un.sqrt(16 * h**2 + D**2) / D


def main():
	# Calculating dark spot diameter
	df_diameter = pd.read_csv('pfund_diameters.CSV').dropna()
	
	reference_cm = df_diameter['reference_cm']
	reference_pixel = df_diameter['reference_pixel']
	diameter_h_pixel = df_diameter['diameter_h_pixel']
	diameter_v_pixel = df_diameter['diameter_v_pixel']

	diameter_h_cm = calculate_diameter_cm(reference_cm, reference_pixel, diameter_h_pixel)
	diameter_v_cm = calculate_diameter_cm(reference_cm, reference_pixel, diameter_v_pixel)


	df_diameter['diameter_h_cm'] = diameter_h_cm
	df_diameter['diameter_v_cm'] = diameter_v_cm
	df_diameter.loc['Mean'] = df_diameter.mean()
	df_diameter.loc['std'] = df_diameter.std()

	diameter_mean = (df_diameter.loc['Mean']['diameter_h_cm'] + df_diameter.loc['Mean']['diameter_v_cm']) / 2
	diameter_std = ((df_diameter.loc['std']['diameter_h_cm'] + df_diameter.loc['std']['diameter_v_cm']) / 2)
	df_diameter['diameter_mean_cm'] = np.nan
	df_diameter['diameter_std_cm'] = np.nan
	df_diameter.at[0, 'diameter_mean_cm'] = diameter_mean
	df_diameter.at[0, 'diameter_std_cm'] = diameter_std
	
	df_diameter.to_csv('pfund_diameters_analyzed.CSV')
	# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
		# print('\n', df_diameter)


	# Calculating PDMS thickness
	df_thickness = pd.read_csv('PDMS_thickness.CSV')
	thickness_mean = df_thickness['thickness_cm'].mean()
	thickness_std = df_thickness['thickness_cm'].std()

	df_thickness.loc['Mean'] = thickness_mean
	df_thickness['thickness_mean_cm'] = np.nan
	df_thickness['thickness_std_cm'] = np.nan
	df_thickness.at[0, 'thickness_mean_cm'] = thickness_mean
	df_thickness.at[0, 'thickness_std_cm'] = thickness_std

	df_thickness.to_csv('PDMS_thickness_analyzed.CSV')
	# print('\n',df_thickness)


	# Calculate refractive index
	thickness = ufloat(thickness_mean, thickness_std)
	diameter = ufloat(diameter_mean, diameter_std)
	refrac_n = calculate_refrac_n(thickness, diameter)

	print(f'\nMean thickness: {thickness}')
	print(f'Mean diameter: {diameter}')
	print(f'PDMS refractive index: {refrac_n}')


	# Export results
	df_results = pd.DataFrame({'thickness_mean_cm': [thickness_mean], 'thickness_std_cm': [thickness_std],
				  			   'diameter_mean_cm': [diameter_mean], 'diameter_std_cm': [diameter_std],
							   'refractive_index': [refrac_n.n], 'refractive_index_std': [refrac_n.s]})

	df_results.to_csv('27-09-24_PDMS_refractive_index.CSV')
	# with pd.option_context('display.max_columns', None):
		# print('\n', df_results)


if __name__ == '__main__':
	main()



