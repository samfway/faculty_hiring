#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"


import networkx as nx
from numpy import array, zeros_like, mean
import scipy as sp


class Struct:
    """ Create a Python object from a dictionary of key-values """ 
    def __init__(self, **entries): 
        self.__dict__.update(entries)


def custom_cast(x, cast_types=[int, float, str]):
    """ Attempt to cast x using the specified types in the order
        in which they appear.  """ 
    for cast_func in cast_types:
        try:
            return cast_func(x)
        except ValueError:
            pass
    raise BaseException('All casts failed!')


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


def add_hires_to_network(G, hires, weight=1.0):
    """ Take list of tuples (faculty, job_location)
        and create a weighted network where the 
        weight of the edge (a,b) indicates the number of 
        graduates sent from a to b.
    """
    for f, job_place in hires:
        phd_place, phd_year = f.phd()
        add_weighted_edge(G, (phd_place, job_place), weight)


def reciprocity(G):
    ''' For every edge (u,v), check that the reciprocating edge (v,u) exists.
        Returns: fraction of edges that are reciprocated
    '''
    return sum([int(G.has_edge(v,u)) for (u,v) in G.edges_iter()]) / float(G.number_of_edges())


def mean_nb_degree(G):
    inds = G.nodes()
    mean_nb_degrees = {i:0. for i in inds}
    for i, school_i in enumerate(inds):
        for j in G.neighbors(i):
            mean_nb_degrees[i] += G.degree(j)
        mean_nb_degrees[i] /= G.degree(school_i)
    return mean(mean_nb_degrees.values())


def mean_degree(G):
    return mean(G.degrees().values())


def mean_max_geodesic(Gu):
    inds = G.nodes()
    geodesic_lengths = {i:0 for i in inds}
    for i in inds:
        # Get path lengths to all reachable nodes, will be zero for disconnected nodes
        lengths = array(nx.shortest_path_length(G, source=i).values())
        geodesic_lengths[i] = lengths.max()

    vals = array(geodesic_lengths.values())
    diameter = vals.max()
    mean_geodesic = mean(vals[vals>0])
    return mean_geodesic, diameter
    

def compute_network_stats(G, inst):
    print 'RECIP:%.5f' % reciprocity(G)
    print 'MEAN_DEGREE:%.5f' % mean_degree(G)
    print 'MEAN_NB_DEGREE:%.5f' % mean_nb_degree(G)

    Gu = G.to_undirected()
    print 'AVG_CLUSTER:%.5f' % nx.average_clustering(Gu)
    print 'DEGREE_ASSORT:%.5f' % nx.degree_assortativity_coefficient(Gu)
    print 'MEAN_GEODESIC:%.5f' % nx.average_shortest_path_length(Gu)
    mg, d = mean_max_geodesic(Gu)
    print 'MEAN_GEODESIC:%.5f' % mg
    print 'DIAMETER:%d' % int(d)

    keep = []
    for n in Gu.nodes_iter():
        if n in inst:
            Gu.node[n]['region'] = inst[n]['Region']
            keep.append(n)
    
    H = Gu.subgraph(keep)
    print 'MOD_REGION:%.5f' % (nx.attribute_assortativity_coefficient(H, 'region'))


def binomial_confidence_interval(x, n, alpha):
    """ Based on "Exact Binomial Confidence Interval for Proportions" by
        Morisette and Khorram (1998).

        The normal is often used to get confidence intervals for binomial random
        variables. This can be OK, but falls apart when p is close to 0 or 1, or
        if there aren't very many samples. In either case, we can use the exact
        binomial confidence intervals.
     """
    lower = 1./(1. + ((n-x+1.)/x)*sp.stats.distributions.f.ppf(1.-alpha/2, 2.*(n-x+1), 2.*x))
    temp = (x+1.)/(n-x)*sp.stats.distributions.f.ppf(1.-alpha/2, 2.*(x+1), 2.*(n-x))
    upper = temp / (1.+temp)
    return lower, upper
