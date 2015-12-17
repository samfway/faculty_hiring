#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"


import argparse
import numpy as np
import cProfile
from scipy.optimize import minimize
from faculty_hiring.parse.load import load_assistant_prof_pools
from faculty_hiring.parse.institution_parser import parse_institution_records
from faculty_hiring.models.simulation_engine import SimulationEngine
from faculty_hiring.models.null_models import ConfigurationModel, BestFirstModel
from faculty_hiring.models.sigmoid_models import SigmoidModel


def interface():
    args = argparse.ArgumentParser()
    args.add_argument('-i', '--input-file', help='Optimization output file', required=True)
    args.add_argument('-n', '--top-n', help='How many values to print', default=10, type=int)
    args = args.parse_args()
    return args


if __name__=="__main__":
    args = interface()
    grab_next = False
    vals = []

    if args.top_n < 0:
        top_n = 10
    else:
        top_n = args.top_n
    N = top_n - 2
    
    for line in open(args.input_file, 'rU'):
        line = line.strip()
        if grab_next:
            found_end = '])' in line
            line = line.replace('])', '') 
            if line.startswith('x:'):
                line = line.split('array([')[1]
                temp = [float(x.strip()) for x in line.split(',') if x]
            else:
                temp += [float(x.strip()) for x in line.split('])')[0].split(',') if x]
            
            if found_end:
                grab_next = False
                vals.append((fun_val, temp))
            
        elif line.startswith('fun:'):
            grab_next = True
            fun_val = float(line.split(': ')[1])

    for i, v in enumerate(sorted(vals)):
        print v[0], '\t', ','.join([str(x) for x in v[1]])
        if i > N:
            break
        
    print 'Done!'

'''
9.87331896 -65.03930206 -44.85336366  45.78762739  15.50518665
 -53.27997179 -28.53989597] 4606.68      4606.68
  status: 2
    nfev: 268
 success: False
     fun: 4594.3971985022745
       x: array([-99.87332475, -65.03930134, -44.85336338,  45.78762597,
        15.50518481, -53.27997003, -28.53990021])
 message: 'Maximum number of iterations has been exceeded.'
     nit: 100
'''
