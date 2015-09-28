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
    args.add_argument('-f', '--fac-file', help='Faculty file', required=True)
    args.add_argument('-i', '--inst-file', help='Institutions file', required=True)
    args = args.parse_args()
    return args


if __name__=="__main__":
    args = interface()
    
    inst = parse_institution_records(open(args.inst_file, 'rU'))
    candidate_pools, job_pools, year_range = load_assistant_prof_pools(open(args.fac_file, 'rU'), school_info=inst, ranking='pi_rescaled',
                                                                       year_start=1970, year_stop=2012, year_step=1)

    model = SigmoidModel()
    w0 = 10*np.random.randn(2)
    bounds = [(-100, 100), (-100, 100)]
    simulator = SimulationEngine(candidate_pools, job_pools, inst, model, power=1, prob_function='rankdiff', weights=w0, reg=10., iters=100)
    res = minimize(simulator.simulate, w0, bounds=bounds, method='Nelder-Mead')
    print res

