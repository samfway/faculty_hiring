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
    
    def simulate_hiring(self, candidates, positions, school_info, **kwargs):
        """ All candidates have an equal chance of being hired to each job """ 
        random_candidates = np.random.permutation(candidates)
        return zip(random_candidates, positions)


# -------------------
# ``BEST-FIRST" MODEL 
# -------------------
class BestFirstModel:
    def __init__(self):
        pass

    def simulate_hiring(self, candidates, positions, school_info, **kwargs):
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
        ranking = kwargs.get('ranking', 'pi_inv')
        worst_ranking = school_info['UNKNOWN'][ranking]

        # Populate list of available candidates
        candidate_pool = []
        noise = NOISE_LEVEL * np.random.randn(len(candidates))
        for i, f in enumerate(candidates:
            place, year = f.phd()
            try:
                rank = school_info[place][ranking]
            except:
                rank = worst_ranking
            candidate_pool.append((rank+noise[i], f))

        # Populate list of open jobs
        job_pool = []
        noise = 0.1 * np.random.randn(len(positions))
        for i, s in enumerate(positions):
            try:
                rank = school_info[s][ranking]
            except:
                rank = worst_ranking
            job_pool.append((rank+noise[i], s))

        # Sort both lists and zip them together:
        # Highest ranked candidate goes to the highest ranked job.
        job_pool.sort()
        candidate_pool.sort()
        sorted_jobs = [j[1] for j in job_pool]
        sorted_pool = [c[1] for c in candidate_pool]

        return zip(sorted_pool, sorted_jobs)


#--------------------
# STEP FUNCTION MODEL 
#--------------------
class StepFunctionModel
    def __init__(self):
        pass

    def simulate_hiring(self, candidates, positions, school_info, **kwargs):
        """ Simulate faculty hiring under the step function model.
            This model is essentially the configuration model but only for 
            candidates ranked at least as high as the institution making 
            the hire. 

            This null model captures the imposed ranking structure
            from the minimum violations ranking scheme, which is that
            schools want to avoid violations whenever possible.

            If ranking is pi_inv (inverse of PI ranking)... 
            setting `power' equal to 0, means that all positions are equally likely to be
            filled first. Setting power to 1 means that positions will be chosen with
            probability proportional to the inverse of their rank. The larger the power,
            the more strictly the hiring order resembles the ranks. 
        """
        ranking = kwargs.get('ranking', 'pi_inv')
        power = kwargs.get('power', 1)

        worst_ranking = school_info['UNKNOWN'][ranking]
        num_jobs = len(positions)
        num_candidates = len(candidates)
        
        # Populate list of available candidates
        candidate_pool = []
        # Use noise to preallocate ranks and break ties
        candidate_ranks = NOISE_LEVEL * np.random.randn(num_candidates)
        for i, f in enumerate(candidates):
            place, year = f.phd()
            try:
                rank = school_info[place][ranking]
            except:
                rank = worst_ranking
            candidate_ranks[i] += rank
        candidate_pool = zip(candidates, candidate_ranks)
        remaining_candidates = len(candidate_pool)

        # Populate list of open jobs
        job_ranks = NOISE_LEVEL * np.random.randn(num_jobs)
        for i, s in enumerate(positions):
            try:
                rank = school_info[s][ranking]
            except:
                rank = worst_ranking
            job_ranks[i] += rank

        job_ranks = array(job_ranks) ** power
        job_ranks /= job_ranks.sum()  # make probability

        # Match candidates to jobs
        for j in xrange(num_jobs):
            # Select job to fill
            job_ind = choice(xrange(num_jobs), p=job_ranks)
            job_rank = job_ranks[job_ind]  # how much probability mass taken out?
            job_ranks /= (1.-job_rank)  # renormalize
            job_ranks[job_ind] = 0.  # mark as unavailable

            # Match candidate to job
            # Select all of the candidates from a school at least as good as the job
            cand_p = np.array([1 if cand_rank >= job_rank else 1e-9 
                               for (c, c_rank) in candidate_pool])
            cand_p /= cand_p.sum()
            cand_ind = choice(xrange(remaining_candidates), p=cand_p)

            # Log the hire
            hires.append((candidate_pool[cand_ind], positions[job_ind])
            
            # Remove the candidate from the pool
            del candidate_pool[cand_ind]
            remaining_candidates -= 1 
    
        return hires
