import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy as sp
import os
import glob
import sys
from uncertainties import ufloat
from matplotlib.patches import Rectangle


def main():
	# Modules
	sys.path.insert(0, '../../Analyzers')
	import thickness_vs_RPM_analyzer as tR

	# Directory, parameters for plot and function for curve fit
	directory = './Data/*.CSV'
	xlabel = 'RPM'
	ylabel = 'Grosor (μm)'

	rc_update = {'font.size': 30, 'font.family': 'serif',
				 'font.serif': ['Times New Roman', 'FreeSerif'], 'mathtext.fontset': 'cm',
				 'lines.linewidth': 3, 'lines.markersize': 4}
	plt.rcParams.update(rc_update)
	colors = ['#0040eb', '#ffbf14', '#ff7f79', '#008086', '#c10000', '#56cccc']
	linestyle = ['-', '--', '-', '--', '-', '--']
	labels = ["$\\alpha = 0$° — 1.5 min", "$\\alpha = (29.8\\pm0.4)$° — 1.5 min",
			  "$\\alpha = 0$° — 2 min", '$\\alpha = (29.8\\pm0.4)$° — 2 min ',
			  "$\\alpha = 0$° — 2 min (++PDMS)", "$\\alpha = (29.8\\pm0.4)$° — 2 min (++PDMS)"]
	title = "PDMS - Grosor ($d$) vs RPM Nominal\nAjuste: $d = p / RPM$"
	graph_filename = "../../Figures/PDMS - Thickness vs RPM.png"

	function = lambda R, p: p / R

	# I/O
	listdir = glob.glob(directory)
	listdir = sorted(listdir)
	dfs = []

	for filename in listdir:
		# Skip test runs
		if '05' in filename:
			continue
		dfs.append(pd.read_csv(filename))

	# Curve fits
	parameters, covariances = tR.individual_curve_fit(dfs, function)

	# Plot
	RPM_bounds = [[1400, 6000], [1400, 6000],
				  [1000, 6000], [1000, 6000],
				  [1100, 6000], [1100, 6000]]
	fig, ax = plt.subplots(figsize = (13, 9))

	# Plotting data
	tR.graph(dfs, fig, ax, labels, title, linestyle, xlabel, ylabel, colors)

	# Plotting individual fits
	for df, p, c, label, color, ls, bounds in zip(dfs, parameters, covariances, labels, colors, linestyle, RPM_bounds):
		RPM = df['RPM']
		rpm = np.linspace(bounds[0], bounds[-1], 1000)
		u_parameter = ufloat(p, np.sqrt(c))
		# Relative error
		rel_STD = float(np.sqrt(c) / p) * 100
		ax.plot(rpm, function(rpm, p),
				label = f'   {label}\n   $p$ = $({float(p):.3E})\\pm{rel_STD:.2f}\\%$',
				linestyle = ls, color = color, alpha = 1, zorder=1)


	# BG for legend
	x_square = 2200
	y_square = 38
	width = 4000
	height = 22
	xlims = [750, 6250]
	ylims = [5, 61]
	ax.add_patch(Rectangle((x_square, y_square), width, height, facecolor="#eee", zorder=3))

	# BG for legend
	x_square = 4150
	y_square = 25
	width = 2050
	height = 22
	xlims = [750, 6250]
	ylims = [5, 61]
	ax.add_patch(Rectangle((x_square, y_square), width, height, facecolor="#eee", zorder=3))

	ax.set(xlim = xlims, ylim = ylims)
	#Legend
	ax.legend(
		framealpha=0,
		loc=1,
	    fontsize=15,
	    ncols=2, 
	    borderaxespad=0.6,
	    handletextpad=0.1,
	    labelspacing=0.75,
	    markerscale=2,
    )
	plt.tight_layout()
	# plt.show()
	plt.savefig(graph_filename, bbox_inches='tight', dpi=300)


if __name__ == '__main__':
	main()