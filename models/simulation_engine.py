#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"


import numpy as np
from faculty_hiring.misc.scoring import sse_rank_diff


class SimulationEngine:
    def __init__(self, candidate_pools, job_pools, job_ranks, school_info, model, 
                 iters=10, reg=0., **kwargs):
        self.candidate_pools = candidate_pools
        self.job_pools = job_pools
        self.job_ranks = job_ranks
        self.school_info = school_info
        self.model = model
        self.model_args = kwargs
        self.iterations = iters
        self.regularization = reg
        self.num_pools = len(candidate_pools)

        self.num_jobs = 0.
        for job_pool in job_pools:
            self.num_jobs += len(job_pool)


    def get_model_weights(self):
        """ Return a copy of the model weights for sanity reasons """ 
        return self.model.get_weights()
    
    
    def simulate(self, weights=None, quiet=False):
        """ Simulate hiring many times under the specified model.
            The returned error is the average squared placement error
            per individual in the dataset PLUS the L2-penalty term, 
            if the model uses weights and regularization is positive. 
        """
        total_error = 0.

        if weights is not None:
            self.model.weights = weights

        if self.regularization > 0.:
            l2_penalty = np.dot(self.model.weights[1:], self.model.weights[1:]) * self.regularization
        else:
            l2_penalty = 0.0

        for t in xrange(self.iterations):
            for i in xrange(self.num_pools):
                hires = self.model.simulate_hiring(self.candidate_pools[i],
                                                   self.job_pools[i],
                                                   self.job_ranks[i],
                                                   self.school_info,
                                                   **self.model_args)
                total_error += sse_rank_diff(hires, self.school_info, 'pi')
        total_error /= (self.iterations * self.num_jobs)

        if not quiet:
            print weights, '%.2f \t %.2f' % (total_error, total_error + l2_penalty)

        return total_error + l2_penalty 


    def generate_network(self, one_list=True):
        """ Generate a network (list of hires) using the 
            specified hiring model """ 
        all_hires = []
        for i in xrange(self.num_pools):
            hires = self.model.simulate_hiring(self.candidate_pools[i],
                                                    self.job_pools[i], 
                                                    self.job_ranks[i],
                                                    self.school_info,
                                                    **self.model_args)
            if one_list:
                all_hires += hires
            else:
                all_hires.append(hires)

        return all_hires
    
