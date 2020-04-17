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

    for i in range(0, len(list_of_graph)):
        if not is_in_set(isomorphism_set, i):
            isomorphism_set.append([i])

    print("Sets of isomorphic graphs:")
    for sett in isomorphism_set:
        print(sett)

def output_isomorphism_improved(list_of_graph):
    isomorphism_set = []

    twins = []
    false_twins = []
    for i in range(0, len(list_of_graph)):
        num_twins,_ = count_twins(list_of_graph[i])
        num_false_twins,_ = count_false_twins(list_of_graph[i])

        num_in_twins = []
        for set_of_twins in num_twins:
            num_in_twins.append(len(set_of_twins))
        if len(num_in_twins) > 0:
            twins.append(num_in_twins)
        else:
            twins.append([0])

        num_in_false_twins = []
        for set_of_false_twins in num_false_twins:
            num_in_false_twins.append(len(set_of_false_twins))
        if len(num_in_false_twins) > 0:
            false_twins.append(num_in_false_twins)
        else:
            false_twins.append([0])

    for i in range(0, len(list_of_graph) - 1):
        for j in range(i + 1, len(list_of_graph)):
            if is_in_same_set(isomorphism_set, i, j):
                continue
            res = False
            if not compare_two_list(twins[i],twins[j]) or not compare_two_list(false_twins[i],false_twins[j]):
                res = False
            elif is_Tree(list_of_graph[i]) and is_Tree(list_of_graph[j]):
                res = is_isomorphism_tree(list_of_graph[i], list_of_graph[j])
            elif not is_Tree(list_of_graph[i]) and is_Tree(list_of_graph[j]):
                res = False
            elif is_Tree(list_of_graph[i]) and not is_Tree(list_of_graph[j]):
                res = False
            else:
                # print("comparing " + str(i) + " and " + str(j))
                new_graph = list_of_graph[i].__add__(list_of_graph[j])
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

    for i in range(0, len(list_of_graph)):
        if not is_in_set(isomorphism_set, i):
            isomorphism_set.append([i])

    print("Sets of isomorphic graphs:")
    for sett in isomorphism_set:
        print(sett)

def output_automorphism(list_of_graph):
    print("Graph: Number of automorphisms:")
    i = 0
    for g in list_of_graph:
        if is_Tree(g):
            res = counting_auth_tree_with_encoding(g)
        else:
            new_graph = g.__add__(g)
            res = count_automorphism_final(union=new_graph, D=[], I=[], a=g)

        print((str(i) + ":").ljust(7) + str(res))
        i += 1


def output_iso_auto(list_of_graph, flag_testing_tree, flag_using_basic_algo):
    isomorphism_set = []
    for i in range(0, len(list_of_graph) - 1):
        for j in range(i + 1, len(list_of_graph)):
            if is_in_same_set(isomorphism_set, i, j):
                continue
            res = False
            if flag_testing_tree and is_Tree(list_of_graph[i]) and is_Tree(list_of_graph[j]):
                res = is_isomorphism_tree(list_of_graph[i], list_of_graph[j])
            else:
                # print("comparing " + str(i) + " and " + str(j))
                new_graph = list_of_graph[i].__add__(list_of_graph[j])
                if not flag_using_basic_algo:
                    res = is_iso(new_graph, [], [], list_of_graph[i], list_of_graph[j])
                else:
                    res = is_isomorphism(new_graph, create_color_map(new_graph), list_of_graph[i], list_of_graph[j])
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

    for i in range(0, len(list_of_graph)):
        if not is_in_set(isomorphism_set, i):
            isomorphism_set.append([i])

    print("Sets of isomorphic graphs:  Number of automorphisms:")
    for sett in isomorphism_set:
        if flag_testing_tree and is_Tree(list_of_graph[sett[0]]):
            res = counting_auth_tree_with_encoding(list_of_graph[sett[0]])
            print(str(sett).ljust(28) + str(res))
        else:
            if flag_using_basic_algo:
                new_graph = list_of_graph[sett[0]].__add__(list_of_graph[sett[1]])
                res = count_isomorphism(new_graph, create_color_map(new_graph), list_of_graph[0], list_of_graph[1])
                print(str(sett).ljust(28) + str(res))

            else:
                new_graph = list_of_graph[sett[0]].__add__(list_of_graph[sett[0]])
                res = count_automorphism_final(union=new_graph, D=[], I=[], a=list_of_graph[sett[0]])
                print(str(sett).ljust(28) + str(res))
