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

    ---

    Candidate-selection functions.

    - These are all used to set the probability of selecting a candidate for 
      a particular job.

    INPUTS
    - `candidates' - candidate pool (tuples of candidates and their ranks)
    - `cand_available' - 0/1, was the person already hired?
    - `inst' - hiring institution
    - `inst_rank' - rank of the hiring institution
    - `school_info' - institution profiles 
    - `weights' - weights for model parameters
    - `**kwargs' - any additional parameters

    OUTPUS
    - `cand_p' - the probability of selecting each candidate in the pool    

    TEMPLATE
    def prob_function_...(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
        cand_p = np.empty(len(candidates), dtype=float)
        .... 
        cand_p /= cand_p.sum()
        return cand_p

    LENGEND FOR FUNCTION NAMES
    - rd: difference in rank between phd and first job (job-phd)
    - rh: rank of hiring institution
    - sf: subfield
    - gg: geography
    - pr: productivity
    - pd: has post-doctoral experience
    - gd: is female 
"""
def prob_function_step_function(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    cand_p = np.zeros(len(candidates), dtype=float)
    cand_p[np.where(cand_available)] = 1e-9
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if candidate_rank >= inst_rank:
            cand_p[i] = 1.
    cand_p /= cand_p.sum()
    return cand_p


def prob_function_sigmoid_rank_diff(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    cand_p = np.zeros(len(candidates), dtype=float)
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if cand_available[i]:
            cand_p[i] = sigmoid(weights[0] + weights[1]*(inst_rank-candidate_rank))
    cand_p /= cand_p.sum()
    return cand_p


def prob_function_sigmoid_rd_rh(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    cand_p = np.zeros(len(candidates), dtype=float)
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if cand_available[i]:
            cand_p[i] = sigmoid(np.dot(weights, [1, inst_rank-candidate_rank, inst_rank]))
    cand_p /= cand_p.sum()
    return cand_p


def prob_function_sigmoid_rd_rh_sf(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    cand_p = np.zeros(len(candidates), dtype=float)
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if cand_available[i]:
            cand_p[i] = sigmoid(np.dot(weights, [1, inst_rank-candidate_rank, inst_rank]))
    cand_p /= cand_p.sum()
    return cand_p


# Provide easy access to the functions above.
default_weights = {'step'     : None,
                   'rankdiff' : [-1.68965263, -5.94514355],
                   'rd_rh'    : [-1.68965263, -5.94514355, -2.0101010101010101]}

prob_functions = {'step'      : prob_function_step_function,
                  'rankdiff'  : prob_function_sigmoid_rank_diff,
                  'rd_rh'     : prob_function_sigmoid_rd_rh}


class SigmoidModel:
    def __init__(self, **kwargs):
        self.prob_function_name = kwargs.get('prob_function', 'step')
        self.prob_function = prob_functions[self.prob_function_name]
        self.weights = kwargs.get('weights', default_weights[self.prob_function_name])

    
    def num_weights(self):
        """ How many weights in this model? """
        return len(self.weights)


    def simulate_hiring(self, candidates, positions, position_ranks, school_info, **kwargs):
        """ Returns a list of person-place tuples (hires) """ 
        hires = []
        self.weights = kwargs.get('weights', self.weights)

        # Is the candidate available or not? 
        cand_available = np.ones(len(candidates))

        # Prepare job rankings (used to determine order in which jobs are filled)
        num_jobs = len(positions)
        job_ranks = np.array(position_ranks, dtype=float)
        job_p = job_ranks / job_ranks.sum()  # make probability

        # Match candidates to jobs
        for j in xrange(num_jobs-1):
            # Select job to fill
            job_ind = np.random.multinomial(1, job_p).argmax()
            job_rank = job_ranks[job_ind]
            job_p[job_ind] = 0.  # mark as unavailable
            job_p /= np.sum(job_p)  # renormalize

            # Match candidate to job
            cand_p = self.prob_function(candidates, cand_available, positions[job_ind], job_rank,
                                        school_info, self.weights, **kwargs)
            cand_ind = np.random.multinomial(1, cand_p).argmax()

            # Log the hire
            hires.append((candidates[cand_ind][0], positions[job_ind]))
            
            # Remove the candidate from the pool
            cand_available[cand_ind] = 0

        return hires


