#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-05-30 01:39:11
# @Author  : NSSimacer Ng
# @Email   : wuxiaoqiang1020@gmail.com
# @Link    : nssimacer.github.io
# @Version : 1.0


import networkx as nx
import igraph
import random
import matplotlib.pyplot as plt


def graph_json(G):
    '''
    图的信息

    -----------
    parameter
      G networkx 图

    return
      图的节点、边信息
    '''

    nodes = G.nodes()
    edges = G.edges()

    nodes_list = []
    edges_list = []

    for node in nodes:

        nodes_list.append({'id': str(node + 1)})

    for edge in edges:

        edges_list.append({'source': edge[0] + 1, 'target': edge[1] + 1})

    return {'nodes': nodes_list, 'edges': edges_list}


def separate_data_by_academy(nodes_vector, graph):
    '''
    分割子图

    -----------
    parameter
      nodes_vector 图中对应节点的 vector 属性
      graph 待分割的图

    return
      分割后的子图
    '''

    aca0_list = []
    aca1_list = []

    for index, node_vector in enumerate(nodes_vector):

        if node_vector[2] == 0:  # 按学院划分子图

            aca0_list.append(index)

        else:

            aca1_list.append(index)

    aca0_sub_igraph = graph.subgraph(aca0_list)
    aca1_sub_igraph = graph.subgraph(aca1_list)

    return aca0_sub_igraph, aca1_sub_igraph


def generate_data():
    '''
    产生计算所需数据

    ------------
    return
      G_igraph 用于 igraph 计算的图
      G_nx 用于 networkx 计算的图
      nodes_vector 图中对应节点的 vector 属性
    '''

    # 由 igraph 生成的随机图
    G_igraph = igraph.Graph.Erdos_Renyi(n=200, p=0.08)

    # 用于 networkx 计算的有向图
    G_nx = nx.DiGraph(G_igraph.get_edgelist())

    # 存储图中对应节点的 vector
    nodes_vector = []
    node_vector = [0] * 4

    # 初始化节点 vector 信息
    for i in xrange(200):

        node_vector[0] = random.randint(0, 1)
        node_vector[1] = random.randint(20, 28)

        ''''
        if i < 100:  # id 前 100 的为一个学院，后 100 的为另外一个学院

            node_vector[2] = 1
        '''

        node_vector[2] = random.randint(0, 1)  # 学院学生数不一定是相同的
        node_vector[3] = random.randint(0, 1)

        nodes_vector.append(node_vector)

        node_vector = [0] * 4  # 清零 vector，否则所有 vector 都是相同的

    return G_igraph, G_nx, nodes_vector


def main():

    G_igraph, G_nx, nodes_vector = generate_data()

    aca0, aca1 = separate_data_by_academy(nodes_vector, G_nx)

    print aca0.nodes()
    print aca1.nodes()

    plt.subplot(121)
    nx.draw_networkx(
        G=aca0,
        pos=nx.spring_layout(aca0),
        with_labels=True,
        node_color='g',
        edge_color='b',
        alpha=1)

    plt.axis('off')

    plt.subplot(122)
    nx.draw_networkx(
        G=aca1,
        pos=nx.spring_layout(aca1),
        with_labels=True,
        node_color='g',
        edge_color='b',
        alpha=1)

    plt.axis('off')
    plt.show()


if __name__ == '__main__':

    main()
