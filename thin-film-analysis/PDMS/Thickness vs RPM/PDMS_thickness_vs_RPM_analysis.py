import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy as sp
import os
import glob
import sys


def main():
	# Modules
	sys.path.insert(0, '../../Analyzers')
	import thickness_vs_RPM_analyzer as tR

	# Directory, parameters for plot and function for curve fit
	directory = './Data/*.CSV'
	xlabel = 'RPM'
	ylabel = 'Thickness (um)'

	colors = ['Purple', 'Red', 'Blue', 'Green', 'Yellow', 'Black']
	linestyle = ['--', '--', '--', '--', '--', '--']
	labels = ["11-09-24", "Inclined 24/11-09-24",
			  "Less PDMS 19-09-24", 'Less PDMS - inclined 24/19-09-24',
			  "More PDMS 19-09-24", "More PDMS - inclined 24/19-09-24"]
	title = "PDMS - Thickness vs RPM\nFit function: thickness = p / RPM"
	graph_filename = "./Figures/PDMS - Thickness vs RPM with inclined plane.pdf"

	function = lambda R, p: p / R

	# I/O
	listdir = glob.glob(directory)
	listdir = sorted(listdir)
	print(listdir)
	dfs = []

	for filename in listdir:
		# Skip test runs
		if '05' in filename:
			continue
		# Skip non separated data from the 24/19th
		if '19' in filename and not ('less' in filename or 'more' in filename):
			continue
		dfs.append(pd.read_csv(filename))

	# Curve fits
	parameters, covariances = tR.individual_curve_fit(dfs, function)

	# rcParams 
	rc_update = {'font.size': 18, 'font.family': 'serif', 'font.serif': ['Times New Roman', 'FreeSerif']}
	plt.rcParams.update(rc_update)

	# Plot
	RPM_bounds = [800, 6000]
	fig, ax = plt.subplots(figsize = (16, 9))

	# Plotting individual fits
	for df, p, c, label, color, ls in zip(dfs, parameters, covariances, labels, colors, linestyle):
		RPM = df['RPM']
		rpm = np.linspace(RPM_bounds[0], RPM_bounds[-1], 1000)
		# Relative error
		rel_STD = float(np.sqrt(c) / p) * 100
		ax.plot(rpm, function(rpm, p),
				label = f'Fit - {label}\np: {float(p):.2f}\nSTD: {rel_STD:.2f}%',
				linestyle = ls, color = color, alpha = 0.5)

	# Plotting data
	tR.graph(dfs, fig, ax, labels, title, linestyle, xlabel, ylabel, colors)
	plt.show()
	plt.savefig(graph_filename, bbox_inches='tight', dpi=200)


if __name__ == '__main__':
	main()