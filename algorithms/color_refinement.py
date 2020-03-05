from utils.graph import *
from utils.graph_io import load_graph, write_dot
from utils.utils import *
import math
import os
import random
import time


def create_color_map(graph: "Graph"):
    color_map = dict()

    for v in graph.vertices:
        # v.cur_color = v.degree
        color_map[v.label] = v.degree

    return color_map


def clone_color_map(color_map: "dict"):
    new_color_map = dict()

    for key, value in color_map.items():
        new_color_map[key] = value

    return new_color_map


def create_single_color_partition(color_map: "dict"):
    partition_union = dict()

    for v, color in color_map.items():
        if color not in partition_union:
            partition_union[color] = [v]
        else:
            partition_union[color].append(v)

    return partition_union


def create_color_partition(color_map: "dict"):
    vertex_num = len(color_map)

    partition_a = dict()
    partition_b = dict()
    partition_union = dict()

    for v, color in color_map.items():
        if color not in partition_union:
            partition_union[color] = [v]
        else:
            partition_union[color].append(v)

        if v < vertex_num // 2:
            if color not in partition_a:
                partition_a[color] = [v]
            else:
                partition_a[color].append(v)
        else:
            if color not in partition_b:
                partition_b[color] = [v]
            else:
                partition_b[color].append(v)

    return partition_a, partition_b, partition_union


def color_refinement_with_initial_color(graph: "Graph", color_map: "dict"):
    max_color = 0

    for v in graph.vertices:
        # v.cur_color = v.degree
        max_color = max(max_color, color_map[v.label])

    i = 0
    while True:
        i += 1
        changed = False
        for v in graph.vertices:
            v.cur_color_neigh = []
            for u in v.neighbours:
                v.cur_color_neigh.append(color_map[u.label])

        for u in graph.vertices:
            for v in graph.vertices:
                if u.label == v.label:
                    continue
                if color_map[u.label] == color_map[v.label] and not compare_two_list(u.cur_color_neigh,
                                                                                     v.cur_color_neigh):
                    max_color += 1
                    # color_map[(u.cur_color, v.cur_color_mul_neigh)] = max_color
                    for z in graph.vertices:
                        if color_map[z.label] == color_map[u.label] and compare_two_list(z.cur_color_neigh,
                                                                                         v.cur_color_neigh):
                            color_map[z.label] = max_color
                    changed = True
                    break
            if changed:
                break
        if not changed:
            break
    # print("--------------------------")
    # for v in graph.vertices:
    #     print(str(v.label) + ": " + str(v.cur_color))
    return color_map


def compare_two_list_with_equal(a, b):
    if len(a) != len(b):
        return 2

    a.sort()
    b.sort()

    flag = False
    for i in range(0, len(a)):
        if i < len(a) - 1 and a[i] == a[i + 1]:
            flag = True
        if a[i] != b[i]:
            return "False"
    if flag:
        return "Undecided"
    return "True"

