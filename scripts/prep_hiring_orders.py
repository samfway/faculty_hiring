#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"


import argparse
import numpy as np
from faculty_hiring.misc.hiring_orders import prepare_hiring_orders, create_hiring_order_set
from faculty_hiring.parse.load import load_assistant_prof_pools
from faculty_hiring.parse.institution_parser import parse_institution_records


def interface():
    args = argparse.ArgumentParser()
    args.add_argument('-f', '--fac-file', help='Faculty file', required=True)
    args.add_argument('-i', '--inst-file', help='Institutions file', required=True)
    args.add_argument('-n', '--num-samples', help='Number of samples', default=10, type=int)
    args.add_argument('-o', '--output-file', help='Output (pickle) file', required=True)
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


    create_hiring_order_set(args.output_file, job_pools, job_ranks, args.num_samples)
    print 'Done!'
