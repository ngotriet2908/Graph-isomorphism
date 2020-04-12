import os
import time
from algorithms.color_refinement import *
from algorithms.branching import *
from algorithms.isomorphic_automorphic_tree import *
from utils.graph_io import *
from algorithms.fast_color_refinement import *
from algorithms.count_auth import *


def output_isomorphism(list_of_graph):
    isomorphism_set = []
    for i in range(0, len(list_of_graph) - 1):
        for j in range(i + 1, len(list_of_graph)):
            if is_in_same_set(isomorphism_set, i, j):
                continue
            res = False
            if is_Tree(list_of_graph[i]) and is_Tree(list_of_graph[j]):
                res = is_isomorphism_tree(list_of_graph[i], list_of_graph[j])
            else:
                # print("comparing " + str(i) + " and " + str(j))
                new_graph = list_of_graph[i].__add__(list_of_graph[j])
                color_map = faster_color_refinement(new_graph, create_color_map(new_graph))
                # res = is_isomorphism(new_graph, color_map, G[0][i], G[0][j])
                res = is_iso(new_graph, [], [], list_of_graph[i], list_of_graph[j])
            if res:
                if not is_in_set(isomorphism_set, i) and not is_in_set(isomorphism_set, j):
                    isomorphism_set.append([i, j])
                elif is_in_set(isomorphism_set, i):
                    for sett in isomorphism_set:
                        if i in sett:
                            sett.append(j)
                elif is_in_set(isomorphism_set, j):
                    for sett in isomorphism_set:
                        if j in sett:
                            sett.append(i)
    print("Sets of isomorphic graphs:")
    for sett in isomorphism_set:
        print(sett)


def output_automorphism(list_of_graph):
    print("Graph: Number of automorphisms:")
    i = 0
    for g in list_of_graph:
        if is_Tree(g):
            res = counting_auth_tree_with_encoding(g)
            i += 1
        else:
            new_graph = g.__add__(g)
            color_map = faster_color_refinement(new_graph, create_color_map(new_graph))
            # res = count_isomorphism(new_graph, color_map, G[0][sett[0]], G[0][sett[1]])
            res = count_automorphism_final(union=new_graph, D=[], I=[], a=g)
            i += 1

        print((str(i) + ":").ljust(7) + str(res))


def output_iso_auto(list_of_graph):
    isomorphism_set = []
    for i in range(0, len(list_of_graph) - 1):
        for j in range(i + 1, len(list_of_graph)):
            if is_in_same_set(isomorphism_set, i, j):
                continue
            res = False
            if is_Tree(list_of_graph[i]) and is_Tree(list_of_graph[j]):
                res = is_isomorphism_tree(list_of_graph[i], list_of_graph[j])
            else:
                # print("comparing " + str(i) + " and " + str(j))
                new_graph = list_of_graph[i].__add__(list_of_graph[j])
                color_map = faster_color_refinement(new_graph, create_color_map(new_graph))
                # res = is_isomorphism(new_graph, color_map, G[0][i], G[0][j])
                res = is_iso(new_graph, [], [], list_of_graph[i], list_of_graph[j])
            if res:
                if not is_in_set(isomorphism_set, i) and not is_in_set(isomorphism_set, j):
                    isomorphism_set.append([i, j])
                elif is_in_set(isomorphism_set, i):
                    for sett in isomorphism_set:
                        if i in sett:
                            sett.append(j)
                elif is_in_set(isomorphism_set, j):
                    for sett in isomorphism_set:
                        if j in sett:
                            sett.append(i)

    print("Sets of isomorphic graphs:  Number of automorphisms:")
    for sett in isomorphism_set:
        if is_Tree(list_of_graph[sett[0]]):
            res = counting_auth_tree_with_encoding(list_of_graph[sett[0]])
            print(str(sett).ljust(28) + str(res))
        else:
            new_graph = list_of_graph[sett[0]].__add__(list_of_graph[sett[0]])
            color_map = faster_color_refinement(new_graph, create_color_map(new_graph))
            # res = count_isomorphism(new_graph, color_map, G[0][sett[0]], G[0][sett[1]])
            res = count_automorphism_final(union=new_graph, D=[], I=[], a=list_of_graph[sett[0]])
            print(str(sett).ljust(28) + str(res))
