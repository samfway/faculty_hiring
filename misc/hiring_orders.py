#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"


import numpy as np
import cPickle as pickle


def prepare_hiring_orders(job_pools, job_ranks, num_orders):
    """ Prepare a number of sample hiring orders for estimating the
        likelihood of the data, given our model, parameters, etc.

        Returns:
          - A list of numpy matrices (|h|*num_orders), where |h| is the size of the
            job_pool for each year.
          - A list of lists containing the probability of each hiring order.
    """
    hiring_orders = [np.zeros((num_orders, len(pool)), dtype=int) for pool in job_pools]
    hiring_probs = [np.zeros(num_orders, dtype=float) for pool in job_pools]

    # Populate the orders and the probabilities
    for i, pool in enumerate(job_pools):
        job_probs = np.array(job_ranks[i], dtype=float)
        job_probs /= job_probs.sum() 
        num_jobs = len(job_probs)

        for j in xrange(num_orders):
            prob = 1.
            job_p = job_probs.copy()
            for k in xrange(num_jobs-1):
                job_p /= job_p.sum()
                selected = np.random.multinomial(1, job_p).argmax()
                hiring_orders[i][j][k] = selected
                prob *= job_p[selected]  # update order probability
                job_p[selected] = 0.  # mark as unavailable
            selected = job_p.argmax()
            hiring_orders[i][j][num_jobs-1] = selected  # last available 
            hiring_probs[i][j] = prob

        #print ' --> '.join([pool[ind] for ind in hiring_orders[i][0]]) + '\n'
    
    return hiring_orders, hiring_probs


def create_hiring_order_set(output_file, job_pools, job_ranks, num_orders):
    """ Create and write out a hiring set to file """
    hiring_orders, hiring_probs = prepare_hiring_orders(job_pools, job_ranks, num_orders)
    hiring_dict = {'orders':hiring_orders, 'probs':hiring_probs}
    with open(output_file, 'wb') as handle:
        pickle.dump(hiring_dict, handle)
    return hiring_orders, hiring_probs


def load_hiring_order_set(input_file):
    """ Load a previously created hiring set from file """ 
    with open(input_file, 'rb') as handle:
        hiring_dict  = pickle.load(handle)
    hiring_orders = hiring_dict['orders']
    hiring_probs = hiring_dict['probs']
    return hiring_orders, hiring_probs
    
