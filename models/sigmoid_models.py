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


def prob_function_sigmoid_rd(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    cand_p = np.zeros(len(candidates), dtype=float)
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if cand_available[i]:
            cand_p[i] = sigmoid(weights[0] + weights[1]*(inst_rank-candidate_rank))
    cand_p /= cand_p.sum()
    return cand_p


def prob_function_sigmoid_rd_gd(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    cand_p = np.zeros(len(candidates), dtype=float)
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if cand_available[i]:
            cand_p[i] = sigmoid(np.dot(weights, [1, 
                                                 inst_rank-candidate_rank,
                                                 int(candidate.is_female)]))
    cand_p /= cand_p.sum()
    return cand_p


# ----------------------
# UNDER EVALUATION ::::: 
# ----------------------
# RANK OF HIRING INSTITUTION
def prob_function_sigmoid_rd_rh(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    cand_p = np.zeros(len(candidates), dtype=float)
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if cand_available[i]:
            cand_p[i] = sigmoid(np.dot(weights, [1, 
                                                 inst_rank-candidate_rank,
                                                 inst_rank]))
    cand_p /= cand_p.sum()
    return cand_p


# GEOGRAPHY
def prob_function_sigmoid_rd_gg(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    job_region = school_info[inst]['Region']
    cand_p = np.zeros(len(candidates), dtype=float)
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if cand_available[i]:
            cand_p[i] = sigmoid(np.dot(weights, [1, 
                                                 inst_rank-candidate_rank,
                                                 int(job_region == candidate.phd_region)]))
    cand_p /= cand_p.sum()
    return cand_p


# PRODUCTIVITY
def prob_function_sigmoid_rd_pr(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    cand_p = np.zeros(len(candidates), dtype=float)
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if cand_available[i]:
            cand_p[i] = sigmoid(np.dot(weights, [1, 
                                                 inst_rank-candidate_rank,
                                                 candidate.dblp_z]))
    cand_p /= cand_p.sum()
    return cand_p

# POSTDOC
def prob_function_sigmoid_rd_pd(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    cand_p = np.zeros(len(candidates), dtype=float)
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if cand_available[i]:
            cand_p[i] = sigmoid(np.dot(weights, [1, 
                                                 inst_rank-candidate_rank,
                                                 int(candidate.has_postdoc)]))
    cand_p /= cand_p.sum()
    return cand_p


# -------------------------------------------------------------------------------------------------------------


# PRODUCTIVITY + ??? 
# + SELF-HIRING
def prob_function_sigmoid_rd_pr_sh(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    cand_p = np.zeros(len(candidates), dtype=float)
    inst_region = school_info.get(inst, school_info['UNKNOWN'])['Region']
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if cand_available[i]:
            cand_p[i] = sigmoid(np.dot(weights, [1, 
                                                 inst_rank-candidate_rank,
                                                 candidate.dblp_z,
                                                 int(candidate.phd_region == inst_region)]))
    cand_p /= cand_p.sum()
    return cand_p


# + RH
def prob_function_sigmoid_rd_pr_rh(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    cand_p = np.zeros(len(candidates), dtype=float)
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if cand_available[i]:
            cand_p[i] = sigmoid(np.dot(weights, [1, 
                                                 inst_rank-candidate_rank,
                                                 candidate.dblp_z,
                                                 inst_rank]))
    cand_p /= cand_p.sum()
    return cand_p


# + PD
def prob_function_sigmoid_rd_pr_pd(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    cand_p = np.zeros(len(candidates), dtype=float)
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if cand_available[i]:
            cand_p[i] = sigmoid(np.dot(weights, [1, 
                                                 inst_rank-candidate_rank,
                                                 candidate.dblp_z,
                                                 int(candidate.has_postdoc)]))
    cand_p /= cand_p.sum()
    return cand_p


# + GG
def prob_function_sigmoid_rd_pr_gg(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    job_region = school_info[inst]['Region']
    cand_p = np.zeros(len(candidates), dtype=float)
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if cand_available[i]:
            cand_p[i] = sigmoid(np.dot(weights, [1, 
                                                 inst_rank-candidate_rank,
                                                 candidate.dblp_z,
                                                 int(job_region == candidate.phd_region)]))
    cand_p /= cand_p.sum()
    return cand_p


# -------------------------------------------------------------------------------------------------------------


# RD + PR + GG + ??? 
# + PD
def prob_function_sigmoid_rd_pr_gg_pd(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    job_region = school_info[inst]['Region']
    cand_p = np.zeros(len(candidates), dtype=float)
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if cand_available[i]:
            cand_p[i] = sigmoid(np.dot(weights, [1, 
                                                 inst_rank-candidate_rank,
                                                 candidate.dblp_z,
                                                 int(job_region == candidate.phd_region),
                                                 int(candidate.has_postdoc)]))
    cand_p /= cand_p.sum()
    return cand_p


# + RH
def prob_function_sigmoid_rd_pr_gg_rh(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    job_region = school_info[inst]['Region']
    cand_p = np.zeros(len(candidates), dtype=float)
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if cand_available[i]:
            cand_p[i] = sigmoid(np.dot(weights, [1, 
                                                 inst_rank-candidate_rank,
                                                 candidate.dblp_z,
                                                 int(job_region == candidate.phd_region),
                                                 inst_rank]))
    cand_p /= cand_p.sum()
    return cand_p


# -------------------------------------------------------------------------------------------------------------


# EVERYTHING *EXCEPT* GENDER (RD, RH, PD, PR, GG)
def prob_function_sigmoid_no_gd(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    job_region = school_info[inst]['Region']
    cand_p = np.zeros(len(candidates), dtype=float)
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if cand_available[i]:
            cand_p[i] = sigmoid(np.dot(weights, [1, 
                                                 inst_rank-candidate_rank,
                                                 inst_rank,
                                                 int(candidate.has_postdoc),
                                                 candidate.dblp_z,
                                                 int(job_region == candidate.phd_region)]))
    cand_p /= cand_p.sum()
    return cand_p


# EVERYTHING *INCLUDING* GENDER (RD, RH, PD, PR, GG, GD)
def prob_function_sigmoid_all(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    job_region = school_info[inst]['Region']
    cand_p = np.zeros(len(candidates), dtype=float)
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if cand_available[i]:
            cand_p[i] = sigmoid(np.dot(weights, [1, 
                                                 inst_rank-candidate_rank,
                                                 inst_rank,
                                                 int(candidate.has_postdoc),
                                                 candidate.dblp_z,
                                                 int(job_region == candidate.phd_region),
                                                 int(candidate.is_female)]))
    cand_p /= cand_p.sum()
    return cand_p


# Provide easy access to the functions above.
default_weights = {'step'           : [],
                   'rd'             : [-1.68965263, -5.94514355],
                   'rd_gd'          : [1., 1., 1.],
                   'rd_rh'          : [-1.68965263, -5.94514355, 1.],
                   'rd_gg'          : [-1.68965263, -5.94514355, 1.],
                   'rd_pr'          : [-1.68965263, -5.94514355, 1.],
                   'rd_pd'          : [-1.68965263, -5.94514355, 1.],
                   'rd_pr_sh'       : [1., 1., 1., 1.],
                   'rd_pr_rh'       : [1., 1., 1., 1.],
                   'rd_pr_pd'       : [1., 1., 1., 1.],
                   'rd_pr_gg'       : [1., 1., 1., 1.],
                   'rd_pr_gg_rh'    : [1., 1., 1., 1., 1.],
                   'rd_pr_gg_pd'    : [1., 1., 1., 1., 1.],
                   'no_gd'          : [1., 1., 1., 1., 1., 1.],
                   'all'            : [1., 1., 1., 1., 1., 1., 1.]}

prob_functions = {'step'           : prob_function_step_function,
                  'rd'             : prob_function_sigmoid_rd,
                  'rd_gd'          : prob_function_sigmoid_rd_gd,
                  'rd_rh'          : prob_function_sigmoid_rd_rh, 
                  'rd_gg'          : prob_function_sigmoid_rd_gg,
                  'rd_pr'          : prob_function_sigmoid_rd_pr,
                  'rd_pd'          : prob_function_sigmoid_rd_pd,
                  'rd_pr_sh'       : prob_function_sigmoid_rd_pr_sh,
                  'rd_pr_rh'       : prob_function_sigmoid_rd_pr_rh,
                  'rd_pr_pd'       : prob_function_sigmoid_rd_pr_pd,
                  'rd_pr_gg'       : prob_function_sigmoid_rd_pr_gg,
                  'rd_pr_gg_rh'    : prob_function_sigmoid_rd_pr_gg_rh,
                  'rd_pr_gg_pd'    : prob_function_sigmoid_rd_pr_gg_pd,
                  'no_gd'          : prob_function_sigmoid_no_gd,
                  'all'            : prob_function_sigmoid_all}     


class SigmoidModel:
    def __init__(self, **kwargs):
        self.prob_function_name = kwargs.get('prob_function', 'step')
        self.prob_function = prob_functions[self.prob_function_name]
        self.weights = kwargs.get('weights', default_weights[self.prob_function_name])

    
    def get_weights(self):
        """ Return a copy of the weights """
        return np.copy(self.weights) 


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
        for j in xrange(num_jobs):
            # Select job to fill
            job_ind = np.random.multinomial(1, job_p).argmax()
            job_rank = job_ranks[job_ind]
            job_p[job_ind] = 0.  # mark as unavailable
            job_p_sum = np.sum(job_p)
            if job_p_sum > 0.:  # jobs left?
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


