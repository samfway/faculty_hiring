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


def get_best_from_file(input_file, how_many):
    """ Get the best function vals and corresponding weights from file """ 
    vals = []
    grab_next = False
    for line in open(input_file, 'rU'):
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
    
    return sorted(vals)[:how_many]


if __name__=="__main__":
    args = interface()

    if args.top_n < 0:
        top_n = 10
    else:
        top_n = args.top_n
    N = top_n - 2
    
    for i, v in enumerate(get_best_from_file(args.input_file, top_n)):
        print v[0], '\t', ','.join([str(x) for x in v[1]])
    print 'Done!'

