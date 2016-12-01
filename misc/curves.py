#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"


from scipy import optimize
import numpy as np


def piecewise_linear1(x, x0, y0, k1, k2):
    """ Lines must pass through the same point """
    return y0 + k1*x + k2*np.maximum(0, x-x0)


def piecewise_linear2(x, x0, m1, b1, m2, b2):
    """ Lines don't need to pass through the same point """ 
    return (x<=x0) * (m1*x + b1) + \
            (x>x0) * (m2*x + b2)
    

def fit_piecewise_linear(x, y, function, params):
    p, e = optimize.curve_fit(function, x, y, p0=params)
    return p   


def unpack_params(p):
    params = {}
    if len(p) == 4:
        #piecewise_linear1
        params['tstar'] = p[0]
        params['b1'] = p[1]
        params['m1'] = p[2]
        params['m2'] = p[2] + p[3]
    elif len(p) == 5:
        #piecewise_linear2
        params['tstar'] = p[0]
        params['m1'] = p[1]
        params['b1'] = p[2]
        params['m2'] = p[3]
        params['b2'] = p[4]
    else:
        raise Exception('Invalid parameters list')
    return params
