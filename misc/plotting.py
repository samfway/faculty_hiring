#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"

""" Functions to plot a confusion matrix (heat map) 
"""

from numpy import arange, array
import matplotlib.pyplot as plt


# CONSTANTS
BAR_WIDTH = 0.6
TICK_SIZE = 15
XLABEL_PAD = 10
LABEL_SIZE = 14
TITLE_SIZE = 16
LEGEND_SIZE = 12
LINE_WIDTH = 2


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
    ax.set_xticks(arange(M.shape[0])+0.5, minor=False)
    ax.set_yticks(arange(M.shape[1])+0.5, minor=False)
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
    c = array(color) * 0.5
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
