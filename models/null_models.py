#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"


import numpy as np


""" All models expect similar inputs and return output in the same format.

    Inputs:
        `candidates' - a list of faculty profile objects (parse/faculty_parser.py)
        `positions' - a list of insitution names with open jobs
        `school_info' - a dictionary of institution profiles (parse/institution_parser.py)
        `ranking' - which ranking to use

    Returns:
        A list of tuples, denoting candidate+position pairs. This is the list of hires made.
"""
NOISE_LEVEL = 1e-6

# -------------------
# CONFIGURATION MODEL 
# -------------------
class ConfigurationModel:
    def __init__(self):
        pass
    
    def simulate_hiring(self, candidates, positions, school_info, **kwargs):
        """ All candidates have an equal chance of being hired to each job """ 
        random_candidates = np.random.permutation(candidates)
        return zip(random_candidates, positions)


# -------------------
# ``BEST-FIRST" MODEL 
# -------------------
class BestFirstModel:
    def __init__(self):
        pass

    def simulate_hiring(self, candidates, positions, school_info, **kwargs):
        """ Simulate faculty hiring under the 'best-first' model.
            Under this model, the highest-ranked job is filled first,
            and they blindly pick the candidate from the highest-ranked
            school (regardless of gender, productivity, etc).

            Assumptions: 
            Unranked schools are effectively tied for last place
            A small amount of noise is added to their ranking to serve as a tie-breaker. 
            Haven't heard of that school? We'll assume the hiring committee hasn't either, 
            and you get no bonus points for prestige.
        """
        ranking = kwargs.get('ranking', 'pi_inv')
        worst_ranking = school_info['UNKNOWN'][ranking]

        # Populate list of available candidates
        candidate_pool = []
        noise = NOISE_LEVEL * np.random.randn(len(candidates))
        for i, f in enumerate(candidates):
            place, year = f.phd()
            try:
                rank = school_info[place][ranking]
            except:
                rank = worst_ranking
            candidate_pool.append((rank+noise[i], f))

        # Populate list of open jobs
        job_pool = []
        noise = 0.1 * np.random.randn(len(positions))
        for i, s in enumerate(positions):
            try:
                rank = school_info[s][ranking]
            except:
                rank = worst_ranking
            job_pool.append((rank+noise[i], s))

        # Sort both lists and zip them together:
        # Highest ranked candidate goes to the highest ranked job.
        job_pool.sort()
        candidate_pool.sort()
        sorted_jobs = [j[1] for j in job_pool]
        sorted_pool = [c[1] for c in candidate_pool]

        return zip(sorted_pool, sorted_jobs)

#-----------------------------------------------------------------
# STEP FUNCTION MODEL 
# is now part of sigmoid_models.py. Just set prob_function='step'. 
#-----------------------------------------------------------------

