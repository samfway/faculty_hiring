#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"


import numpy as np
from scipy.special import expit as sigmoid
from faculty_hiring.models.sigmoid_prob_functions import *  # All prob. function definitions


class SigmoidModel:
    def __init__(self, **kwargs):
        self.prob_function_name = kwargs.get('prob_function', 'step')
        self.prob_function = prob_functions[self.prob_function_name]
        self.weights = kwargs.get('weights', default_weights[self.prob_function_name])
        self.power = kwargs.get('power', 1.0)
    

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
        self.power = kwargs.get('power', self.power)

        # Is the candidate available or not? 
        cand_available = np.ones(len(candidates))

        # Prepare job rankings (used to determine order in which jobs are filled)
        num_jobs = len(positions)
        job_ranks = np.array(position_ranks, dtype=float)
        job_p = job_ranks / job_ranks.sum()  # make probability

        # Original model, select job proportional to rank
        if self.power > 1:
            job_p = job_p ** self.power
            job_p /= job_p.sum() 

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
            cand_p /= cand_p.sum()
            cand_ind = np.random.multinomial(1, cand_p).argmax()

            # Log the hire
            hires.append((candidates[cand_ind][0], positions[job_ind]))
            
            # Remove the candidate from the pool
            cand_available[cand_ind] = 0

        return hires


''' # NOTE: Hire in order according to rank:
        sorted_jobs = np.argsort(job_p)[::-1]
        for j in xrange(num_jobs):
            # Select job to fill
            job_ind = sorted_jobs[j]
            job_rank = job_ranks[job_ind]

            # Match candidate to job
            cand_p = self.prob_function(candidates, cand_available, positions[job_ind], job_rank,
                                        school_info, self.weights, **kwargs)
            cand_ind = np.random.multinomial(1, cand_p).argmax()

            # Log the hire
            hires.append((candidates[cand_ind][0], positions[job_ind]))
            
            # Remove the candidate from the pool
            cand_available[cand_ind] = 0
'''


