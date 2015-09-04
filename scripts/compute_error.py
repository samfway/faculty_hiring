#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"


import argparse
import numpy as np
from faculty_hiring.parse.load import load_hires_by_year
from faculty_hiring.parse.institution_parser import parse_institution_records
from faculty_hiring.models.simulation_engine import SimulationEngine
from faculty_hiring.models.null_models import ConfigurationModel, BestFirstModel, StepFunctionModel


def interface():
    args = argparse.ArgumentParser()
    args.add_argument('-f', '--fac-file', help='Faculty file')
    args.add_argument('-i', '--inst-file', help='Institutions file')
    args = args.parse_args()
    return args


if __name__=="__main__":
    args = interface()
    

    inst = parse_institution_records(open(args.inst_file, 'rU'))
    candidate_pools, job_pools, year_range = load_hires_by_year(open(args.fac_file, 'rU'))

    model = ConfigurationModel()
    simulator = SimulationEngine(candidate_pools, job_pools, inst, model)
    print 'Configuration:', simulator.simulate()

    model = BestFirstModel()
    simulator = SimulationEngine(candidate_pools, job_pools, inst, model)
    print 'BestFirst:', simulator.simulate()

    model = StepFunctionModel()
    simulator = SimulationEngine(candidate_pools, job_pools, inst, model)
    print 'Step (pow=1):', simulator.simulate()

    model = StepFunctionModel()
    simulator = SimulationEngine(candidate_pools, job_pools, inst, model, power=2)
    print 'Step (pow=2):', simulator.simulate()

