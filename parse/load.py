#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"


import os
import numpy as np
from faculty_hiring.parse.faculty_parser import parse_faculty_records
from faculty_hiring.parse.dblp import parse_dblp_publications
from faculty_hiring.parse.google_scholar import parse_gs_publications
try:
   import cPickle as pickle
except:
   import pickle


GS_PKL = 'GSP_%s.pkl'
DBLP_PKL = 'DBLP_%s.pkl'


def load_assistant_prof_pools(faculty_fp, school_info=None, ranking='pi_rescaled',
                              year_start=1970, year_stop=2012, year_step=1):
    """ Load all assistant professors, format as pools for simulation models """ 
    assistant_professors = load_assistant_profs(faculty_fp, school_info, ranking)
    return split_faculty_by_year(assistant_professors, year_start, year_stop, year_step)


def load_assistant_profs(faculty_fp, school_info=None, ranking='pi_rescaled'):
    """ Return a list of the assistant professors """
    assistant_professors = []
    for f in parse_faculty_records(faculty_fp, school_info, ranking):
        place, year = f.first_asst_prof()
        if year is not None and place is not None:
            assistant_professors.append(f)
    return assistant_professors


def split_faculty_by_year(faculty, year_start, year_stop, year_step=1):
    """ Similar to load_hires_by_year, but instead it takes in a list
        of faculty and splits into candidate/job pools. """ 
    year_range = np.arange(year_start, year_stop, year_step)
    num_steps = len(year_range)
    candidate_pools = [[] for year in xrange(num_steps - 1)]
    job_pools = [[] for year in xrange(num_steps - 1)]
    job_ranks = [[] for year in xrange(num_steps - 1)]
    num_professors = len(faculty)

    fac = [(f.first_asst_job_year, f.first_asst_job_location, f) for f in faculty]
    fac.sort()

    YEAR = 0; PLACE = 1 ; FACULTY = 2

    ptr = 0  # Index over the list of faculty
    for i in xrange(num_steps-1):  # Index over the time bins
        start = year_range[i]
        stop = year_range[i+1]
        while ptr < num_professors:
            if fac[ptr][YEAR] < stop: 
                if fac[ptr][YEAR] >= start:
                    job_pools[i].append(fac[ptr][PLACE])
                    job_ranks[i].append(fac[ptr][FACULTY].first_asst_job_rank)
                    candidate_pools[i].append((fac[ptr][FACULTY], f.phd_rank))
                ptr += 1
            else:
                break  # Advance to next year range

    return candidate_pools, job_pools, job_ranks, year_range


def load_all_publications(faculty, dblp_dir=None, gs_dir=None):
    """ Load all publication data into faculty records """ 
    for f in faculty:
        if gs_dir and 'gs' in f:
            filename = os.path.join(gs_dir, GS_PKL % f['gs'])
            with open(filename,'rb') as fp:
                f['gs_pubs'] = pickle.load(fp)
                f['gs_stats'] = pickle.load(fp)
                
        if dblp_dir and 'dblp' in f:
            filename = os.path.join(dblp_dir, DBLP_PKL % f['dblp'])
            with open(filename,'rb') as fp:
                f['dblp_pubs'] = pickle.load(fp)
                f['dblp_stats'] = pickle.load(fp)


