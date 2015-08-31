#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"

""" How to score a hiring simulation
"""

def sse_rank_diff(hires, inst, worst_rank, rank='pi'):
    """ Compute the sum of squares rank difference error """
    total = 0.0
    for f, place in hires:
        actual_place, year = f.first_asst_prof()
            
        actual_rank = worst_rank
        if actual_place in inst:
            actual_rank = inst[actual_place][rank]
                
        sim_rank = worst_rank
        if place in inst:
            sim_rank = inst[place][rank]
           
        total += (actual_rank-sim_rank)**2
    return total


def rank_and_error(hires, inst, worst_rank, rank='pi'):
    """ Split into rank and error lists
        
        Returns three lists:
            - phd_ranks. Ranks of the placing institution
            - job_ranks. Ranks of the hiring institution (actual hire)
            - errors. Squared difference between actual and simulated placement ranks

     """ 
    phd_ranks = []
    job_ranks = []
    errors = []

    for f, place in hires:
        actual_place, year = f.first_asst_prof()
        phd_place, phd_year = f.phd()
            
        actual_rank = worst_rank
        if actual_place in inst:
            actual_rank = inst[actual_place][rank]
                
        sim_rank = worst_rank
        if place in inst:
            sim_rank = inst[place][rank]
           
        phd_rank = worst_rank
        if phd_place in inst:
            phd_rank = inst[phd_place][rank]
           
        phd_ranks.append(phd_rank)
        job_ranks.append(actual_rank)
        errors.append(actual_rank-sim_rank)

    return phd_ranks, job_ranks, errors

def places_and_errors(hires, inst, worst_rank, rank='pi'):
    """ Split out phd place and placement error
    """ 
    places = []
    errors = []

    for f, place in hires:
        actual_place, year = f.first_asst_prof()
        phd_place, phd_year = f.phd()
        
        actual_rank = worst_rank
        if actual_place in inst:
            actual_rank = inst[actual_place][rank]
                
        sim_rank = worst_rank
        if place in inst:
            sim_rank = inst[place][rank]
           
        places.append(phd_place) 
        errors.append(actual_rank-sim_rank)
    
    return zip(places, errors)


def diffs_and_errors(hires, inst, worst_rank, rank='pi'):
    """ Split out phd place and placement error
    """ 
    diffs = []
    errors = []

    for f, place in hires:
        actual_place, year = f.first_asst_prof()
        phd_place, phd_year = f.phd()
        
        actual_rank = worst_rank
        if actual_place in inst:
            actual_rank = inst[actual_place][rank]
                
        sim_rank = worst_rank
        if place in inst:
            sim_rank = inst[place][rank]
           
        phd_rank = worst_rank
        if phd_place in inst:
            phd_rank = inst[phd_place][rank]
           
        diffs.append(phd_rank-actual_rank) 
        errors.append(actual_rank-sim_rank)
    
    return zip(diffs, errors)
