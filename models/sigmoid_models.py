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
class SigmoidModel:
    def __init__(self):
        self.prob_functions = {'step':prob_function_step_function}

    def simulate_hiring(self, candidates, positions, school_info, **kwargs):
        hires = []
        ranking = kwargs.get('ranking', 'pi_inv')
        power = kwargs.get('power', 1)
        f = kwargs.get('prob_function', 'step')
        prob_function = self.prob_functions[f] 

        worst_ranking = school_info['UNKNOWN'][ranking]
        num_jobs = len(positions)
        num_candidates = len(candidates)
        
        # Populate list of available candidates
        candidate_pool = []
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
                rank = school_info[s][ranking]
            except:
                rank = worst_ranking
            job_ranks[i] = rank

        job_ranks = np.array(job_ranks) ** power
        job_ranks /= job_ranks.sum()  # make probability

        # Match candidates to jobs
        for j in xrange(num_jobs):
            # Select job to fill
            job_ind = np.random.choice(xrange(num_jobs), p=job_ranks)
            job_rank = job_ranks[job_ind]  # how much probability mass taken out?
            if job_rank != 1.:
                job_ranks /= (1.-job_rank)  # renormalize
            job_ranks[job_ind] = 0.  # mark as unavailable

            # Match candidate to job
            # Select all of the candidates from a school at least as good as the job
            cand_p = prob_function(candidate_pool, positions[job_ind], job_rank, school_info, **kwargs)
            cand_ind = np.random.choice(xrange(remaining_candidates), p=cand_p)

            # Log the hire
            hires.append((candidate_pool[cand_ind][0], positions[job_ind]))
            
            # Remove the candidate from the pool
            del candidate_pool[cand_ind]
            remaining_candidates -= 1 
    
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
        cand_p = np.zeros(len(candidates), dtype=float)
        ... 
        return cand_p
"""
def prob_function_step_function(candidates, inst, inst_rank, school_info, **kwargs):
    cand_p = np.empty(len(candidates), dtype=float)
    cand_p.fill(1e-9)
    for i, (candidate, candidate_rank) in enumerate(candidates):
        if candidate_rank >= inst_rank:
            cand_p[i] += 1.
    cand_p /= cand_p.sum()
    return cand_p

