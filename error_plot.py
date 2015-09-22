#!/usr/bin/python

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from optparse import OptionParser

# Matplotlib general parameters :
params = {
	'axes.labelsize': 8,
	'text.fontsize': 8,
	'legend.fontsize': 10,
	'xtick.labelsize': 10,
	'ytick.labelsize': 10,
	'text.usetex': False,
	'figure.figsize': [6.0, 6.0]
}
mpl.rcParams.update(params)

parser = OptionParser()
parser.add_option("-f", "--file", action="store", type="string", dest="wFile")
(options, args) = parser.parse_args()
print options, args, options.wFile

errorValues = np.loadtxt(options.wFile)

print 'Games played:',len(errorValues)

fig, ax1 = plt.subplots()

#x = np.arange(len(errorValues))
#xTicksLabels=['Game '+str(n) for n in np.arange(len(errorValues))]
#plt.xticks(np.arange(len(errorValues)), xTicksLabels, rotation='vertical')
ax1.plot(errorValues , linewidth=2, color='b')
#ax1.plot(x, errorValues , linewidth=2, color='b')
ax1.set_xlabel('Words')
ax1.set_ylabel('Error', color='b')
leg = plt.legend(["Error over time"], loc=2)

plt.show()

outputImage = "plot_"+(options.wFile.split("."))[0]+".png"

fig.savefig(outputImage)
