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
                 iters=10, reg=0., hiring_orders=None, hiring_probs=None, **kwargs):
        self.candidate_pools = candidate_pools
        self.job_pools = job_pools
        self.job_ranks = job_ranks
        self.school_info = school_info
        self.model = model
        self.model_args = kwargs
        self.iterations = iters
        self.regularization = reg
        self.hiring_orders = hiring_orders
        self.hiring_probs = hiring_probs
        self.num_pools = len(candidate_pools)
   
        if len(hiring_orders) != self.num_pools:
            raise ValueError('Hiring orders must be the same size as hiring pools')

        if self.hiring_orders is not None:
            self.num_orders = len(self.hiring_orders[0])
            self.pool_sizes = [len(self.hiring_orders[i][0]) for i in xrange(self.num_pools)]
            self.likelihoods = np.ones((self.num_pools, self.num_orders), dtype=np.float128)
            self.log_pr_y_ri = np.zeros(self.num_orders, dtype=np.float128)
            self.log_pr_ri = np.sum(np.log(self.hiring_probs), axis=0)

        self.num_jobs = 0.
        for job_pool in job_pools:
            self.num_jobs += len(job_pool)


    def get_model_weights(self):
        """ Return a copy of the model weights for sanity reasons """ 
        return self.model.get_weights()
    
    
    def simulate(self, weights=None, quiet=False, ranking='pi'):
        """ Simulate hiring many times under the specified model.
            The returned error is the average squared placement error
            per individual in the dataset PLUS the L2-penalty term, 
            if the model uses weights and regularization is positive. 
        """
        total_error = 0.

        if weights is not None:
            self.model.weights = weights

        if self.regularization > 0.:
            penalty = np.dot(self.model.weights[1:], self.model.weights[1:]) * self.regularization  # L2
            #penalty = np.sum(np.abs(self.model.weights[1:]) * self.regularization)  # L1
        else:
            penalty = 0.0

        for t in xrange(self.iterations):
            for i in xrange(self.num_pools):
                hires = self.model.simulate_hiring(self.candidate_pools[i],
                                                   self.job_pools[i],
                                                   self.job_ranks[i],
                                                   self.school_info,
                                                   **self.model_args)
                total_error += sse_rank_diff(hires, self.school_info, ranking)
        total_error /= (self.iterations * self.num_jobs)

        if not quiet:
            if ranking == 'pi':
                print weights, '%.2f \t %.2f' % (total_error, total_error + penalty)
            else:
                print weights, '%.6f \t %.6f' % (total_error, total_error + penalty)

        return total_error + penalty 


    def generate_network(self, weights=None, one_list=True):
        """ Generate a network (list of hires) using the 
            specified hiring model """ 
        all_hires = []

        if weights is not None:
            self.model.weights = weights

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
    
    
    def calculate_neg_likelihood(self, weights=None):
        """ Return the ***NEGATED*** likelihood of the model given the data (the hiring 
            and candidate pools). Negated because this is getting passed into a function
            minimizer, similar to the placement error calculation. 
        """
        if weights is not None:
            self.model.weights = weights

        likelihood = np.float128(0.)
        self.likelihoods[:] = 1.

        for i in xrange(self.num_pools):
            F = np.zeros((self.pool_sizes[i], self.pool_sizes[i]), dtype=float)
            for j, job in enumerate(self.job_pools[i]):
                self.model.score_candidates(F[j,:], self.candidate_pools[i], job, 
                                            self.job_ranks[i][j], self.school_info)

            """ For each hiring sequence, calculate the likelihood, building up from the "final" hire.
                That is, start with the last school to make a hire. There was only one candidate remaining
                in the pool, so they chose them with probability 1. Go to the second-to-last. They chose 
                from the last two candidates, and picked their hiring with probability equal to
                    
                    f(actual) / [f(actual) + f(not_hired)]. 

                Build up this list until all hires have been accounted for. 
            """
            for j in xrange(self.num_orders):
                available = [] 
                for k in xrange(F.shape[0]):
                    current = self.hiring_orders[i][j][-(k+1)]
                    available.append(current)
                    self.likelihoods[i,j] *= np.float128(F[current][current] / np.sum(F[current][available]))

        for j in xrange(self.num_orders):
            ri_term = np.float128(1e100) 
            for i in xrange(self.num_pools):
                ri_term *= np.float128(self.likelihoods[i,j] * 1e100) * np.float128(self.hiring_probs[i][j] * 1e100)
            likelihood += ri_term

        print weights, likelihood,'\t', likelihood

        return -likelihood


    def calculate_neg_log_likelihood(self, weights=None, verbose=True):
        if weights is not None:
            self.model.weights = weights

        log_likelihood = 0.0

        # log(Pr(Y,Ri)) = log(Pr(Y|Ri)) + log(Pr(R))
        self.log_pr_y_ri[:] = self.log_pr_ri

        for i in xrange(self.num_pools):
            F = np.zeros((self.pool_sizes[i], self.pool_sizes[i]), dtype=float)
            # Precompute all F scores
            for j, job in enumerate(self.job_pools[i]):
                self.model.score_candidates(F[j,:], self.candidate_pools[i], job, 
                                            self.job_ranks[i][j], self.school_info)

            for j in xrange(self.num_orders):
                available = [] 
                for k in xrange(F.shape[0]):
                    current = self.hiring_orders[i][j][-(k+1)]
                    available.append(current)
                    self.log_pr_y_ri[j] += np.log(F[current][current] / np.sum(F[current][available])) 

        # log of sum trick
        log_likelihood = self.log_pr_y_ri[0] + np.log(np.sum(np.exp(self.log_pr_y_ri - self.log_pr_y_ri[0])))

        if self.regularization > 0.:
            penalty = np.dot(self.model.weights[1:], self.model.weights[1:]) * self.regularization  # L2
        else:
            penalty = 0.0
      
        if verbose:
            print weights, -log_likelihood + penalty, '\t', -log_likelihood + penalty

        return -log_likelihood + penalty

