#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"


import numpy as np
from scipy.special import expit as sigmoid


""" All models expect similar inputs and return output in the same format.

    Inputs:
        `candidates' - a list of faculty profile objects (parse/faculty_parser.py)
        `positions' - a list of insitution names with open jobs
        `school_info' - a dictionary of institution profiles (parse/institution_parser.py)
        `ranking' - which ranking to use

    Returns:
        A list of tuples, denoting candidate+position pairs. This is the list of hires made.
"""
class SigmoidModel:
    def __init__(self):
        self.prob_functions = {'step':prob_function_step_function,
                               'rankdiff':prob_function_sigmoid_rank_diff}

    def simulate_hiring(self, candidates, positions, school_info, **kwargs):
        """ Returns a list of person-place tuples (hires) """ 
        hires = []
        ranking = kwargs.get('ranking', 'pi_rescaled')
        power = kwargs.get('power', 1)
        f = kwargs.get('prob_function', 'step')
        prob_function = self.prob_functions[f] 

        worst_ranking = school_info['UNKNOWN'][ranking]
        num_jobs = len(positions)
        num_candidates = len(candidates)
        
        # Populate list of available candidates
        candidate_ranks = np.empty(num_candidates, dtype=float)
        for i, f in enumerate(candidates):
            place, year = f.phd()
            try:
                candidate_ranks[i] = school_info[place][ranking]
            except:
                candidate_ranks[i] = worst_ranking
        candidate_pool = zip(candidates, candidate_ranks)
        remaining_candidates = len(candidate_pool)

        # Populate list of open jobs
        job_ranks = np.zeros(num_jobs, dtype=float)
        for i, s in enumerate(positions):
            try:
                job_ranks[i] = school_info[s][ranking]
            except:
                job_ranks[i] = worst_ranking

        job_p = job_ranks.copy() ** power
        job_p /= job_p.sum()  # make probability

        # Match candidates to jobs
        for j in xrange(num_jobs-1):
            # Select job to fill
            job_ind = np.random.multinomial(1, job_p).argmax()
            job_rank = job_ranks[job_ind]
            job_p[job_ind] = 0.  # mark as unavailable
            job_p /= np.sum(job_p)  # renormalize

            # Match candidate to job
            # Select all of the candidates from a school at least as good as the job
            cand_p = prob_function(candidate_pool, positions[job_ind], job_rank, school_info, **kwargs)
            cand_ind = np.random.multinomial(1, cand_p).argmax()

            # Log the hire
            hires.append((candidate_pool[cand_ind][0], positions[job_ind]))
            
            # Remove the candidate from the pool
            del candidate_pool[cand_ind]
            remaining_candidates -= 1 

        job_ind 
    
        return hires


""" Candidate-selection functions.

    - These are all used to set the probability of selecting a candidate for 
      a particular job.

    INPUTS
    - `candidates' - candidate pool (tuples of candidates and their ranks)
    - `inst' - hiring institution
    - `inst_rank' - rank of the hiring institution
    - `school_info' - institution profiles 
    - `**kwargs' - any additional parameters

    OUTPUS
    - `cand_p' - the probability of selecting each candidate in the pool    

    TEMPLATE
    def prob_function_...(candidates, inst, inst_rank, school_info, **kwargs):
        cand_p = np.empty(len(candidates), dtype=float)
        .... 
        cand_p /= cand_p.sum()
        return cand_p
"""
def prob_function_step_function(candidates, inst, inst_rank, school_info, **kwargs):
    cand_p = np.empty(len(candidates), dtype=float)
    cand_p.fill(1e-9)
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if candidate_rank >= inst_rank:
            cand_p[i] = 1.
    cand_p /= cand_p.sum()
    return cand_p


def prob_function_sigmoid_rank_diff(candidates, inst, inst_rank, school_info, **kwargs):
    cand_p = np.empty(len(candidates), dtype=float)
    weights = kwargs.get('weights', np.array([1., 1.]))

    for i, (candidate, candidate_rank) in enumerate(candidates):
        cand_p[i] = sigmoid(weights[0] + weights[1]*(inst_rank-candidate_rank))

    cand_p /= cand_p.sum()
    return cand_p

