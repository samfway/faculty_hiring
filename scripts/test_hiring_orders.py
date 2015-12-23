#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"


import argparse
import numpy as np
from faculty_hiring.misc.hiring_orders import load_hiring_order_set
from faculty_hiring.parse.load import load_assistant_prof_pools
from faculty_hiring.parse.institution_parser import parse_institution_records


def interface():
    args = argparse.ArgumentParser()
    args.add_argument('-f', '--fac-file', help='Faculty file', required=True)
    args.add_argument('-i', '--inst-file', help='Institutions file', required=True)
    args.add_argument('-s', '--orders-file', help='Input (pickle) file', required=True)
    args = args.parse_args()
    return args


if __name__=="__main__":
    args = interface()
    
    inst = parse_institution_records(open(args.inst_file, 'rU'))
    candidate_pools, job_pools, job_ranks, year_range = load_assistant_prof_pools(open(args.fac_file), 
                                                                                  school_info=inst, 
                                                                                  ranking='pi_rescaled',
                                                                                  year_start=1970, 
                                                                                  year_stop=2012, 
                                                                                  year_step=1)


    hiring_orders, hiring_probs = load_hiring_order_set(args.orders_file)
    if len(hiring_orders) != len(job_pools):
        raise ValueError('Incorrect number of pools!')

    for i, pool in enumerate(job_pools):
        pool_size = len(pool)
        if len(pool) != len(hiring_orders[i][0]):
            raise ValueError('Incorrect pool size')
        if np.sum(hiring_orders[i][0]) != np.sum(np.arange(pool_size)):
            raise ValueError('Ordering doesnt seem legit') 

    print 'Everything checks out!'
