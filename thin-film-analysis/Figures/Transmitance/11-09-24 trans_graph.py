import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
from uncertainties import ufloat


def import_data(filename):
	df = pd.read_csv(filename, skiprows = 2, sep = "  ", names=["Wavelength", "Transmitance"], engine='python', dtype='float64')
	return df


def graph(x, y, n_max, title, max_positions_x, max_positions_y):
	# rcParams
	rc_update = {'font.size': 30, 'font.family': 'serif',
				 'font.serif': ['Times New Roman', 'FreeSerif'], 'mathtext.fontset': 'cm',
				 'lines.linewidth': 3, 'lines.markersize': 8}
	plt.rcParams.update(rc_update)

	# Plots
	fig, ax = plt.subplots(figsize=(20, 10), dpi=300)
	# Maximum positions
	ax.scatter(max_positions_x, max_positions_y,
			   color = '#ffbf14', linestyle = '--', label = f"Número de máximos: M = {n_max:.0f}",
			   zorder = 2)
	# Data
	ax.plot(x, y, zorder = 1, color='#008086')

	# Limits
	ax.axvline(min(x), color = 'k', linestyle = '--', zorder=0)
	ax.axvline(max(x), color = 'k', linestyle = '--', zorder=0)
	ax.text(min(x) - 11, 22, '$\\lambda_0$',
			fontsize=35)
	ax.text(max(x) + 4, 22, '$\\lambda_f$',
			fontsize=35)

	# Format
	ax.set(title = title, xlabel = "Longitud de onda (nm)", ylabel = "Transmitancia (%)")
	ax.grid(color = '#999', linestyle = '--')
	ax.legend(
		framealpha = 1,
		loc=1,
	    fontsize=26,
	    ncols=2, 
	    borderaxespad=0.3,
	    handletextpad=0.1,
	    markerscale=2,
    )


def get_max_positions(df):
	max_positions_x = []
	max_positions_y = []
	wavelength = df['Wavelength']
	transmitance = df['Transmitance']
	slopes = calculate_slope(transmitance, wavelength)
	for s, n_s, wl, tr in zip(slopes[:-1], slopes[1:], wavelength[1:], transmitance[1:]):
		if s >= 0 and n_s <= 0:
			max_positions_x.append(wl)
			max_positions_y.append(tr)
	return max_positions_x, max_positions_y


def calculate_slope(x, y):
	slopes = []
	for x1, x2, y1, y2 in zip(x[:-1], x[1:], y[:-1], y[1:]):
		slopes.append((y2 - y1) / (x2 - x1))
	return slopes


def main():
	sys.path.insert(0, '../../Analyzers')
	import thickness_analyzer as ta

	# Directory for transmitance vs wavelength.
	filename = './12-09-24_trans_PDMS_2.TRM'
	df = import_data(filename)

	# Default bounds
	min_wl, max_wl = 439.9, 740

	# Max positions
	df = df[df['Wavelength'] > min_wl][df['Wavelength'] < max_wl]
	max_positions_x, max_positions_y = get_max_positions(df)

	# Refiltering df to have maxima at bounds
	min_wl, max_wl = min(max_positions_x), max(max_positions_x)
	df = df[df['Wavelength'] > min_wl][df['Wavelength'] < max_wl]

	title = "Transmitancia (%) vs Longitud de onda (nm)\nPDMS - 4480 RPM; velocidad máxima por 1.5 min"
	graph(df['Wavelength'], df['Transmitance'], len(max_positions_x),
		  title, max_positions_x, max_positions_y)

	figManager = plt.get_current_fig_manager()
	figManager.full_screen_toggle()
	plt.tight_layout()
	# plt.show()
	graph_name = '../PDMS - Film Transmitance.pdf'
	plt.savefig(graph_name)


if __name__ == '__main__':
	main()