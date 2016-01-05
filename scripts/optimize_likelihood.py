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
from faculty_hiring.misc.hiring_orders import load_hiring_order_set

def interface():
    args = argparse.ArgumentParser()
    args.add_argument('-f', '--fac-file', help='Faculty file', required=True)
    args.add_argument('-i', '--inst-file', help='Institutions file', required=True)
    args.add_argument('-p', '--prob-function', help='Candidate probability/matching function', required=True)
    args.add_argument('-o', '--hiring-orders-file', help='Hiring order set file (pkl)', required=True)
    args.add_argument('-s', '--num-steps', help='Number of steps allowed', default=100, type=int)
    args.add_argument('-r', '--reg', help='Regularization amount', default=0., type=float)
    args.add_argument('-v', '--validation', help='Years to hold out', default='')
    args.add_argument('-t', '--tolerance', help='Optimization tolerance', default=10.0, type=float)
    args = args.parse_args()
    return args


if __name__=="__main__":
    args = interface()
    
    # Load in all data
    inst = parse_institution_records(open(args.inst_file, 'rU'))
    candidate_pools, job_pools, job_ranks, year_range = load_assistant_prof_pools(open(args.fac_file), 
                                                                                  school_info=inst, 
                                                                                  ranking='pi_rescaled',
                                                                                  year_start=1970, 
                                                                                  year_stop=2012, 
                                                                                  year_step=1)
    hiring_orders, hiring_probs = load_hiring_order_set(args.hiring_orders_file)

    # If specified years are to be left out
    if args.validation:  
        hold_out = [int(year) for year in args.validation.split(',')]
        training_candidates, training_jobs, training_job_ranks = [], [], []
        training_orders, training_probs = [], []
        for i, year in enumerate(year_range):
            if year not in hold_out:
                training_candidates.append(candidate_pools[i])
                training_jobs.append(job_pools[i])
                training_job_ranks.append(job_ranks[i])
                training_orders.append(hiring_orders[i])
                training_probs.append(hiring_probs[i])
        # Overwrite originals:
        candidate_pools, job_pools, job_ranks = training_candidates, training_jobs, training_job_ranks
        hiring_orders, hiring_probs = training_orders, training_probs
    
    # Which model?
    model = SigmoidModel(prob_function=args.prob_function)

    # Find a starting place
    simulator = SimulationEngine(candidate_pools, job_pools, job_ranks, inst, model, power=1, reg=args.reg,
                                 hiring_orders=hiring_orders, hiring_probs=hiring_probs)
    w0 = None
    best_neg_likelihood = np.inf
    for i in xrange(10): #args.num_steps):
        #wtemp = 100*np.random.randn(model.num_weights())  # ~[-100, 100]
        wtemp = 100*(np.random.random(model.num_weights()) - 0.5)  # ~[-100, 100]
        temp = simulator.calculate_neg_log_likelihood(weights=wtemp)
        if temp < best_neg_likelihood:
            w0 = wtemp.copy()
            best_neg_likelihood = temp

    # Optimize from there
    simulator = SimulationEngine(candidate_pools, job_pools, job_ranks, inst, model, power=1, reg=args.reg, 
                                 hiring_orders=hiring_orders, hiring_probs=hiring_probs)
    opt = {'maxiter':args.num_steps}
    method = 'Nelder-Mead'

    res = minimize(simulator.calculate_neg_log_likelihood, w0, method=method, options=opt, tol=args.tolerance)
    print res

