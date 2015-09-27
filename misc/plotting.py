#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"

""" Functions to plot a confusion matrix (heat map) 
"""

import numpy as np
import matplotlib.pyplot as plt


# CONSTANTS
BAR_WIDTH = 0.6
TICK_SIZE = 15
XLABEL_PAD = 10
LABEL_SIZE = 14
TITLE_SIZE = 16
LEGEND_SIZE = 12
LINE_WIDTH = 2
LIGHT_COLOR = '0.8'
DARK_COLOR = '0.2'
MALE_COLOR = np.array([0.25490196, 0.41176471, 0.88235294])
FEMALE_COLOR = np.array([1.,  0.36,  0.72])


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
    c = np.array(color) * 0.5
    c = tuple(c)

    for x in bp['boxes']:
        plt.setp(x, color=c)
        x.set_facecolor(color)
    for x in bp['medians']:
        plt.setp(x, color=c)
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

