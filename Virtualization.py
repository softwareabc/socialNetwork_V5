#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-05-17 11:45:49
# @Author  : NSSimacer Ng
# @Email   : wuxiaoqiang1020@gmail.com
# @Link    : nssimacer.github.io
# @Version : 1.0


import igraph
import networkx as nx
from flask import Flask, render_template, request, make_response
import json

import Calculation as c
import DataProcess as dp

# 声明全局变量
data = {}
G_igraph = igraph.Graph()
G_nx = nx.Graph()
nodes_vector = []
aca_graph = ()

# 创建 Flask 应用
app = Flask(__name__)


@app.route('/')
def index():
    '''
    应用起始页面
    '''

    return render_template('main.html')


@app.route('/centrality/<int(min=1, max=5):req_id>', methods=['POST', 'GET'])
def top_students(req_id):
    '''
    处理名人推荐、学院搜索

    ----------
    parameter
      req_id 请求编号

    return
      渲染的模板
    '''

    global G_igraph, G_nx, nodes_vector, aca_graph, data

    paramas = request.form

    if req_id == 1:  # 请求全校学生节点中心度值

        ig_list = c.centrality_calculation_by_igraph(G_igraph)
        nx_list = c.centrality_calculation_by_networkx(G_nx)

        data = ig_list + nx_list  # 根据请求返回需要的对应格式的数据

        return make_response(json.dumps(data))

    elif req_id == 2:  # 请求某个院学生节点中心度值

        aca_id = int(paramas['search'])

        ig_list = c.centrality_calculation_by_igraph(aca_graph[aca_id])
        nx_list = c.centrality_calculation_by_networkx(
            nx.DiGraph(aca_graph[aca_id].get_edgelist()))

        data = ig_list + nx_list  # 根据请求返回需要的对应格式的数据

        return make_response(json.dumps(data))

    elif req_id == 3:  # 请求某个学生节点中心度值

        stu_id = int(paramas['search'])

        ig_list = c.centrality_calculation_by_igraph(G_igraph)
        nx_list = c.centrality_calculation_by_networkx(G_nx)

        data = ig_list + nx_list  # 根据请求返回需要的对应格式的数据

        stu_centrality = {}

        for centrality in data:  # 取出所有计算该节点 centrality 算法中对应的值

            centrality_key = centrality.keys()[0]
            centrality_value = centrality.values()[0][stu_id]

            stu_centrality[centrality_key] = centrality_value

        return make_response(json.dumps(stu_centrality))


@app.route('/page2/<int(min=1, max=5):req_id>', methods=['POST', 'GET'])
def closest_group(req_id):
    '''
    处理学院聚集度

    ----------
    parameter
      req_id 请求编号

    return
      渲染的模板
    '''

    global G_igraph, G_nx, nodes_vector, aca_graph, data

    if req_id == 1:  # 跳转到群体团结度页面

        return render_template('page2.html')

    if req_id == 2:  # 选择两个学院

        aca1_id = int(request.form['acaId1'])
        aca2_id = int(request.form['acaId2'])

        ig_list = c.centrality_calculation_by_igraph(aca_graph[aca1_id])
        nx_list = c.centrality_calculation_by_networkx(
            nx.DiGraph(aca_graph[aca1_id].get_edgelist()))

        aca1_coefficient = c.cluster_coefficient_calculation(
            nx.DiGraph(
                aca_graph[aca1_id].
                get_edgelist()).to_undirected(reciprocal=False))

        # 根据请求返回需要的对应格式的数据
        aca1_data = ig_list + nx_list +\
            [{'ClusterCoefficient': aca1_coefficient}]

        ig_list = c.centrality_calculation_by_igraph(aca_graph[aca2_id])
        nx_list = c.centrality_calculation_by_networkx(
            nx.DiGraph(aca_graph[aca2_id].get_edgelist()))

        aca2_coefficient = c.cluster_coefficient_calculation(
            nx.DiGraph(
                aca_graph[aca2_id].
                get_edgelist()).to_undirected(reciprocal=False))

        # 根据请求返回需要的对应格式的数据
        aca2_data = ig_list + nx_list +\
            [{'ClusterCoefficient': aca2_coefficient}]

        return render_template(
            'test_page2.html',
            aca1_data=json.dumps(aca1_data),
            aca2_data=json.dumps(aca2_data))


def main():

    global G_igraph, G_nx, nodes_vector, aca_graph

    G_igraph, G_nx, nodes_vector = dp.generate_data()

    aca_graph = dp.separate_data_by_academy(nodes_vector, G_igraph)


if __name__ == '__main__':

    main()

    app.run(debug=True)
