#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"


import numpy as np
from faculty_hiring.parse.faculty_parser import parse_faculty_records


def load_hires_by_year(faculty_fp, year_start=1970, year_stop=2012, year_step=1):
    """ Get lists of faculty and hiring institutions by year (range of years)
        
        Returns two lists of lists:
          - candidate_pools: all faculty profiles hired in each hiring period.
          - job_pools: all institutions making hires during those years.
    """ 
    year_range = np.arange(year_start, year_stop, year_step) 
    num_steps = len(year_range)
    candidate_pools = [[] for year in xrange(num_steps - 1)]
    job_pools = [[] for year in xrange(num_steps - 1)]

    assistant_professors = []
    for f in parse_faculty_records(faculty_fp):
        place, year = f.first_asst_prof()
        if year is not None and year >= year_start and year <= year_stop:
            assistant_professors.append((year, place, f))
    YEAR = 0 ; PLACE = 1 ; FACULTY = 2
    assistant_professors.sort()
    num_professors = len(assistant_professors)

    ptr = 0
    for i in xrange(num_steps-1):
        stop = year_range[i+1]
        while ptr < num_professors:
            if assistant_professors[ptr][YEAR] < stop:
                job_pools[i].append(assistant_professors[ptr][PLACE])
                candidate_pools[i].append(assistant_professors[ptr][FACULTY])
                ptr += 1
            else:
                break  # Advance to next year range

    return candidate_pools, job_pools, year_range
