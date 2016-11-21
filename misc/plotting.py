#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"


# CONSTANTS
import numpy as np
SINGLE_FIG_SIZE = (6,4)
BAR_WIDTH = 0.6
TICK_SIZE = 15
XLABEL_PAD = 10
LABEL_SIZE = 14
TITLE_SIZE = 16
LEGEND_SIZE = 12
LINE_WIDTH = 2
LIGHT_COLOR = '0.8'
LIGHT_COLOR_V = np.array([float(LIGHT_COLOR) for i in xrange(3)])
DARK_COLOR = '0.4'
DARK_COLOR_V = np.array([float(DARK_COLOR) for i in xrange(3)])
ALMOST_BLACK = '0.125'
ALMOST_BLACK_V = np.array([float(ALMOST_BLACK) for i in xrange(3)])
MALE_COLOR = np.array([0.25490196, 0.41176471, 0.88235294])
#FEMALE_COLOR = np.array([1.,  0.36,  0.72])
#FEMALE_COLOR = np.array([ 0.33333333,  0.6745098 ,  0.93333333])
FEMALE_COLOR = np.array([0.40254901960784313, 0.75274509803921569, 0.50254901960784313])
ACCENT_COLOR_1 = np.array([255., 145., 48.]) / 255.  # Trump orange.


# IMPORTS AND CONFIG
from matplotlib import rcParams
#rcParams['text.usetex'] = True #Let TeX do the typsetting
#rcParams['pdf.use14corefonts'] = True
#rcParams['ps.useafm'] = True
#rcParams['text.latex.preamble'] = [r'\usepackage{sansmath}', r'\sansmath'] #Force sans-serif math mode (for axes labels)
rcParams['font.family'] = 'sans-serif' # ... for regular text
rcParams['font.sans-serif'] = ['Helvetica'] #, Avant Garde, Computer Modern Sans serif' # Choose a nice font here
rcParams['pdf.fonttype'] = 42
rcParams['ps.fonttype'] = 42

rcParams['xtick.major.pad'] = '8'
rcParams['axes.edgecolor']  = ALMOST_BLACK
rcParams['axes.labelcolor'] = ALMOST_BLACK
rcParams['lines.color']     = ALMOST_BLACK
rcParams['xtick.color']     = ALMOST_BLACK 
rcParams['ytick.color']     = ALMOST_BLACK 
rcParams['text.color']      = ALMOST_BLACK 
rcParams['lines.solid_capstyle'] = 'butt'

import matplotlib.pyplot as plt
import matplotlib as mpl

# For making custom legends:
from matplotlib.lines import Line2D

# Make a themed colormap
r,g,b = ACCENT_COLOR_1
cdict = {'red':   ((0.0,  1, 1),
                   (0.5,  r, r),
                   (1.0,  0, 0)),
         'green': ((0.0,  1, 1),
                   (0.5,  g, g),
                   (1.0,  0, 0)),
         'blue':  ((0.0,  1, 1),
                   (0.5,  b, b),
                   (1.0,  0, 0))}

ACCENT_COLOR_1_CMAP = mpl.colors.LinearSegmentedColormap('testcmap', cdict)
plt.register_cmap(cmap=ACCENT_COLOR_1_CMAP)

#plt.rc('pdf',fonttype = 1)
#plt.rc('ps',fonttype = 1)

def plot_confusion_matrix(M, labels, ax, cmap=plt.cm.Blues, rng=None):
    """ Plot a confusion matrix on supplied axes. 
    
        Inputs:
        M - (KxK) array-like confusion/mixing matrix
        labels - K-dim vector of string labels
        ax - matplotlib axes object to be drawn upon
        cmap - (optional) mpl-compatible colormap 

        Returns:
        matplotlib pcolor results

        Notes:
        Add colorbar with...
    
        >>> # M, labels both previous defined... 
        >>> fig, ax = plt.subplots()
        >>> cm = plot_confusion_matrix(M, labels, ax)
        >>> fig.colorbar(cm)
    """ 
    if rng is None:
        min_value = M.min()
        max_value = M.max()
    else:
        min_value, max_value = rng

    #if max_value < 1.0:
    #    max_value = 1.0 # matrix is normalized 

    heatmap = ax.pcolor(M, cmap=cmap)
    ax.set_xticks(np.arange(M.shape[0])+0.5, minor=False)
    ax.set_yticks(np.arange(M.shape[1])+0.5, minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    ax.set_xticklabels(labels, minor=False) # add rotation=int to rotate labels
    ax.set_yticklabels(labels, minor=False)
    ax.set_aspect('equal', adjustable='box')  
    ax.xaxis.set_label_position('top')
    heatmap.set_clim(vmin=min_value,vmax=max_value)
    print min_value, max_value

    return heatmap
    

def color_bp(bp, color):
    ''' Helper function for making prettier boxplots '''
    c = np.array(color) # * 0.5
    c = tuple(c)

    for x in bp['boxes']:
        plt.setp(x, color=c)
        x.set_facecolor(color)
    for x in bp['medians']:
        plt.setp(x, color='w')
    for x in bp['whiskers']:
        plt.setp(x, color=c)
    for x in bp['fliers']:
        plt.setp(x, color=c)
    for x in bp['caps']:
        plt.setp(x, color=c)


def adjust_spines(ax, spines):
    """ From http://matplotlib.org/examples/pylab_examples/spine_placement_demo.html """ 
    for loc, spine in ax.spines.items():
        if loc in spines:
            spine.set_position(('outward', 10))  # outward by 10 points
            spine.set_smart_bounds(True)
        else:
            spine.set_color('none')  # don't draw spine

    # turn off ticks where there is no spine
    if 'left' in spines:
        ax.yaxis.set_ticks_position('left')
    else:
        # no yaxis ticks
        ax.yaxis.set_ticks([])

    if 'bottom' in spines:
        ax.xaxis.set_ticks_position('bottom')
    else:
        # no xaxis ticks
        ax.xaxis.set_ticks([])


def hide_right_top_axis(ax):
    """ Remove the top and right axis """ 
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)


def finalize(ax, fontsize=LABEL_SIZE, labelpad=7):
    """ Make fonts bigger for publication """ 
    ax.tick_params(direction='out') 
    hide_right_top_axis(ax)
    ax.yaxis.label.set_size(fontsize)
    ax.xaxis.label.set_size(fontsize)
    ax.tick_params(axis='both', which='major', labelsize=fontsize, pad=labelpad)

