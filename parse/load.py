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
    assistant_professors = load_assistant_profs(faculty_fp, school_info, ranking, year_start, year_stop)
    return split_faculty_by_year(assistant_professors, year_start, year_stop, year_step)


def load_assistant_profs(faculty_fp, school_info, ranking='pi_rescaled', year_start=1970, year_stop=2012):
    """ Return a list of the assistant professors """
    assistant_professors = []
    for f in parse_faculty_records(faculty_fp, school_info, ranking):
        year = f.first_asst_job_year
        if (year is not None and                          # We know their start year
            year >= year_start and                        # It's in the range we want
            year < year_stop and 
            f.phd_location in school_info and             # Their PhD location is in-sample
            f.first_asst_job_location in school_info and  # Their hiring location is in-sample
            f.num_asst_jobs == f.num_asst_jobs_kd):       # It's clear which is the first gig
            assistant_professors.append(f)
    return assistant_professors


def split_faculty_by_year(faculty, year_start, year_stop, year_step=1):
    """ Similar to load_hires_by_year, but instead it takes in a list
        of faculty and splits into candidate/job pools. """ 
    year_range = np.arange(year_start, year_stop)
    num_steps = len(year_range)
    candidate_pools = [[] for year in xrange(num_steps)]
    job_pools = [[] for year in xrange(num_steps)]
    job_ranks = [[] for year in xrange(num_steps)]

    for f in faculty:
        year = f.first_asst_job_year
        if year >= year_start and year < year_stop:
            i = np.where(year_range == year)[0]
            job_pools[i].append(f.first_asst_job_location)
            job_ranks[i].append(f.first_asst_job_rank)
            candidate_pools[i].append((f, f.phd_rank))
        
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



def convert_faculty_list_to_df(faculty, discipline=None):
    data = []
    fields = ['facultyName', 'first_asst_job_location', 'first_asst_job_year',
             'has_postdoc', 'sex', 'num_asst_jobs', 'num_asst_jobs_kd', 
             'phd_location', 'phd_year', 'place']
    
    for person in faculty:
        person_data = [person[f] for f in fields]
        if discipline is not None:
            person_data.append(discipline)
        data.append(person_data)
        
    if discipline is not None:
        fields.append('discipline')
        
    return pd.DataFrame(data=data, columns=fields)