#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-04-25 20:44:43
# @Author  : NSSimacer Ng
# @Email   : wuxiaoqiang1020@gmail.com
# @Link    : nssimacer.github.io
# @Version : 1.0


import igraph
import networkx as nx
import numpy as np
import random


def group_centrality(matrix):

    N = len(matrix)
    vertex = random.randint(0, N - 30)
    number = random.randint(10, 30)
    selectver = []
    remainver = []
    selectver.append(vertex)
    for i in xrange(1, number):
        flag = False
        # flag4 = True
        for j in xrange(N):
            if matrix[vertex][j] == 1:
                if j not in selectver:
                    selectver.append(j)

            if len(selectver) == number:
                flag = True
                break
        if flag:
            break
        vertex = selectver[i]

    for i in xrange(N):
        flag1 = True
        for j in xrange(len(selectver)):
            if i == selectver[j]:
                flag1 = False
                break
        if flag1:
            remainver.append(i)

    sum = 0
    for i in xrange(len(remainver)):
        t1 = remainver[i]
        flag2 = False
        for j in xrange(len(selectver)):
            t2 = selectver[j]
            if matrix[t1][t2] == 1:
                flag2 = True
                break
        if flag2:
            sum = sum + 1

    return [{'GroupDegree': [sum, selectver]}]


def regular_equivalence(matrix):

    N = len(matrix)

    eigen_value, eigen_vectors = np.linalg.eig(matrix)

    alpha = round(1.0 / eigen_value[0], 1)

    matrix = (np.eye(N, N) - np.dot(matrix, alpha)).I

    array = matrix.tolist()

    for i in xrange(len(array)):

        for j in xrange(len(array[i])):

            array[i][j] = round(array[i][j], 4)

    return array


def structural_equivalence(matrix):

    result = []

    row_num = len(matrix)

    adj = [0] * row_num

    for i in xrange(row_num):

        col_num = len(matrix[i])

        for j in xrange(col_num):

            adj[i] += matrix[i][j]

        adj[i] /= row_num

    for i in xrange(row_num):

        col_num = len(matrix[i])

        for j in xrange(col_num):

            sig = 0.0
            v1 = 0.0
            v2 = 0.0
            v = 0.0

            for k in xrange(row_num):

                sig += (matrix[i][k] - adj[i]) * (matrix[j][k] - adj[j])
                v1 += (matrix[i][k] - adj[i]) ** 2
                v2 += (matrix[j][k] - adj[j]) ** 2

            v = (v1 * v2) ** 0.5

            tmp = 0

            if v != 0.0:

                tmp = sig / v

            result.append((i, j, tmp))

    array = [[0 for col in xrange(col_num)] for row in xrange(row_num)]

    for item in result:

        array[item[0]][item[1]] = round(item[2], 4)

    return array


def cluster_coefficient_calculation(G):
    ''''
    使用 networkx 计算 Cluster Coefficient
    '''

    c_c = nx.average_clustering(G)

    return round(c_c, 4)


def centrality_calculation_by_networkx(G):
    '''
    使用 networkx 计算 Centrality
    '''

    d_c = nx.degree_centrality(G)

    k_z = nx.katz_centrality(
        G=G,
        alpha=0.3,
        beta=0.3,
        max_iter=1000,
        tol=1.0e-6,
        nstart=None,
        normalized=True)

    # 归一化，每个元素除以集合中最大元素
    d_c = [round(1.0 * item / max(d_c), 4) for item in d_c]
    k_z = [round(1.0 * item / max(k_z), 4) for item in k_z]

    nx_list = [{'Degree': d_c}, {'Katz': k_z}]

    return nx_list


def centrality_calculation_by_igraph(G):
    '''
    使用 igraph 计算 Centrality
    '''

    e_c = G.evcent(directed=True, scale=True)
    b_c = G.betweenness(vertices=None, directed=True, cutoff=2)
    c_c = G.closeness(vertices=None, mode=igraph.ALL, cutoff=2)
    p_r = G.pagerank(vertices=None, directed=True, damping=0.85,
                     implementation='prpack', niter=1000, eps=0.001)

    # 归一化，每个元素除以集合中最大元素
    e_c = [round(item / max(e_c), 4) for item in e_c]
    b_c = [round(item / max(b_c), 4) for item in b_c]
    c_c = [round(item / max(c_c), 4) for item in c_c]
    p_r = [round(item / max(p_r), 4) for item in p_r]

    ig_list = [{'Eigenvector': e_c}, {'Betweenness': b_c},
               {'Closeness': c_c}, {'PageRank': p_r}]

    return ig_list


def main():

    G = igraph.Graph.Erdos_Renyi(n=400, p=0.3)
    centrality_calculation_by_igraph(G)

    print 'Done i'

    G = nx.DiGraph(G.get_edgelist())
    centrality_calculation_by_networkx(G)

    print 'Done nx'

    G = G.to_undirected(reciprocal=False)

    matrix = nx.to_numpy_matrix(G)

    structural_equivalence(matrix.tolist())

    print 'Done se'

    regular_equivalence(matrix)

    print 'Done re'

if __name__ == '__main__':

    main()
