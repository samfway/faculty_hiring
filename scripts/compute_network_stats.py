#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"


import argparse
import numpy as np
import networkx as nx
import cProfile
from scipy.optimize import minimize
from faculty_hiring.parse.load import load_assistant_prof_pools
from faculty_hiring.parse.institution_parser import parse_institution_records
from faculty_hiring.models.simulation_engine import SimulationEngine
from faculty_hiring.models.null_models import ConfigurationModel, BestFirstModel
from faculty_hiring.models.sigmoid_models import SigmoidModel


def interface():
    args = argparse.ArgumentParser()
    args.add_argument('-f', '--fac-file', help='Faculty file', required=True)
    args.add_argument('-i', '--inst-file', help='Institutions file', required=True)
    args.add_argument('-o', '--output-file', help='Output file', required=True)
    args.add_argument('-p', '--prob-function', help='Candidate probability/matching function', required=True)
    args.add_argument('-n', '--num-iters', help='Number of iterations to est. error', default=100, type=int)
    args.add_argument('-w', '--weights', help='Model parameters (as comma-separated string)')
    args.add_argument('--actual', help='Compute network stats for the empirical network', action='store_true')
    args = args.parse_args()
    return args


def add_weighted_edge(G, vertex_pair, weight=1.0):
    """ Wrapper to facilitate making weighted, directed
        networks.  If an edge exists between the vertex_pair,
        the weight is incremented by the supplied value.
        If the edge does not already exist, it is created
        and initialized with the supplied weight value.
    """
    s, d = vertex_pair  # unpack
    if G.has_edge(s, d):
        G[s][d]['weight'] += weight
    else:
        G.add_edge(s,d, weight=weight)
        

def network_from_hiring_list(hiring_list):
    """ Create a weighted, directed network from a list of hires """ 
    G = nx.DiGraph()
    for person, place in hiring_list:
        if person.phd_location is None:
            print person.facultyName
        add_weighted_edge(G, (person.phd_location, place))
    return G


def weighted_fraction_reciprocated(G, weight='weight'):
    """ Computes the total number of reciprocated edges in the network """ 
    unrecip = 0.
    total = 0.

    for s,d in G.edges_iter():
        sd_weight = G[s][d][weight]
        total += sd_weight

        if (d,s) in G.edges():
            ds_weight = G[d][s][weight]
        else:
            ds_weight = 0.

        # Unreciprocated is the difference
        unrecip += sd_weight - ds_weight

    return (total-unrecip)/total


def unweighted_fraction_reciprocated(G, weight='weight'):
    """ Computes the total number of reciprocated edges in the network...
        ...ignoring weight (number of people exchanged)!
    """ 
    recip = 0.
    total = G.number_of_edges()

    for s,d in G.edges_iter():
        if (d,s) in G.edges():
            recip += 1
            
    return recip/total


def fraction_self_loops(G, weight='weight'):
    """ How many self-loops are there? """ 
    loops = 0.
    total = 0.

    for s,d in G.edges_iter():
        total += G[s][d][weight]
        if s == d:
            loops += G[s][d][weight]
            
    return loops/total


def fraction_same_region(G, school_info, weight='weight'):
    """ Computes the total number of reciprocated edges in the network...
        ...ignoring weight (number of people exchanged)!
    """
    same = 0.
    total = 0.

    for s,d in G.edges_iter():
        if s in school_info and d in school_info:
            s_region = school_info[s]['Region']
            d_region = school_info[d]['Region']
            total += G[s][d][weight]
            if s_region == d_region:
                same += G[s][d][weight]
            
    return same/total


def compute_network_stats(hires, school_info, output_fp):
    """ Given a list of hires, compute some stats, and write
        them out to the output file.
    """ 
    G = network_from_hiring_list(hires)
    Gu = G.to_undirected()
    Gcc = max(nx.connected_component_subgraphs(Gu), key=len)

    # Size of the giant component
    output.write('%s:%d\n' % ('SIZE_GC', Gcc.number_of_nodes()))
    # Mean geodesic path length
    output.write('%s:%f\n' % ('MEAN_GEODESIC', nx.average_shortest_path_length(Gcc)))
    # Clustering component
    output.write('%s:%f\n' % ('AVG_CLUSTER', nx.average_clustering(Gcc)))
    # Fraction of reciprocated edges
    output.write('%s:%f\n' % ('W_RECIP', weighted_fraction_reciprocated(G)))
    output.write('%s:%f\n' % ('UW_RECIP', unweighted_fraction_reciprocated(G)))
    # Fraction of self-loops
    output.write('%s:%f\n' % ('SELF_HIRES', fraction_self_loops(G)))
    # Fraction of in same region
    output.write('%s:%f\n' % ('SAME_REGION', fraction_same_region(G, school_info)))


if __name__=="__main__":
    args = interface()
    output = open(args.output_file, 'w')
    
    # Load the data
    inst = parse_institution_records(open(args.inst_file, 'rU'))
    candidate_pools, job_pools, job_ranks, year_range = load_assistant_prof_pools(open(args.fac_file), 
                                                                                  school_info=inst, 
                                                                                  ranking='pi_rescaled',
                                                                                  year_start=1970, 
                                                                                  year_stop=2012, 
                                                                                  year_step=1)

    # Compute actual stats, if requested.
    if args.actual:
        actual_hires = []
        for pool in candidate_pools:
            for person, rank in pool:
                actual_hires.append((person, person.first_asst_job_location))
        compute_network_stats(actual_hires, inst, output)
        output.close()
        exit()

    # Otherwise, set up the model + simulator
    if args.prob_function == 'flat':
        # 'flat' could very easily be a prob_function in the sigmoid model -- this is faster
        model = ConfigurationModel()
    else:
        model = SigmoidModel(prob_function=args.prob_function)
    simulator = SimulationEngine(candidate_pools, job_pools, job_ranks, inst, model, iters=1, reg=0)
    if model.num_weights() > 0:
        w = np.array([float(x) for x in args.weights.split(',')])
        if len(w) != model.num_weights():
            print len(w), model.num_weights()
            raise ValueError('Invalid number of weights/model parameters!')
    else:
        w = None

    # Run however many iterations and compute stats
    for i in xrange(args.num_iters):
        hires = simulator.generate_network(weights=w, one_list=True)
        compute_network_stats(hires, inst, output)

    output.close()
