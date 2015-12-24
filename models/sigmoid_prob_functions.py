#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"


import numpy as np
from scipy.special import expit as sigmoid


def prob_function_step_function(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    cand_p = np.zeros(len(candidates), dtype=float)
    cand_p[np.where(cand_available)] = 1e-9
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if candidate_rank >= inst_rank:
            cand_p[i] = 1.
    #cand_p /= cand_p.sum()
    return cand_p


def prob_function_sigmoid_rd(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    cand_p = np.zeros(len(candidates), dtype=float)
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if cand_available[i]:
            cand_p[i] = sigmoid(weights[0] + weights[1]*(inst_rank-candidate_rank))
    #cand_p /= cand_p.sum()
    return cand_p


def prob_function_sigmoid_gg(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    job_region = school_info[inst]['Region']
    cand_p = np.zeros(len(candidates), dtype=float)
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if cand_available[i]:
            cand_p[i] = sigmoid(np.dot(weights, [1, 
                                                 int(job_region == candidate.phd_region)]))
    #cand_p /= cand_p.sum()
    return cand_p


def prob_function_sigmoid_pr(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    cand_p = np.zeros(len(candidates), dtype=float)
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if cand_available[i]:
            cand_p[i] = sigmoid(np.dot(weights, [1, 
                                                 candidate.dblp_z]))
    #cand_p /= cand_p.sum()
    return cand_p


def prob_function_sigmoid_pd(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    cand_p = np.zeros(len(candidates), dtype=float)
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if cand_available[i]:
            cand_p[i] = sigmoid(np.dot(weights, [1, 
                                                 int(candidate.has_postdoc)]))
    #cand_p /= cand_p.sum()
    return cand_p


def prob_function_sigmoid_rd_gd(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    cand_p = np.zeros(len(candidates), dtype=float)
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if cand_available[i]:
            cand_p[i] = sigmoid(np.dot(weights, [1, 
                                                 inst_rank-candidate_rank,
                                                 int(candidate.is_female)]))
    #cand_p /= cand_p.sum()
    return cand_p


def prob_function_sigmoid_rd_rh(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    cand_p = np.zeros(len(candidates), dtype=float)
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if cand_available[i]:
            cand_p[i] = sigmoid(np.dot(weights, [1, 
                                                 inst_rank-candidate_rank,
                                                 inst_rank]))
    #cand_p /= cand_p.sum()
    return cand_p


def prob_function_sigmoid_rd_gg(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    job_region = school_info[inst]['Region']
    cand_p = np.zeros(len(candidates), dtype=float)
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if cand_available[i]:
            cand_p[i] = sigmoid(np.dot(weights, [1, 
                                                 inst_rank-candidate_rank,
                                                 int(job_region == candidate.phd_region)]))
    #cand_p /= cand_p.sum()
    return cand_p


def prob_function_sigmoid_rd_pr(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    cand_p = np.zeros(len(candidates), dtype=float)
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if cand_available[i]:
            cand_p[i] = sigmoid(np.dot(weights, [1, 
                                                 inst_rank-candidate_rank,
                                                 candidate.dblp_z]))
    #cand_p /= cand_p.sum()
    return cand_p


def prob_function_sigmoid_rd_pd(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    cand_p = np.zeros(len(candidates), dtype=float)
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if cand_available[i]:
            cand_p[i] = sigmoid(np.dot(weights, [1, 
                                                 inst_rank-candidate_rank,
                                                 int(candidate.has_postdoc)]))
    #cand_p /= cand_p.sum()
    return cand_p


def prob_function_sigmoid_rd_pr_rh(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    cand_p = np.zeros(len(candidates), dtype=float)
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if cand_available[i]:
            cand_p[i] = sigmoid(np.dot(weights, [1, 
                                                 inst_rank-candidate_rank,
                                                 candidate.dblp_z,
                                                 inst_rank]))
    #cand_p /= cand_p.sum()
    return cand_p


def prob_function_sigmoid_rd_pr_pd(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    cand_p = np.zeros(len(candidates), dtype=float)
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if cand_available[i]:
            cand_p[i] = sigmoid(np.dot(weights, [1, 
                                                 inst_rank-candidate_rank,
                                                 candidate.dblp_z,
                                                 int(candidate.has_postdoc)]))
    #cand_p /= cand_p.sum()
    return cand_p


def prob_function_sigmoid_rd_pr_gg(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    job_region = school_info[inst]['Region']
    cand_p = np.zeros(len(candidates), dtype=float)
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if cand_available[i]:
            cand_p[i] = sigmoid(np.dot(weights, [1, 
                                                 inst_rank-candidate_rank,
                                                 candidate.dblp_z,
                                                 int(job_region == candidate.phd_region)]))
    #cand_p /= cand_p.sum()
    return cand_p


def prob_function_sigmoid_rd_pr_rh_gg(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    job_region = school_info[inst]['Region']
    cand_p = np.zeros(len(candidates), dtype=float)
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if cand_available[i]:
            cand_p[i] = sigmoid(np.dot(weights, [1, 
                                                 inst_rank-candidate_rank,
                                                 candidate.dblp_z,
                                                 inst_rank, 
                                                 int(job_region == candidate.phd_region)]))
    #cand_p /= cand_p.sum()
    return cand_p


def prob_function_sigmoid_rd_pr_rh_pd(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    cand_p = np.zeros(len(candidates), dtype=float)
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if cand_available[i]:
            cand_p[i] = sigmoid(np.dot(weights, [1, 
                                                 inst_rank-candidate_rank,
                                                 candidate.dblp_z,
                                                 inst_rank, 
                                                 int(candidate.has_postdoc)]))
    #cand_p /= cand_p.sum()
    return cand_p


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
    #cand_p /= cand_p.sum()
    return cand_p


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
    #cand_p /= cand_p.sum()
    return cand_p


def prob_function_sigmoid_no_gd(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    """ Probability function for everything except gender """
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
    #cand_p /= cand_p.sum()
    return cand_p


def prob_function_sigmoid_all(candidates, cand_available, inst, inst_rank, school_info, weights, **kwargs):
    """ Probability function for *EVERYTHING* """ 
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
    #cand_p /= cand_p.sum()
    return cand_p


# Provide easy access to the functions above.
default_weights = {'step'           : [],
                   'rd'             : [1, 1],
                   'gg'             : [1, 1],
                   'pr'             : [1, 1],
                   'pd'             : [1, 1],
                   'rd_gd'          : [1., 1., 1.],
                   'rd_rh'          : [1., 1., 1.],
                   'rd_gg'          : [1., 1., 1.],
                   'rd_pr'          : [1., 1., 1.],
                   'rd_pd'          : [1., 1., 1.],
                   'rd_pr_rh'       : [1., 1., 1.],
                   'rd_pr_pd'       : [1., 1., 1., 1.],
                   'rd_pr_gg'       : [1., 1., 1., 1.],
                   'rd_pr_gg_rh'    : [1., 1., 1., 1., 1.],
                   'rd_pr_gg_pd'    : [1., 1., 1., 1., 1.],
                   'rd_pr_rh_gg'    : [1., 1., 1., 1., 1.],
                   'rd_pr_rh_pd'    : [1., 1., 1., 1., 1.],
                   'no_gd'          : [1., 1., 1., 1., 1., 1.],
                   'all'            : [1., 1., 1., 1., 1., 1., 1.]}

prob_functions = {'step'           : prob_function_step_function,
                  'rd'             : prob_function_sigmoid_rd,
                  'gg'             : prob_function_sigmoid_gg,
                  'pr'             : prob_function_sigmoid_pr,
                  'pd'             : prob_function_sigmoid_pd,
                  'rd_gd'          : prob_function_sigmoid_rd_gd,
                  'rd_rh'          : prob_function_sigmoid_rd_rh, 
                  'rd_gg'          : prob_function_sigmoid_rd_gg,
                  'rd_pr'          : prob_function_sigmoid_rd_pr,
                  'rd_pd'          : prob_function_sigmoid_rd_pd,
                  'rd_pr_rh'       : prob_function_sigmoid_rd_pr_rh,
                  'rd_pr_pd'       : prob_function_sigmoid_rd_pr_pd,
                  'rd_pr_gg'       : prob_function_sigmoid_rd_pr_gg,
                  'rd_pr_gg_rh'    : prob_function_sigmoid_rd_pr_gg_rh,
                  'rd_pr_gg_pd'    : prob_function_sigmoid_rd_pr_gg_pd,
                  'rd_pr_rh_gg'    : prob_function_sigmoid_rd_pr_rh_gg,
                  'rd_pr_rh_pd'    : prob_function_sigmoid_rd_pr_rh_pd,
                  'no_gd'          : prob_function_sigmoid_no_gd,
                  'all'            : prob_function_sigmoid_all}     

