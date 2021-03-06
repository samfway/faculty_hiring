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


    def num_weights(self):
        return 0  # There should really be a HiringModel class... To-do. 
    

    def simulate_hiring(self, candidates, positions, position_ranks, school_info, **kwargs):
        """ All candidates have an equal chance of being hired to each job """ 
        candidates_without_ranks = np.random.permutation([f[0] for f in candidates])
        return zip(candidates_without_ranks, positions)


# -------------------
# ``BEST-FIRST" MODEL 
# -------------------
class BestFirstModel:
    def __init__(self):
        pass

    
    def num_weights(self):
        return 0


    def simulate_hiring(self, candidates, positions, position_ranks, school_info, **kwargs):
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
        # Populate list of available candidates
        candidate_pool = []
        noise = NOISE_LEVEL * np.random.randn(len(candidates))
        for i, f in enumerate(candidates):
            # candidates are tuples (faculty_profile, phd_rank)
            candidate_pool.append((f[1]+noise[i], f[0]))

        # Populate list of open jobs
        job_pool = []
        noise = 0.1 * np.random.randn(len(positions))
        for i, s in enumerate(positions):
            job_pool.append((position_ranks[i]+noise[i], s))

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

