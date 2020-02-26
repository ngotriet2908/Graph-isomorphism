from utils.graph import *
from utils.graph_io import load_graph, write_dot
from algorithms.prime import *
import math


def color_refinement_without_initial_color(graph: "Graph"):
    max_color = 0

    for v in graph.vertices:
        v.cur_color = v.degree
        max_color = max(max_color, v.cur_color)

    color_map = dict()

    i = 0
    while True:
        i += 1
        changed = False
        for v in graph.vertices:
            v.cur_color_mul_neigh = 1
            for u in v.neighbours:
                v.cur_color_mul_neigh *= prime_n_th(u.cur_color)

        for u in graph.vertices:
            for v in graph.vertices:
                if u.label == v.label:
                    continue
                if u.cur_color == v.cur_color and u.cur_color_mul_neigh != v.cur_color_mul_neigh:
                    max_color += 1
                    # color_map[(u.cur_color, v.cur_color_mul_neigh)] = max_color
                    for z in graph.vertices:
                        if z.cur_color == v.cur_color and z.cur_color_mul_neigh == v.cur_color_mul_neigh:
                            z.cur_color = max_color
                    changed = True
                    break
            if changed:
                break
        if not changed:
            break
    # print("--------------------------")
    # for v in graph.vertices:
    #     print(str(v.label) + ": " + str(v.cur_color))
    # return graph


def gen_prime():
    prime = [2]
    for num in range(3, 20000000000, 2):
        if all(num % i != 0 for i in range(3, int(math.sqrt(num)) + 1, 2)):
            prime.append(num)
        if len(prime) > 2000:
            break
    print(prime)


def compare_two_graph(a: "Graph", b: "Graph"):
    color_a = []
    color_b = []
    for u in a.vertices:
        color_a.append(u.cur_color)

    for u in b.vertices:
        color_b.append(u.cur_color)

    color_a_dict = dict()
    color_b_dict = dict()

    for i in color_a:
        if i not in color_a_dict:
            color_a_dict[i] = 1
        else:
            color_a_dict[i] += 1

    for i in color_b:
        if i not in color_b_dict:
            color_b_dict[i] = 1
        else:
            color_b_dict[i] += 1

    color_a_dict_sort_list = []
    color_b_dict_sort_list = []
    for i in color_a_dict.values():
        color_a_dict_sort_list.append(i)
    for i in color_b_dict.values():
        color_b_dict_sort_list.append(i)
    color_a_dict_sort_list.sort()
    color_b_dict_sort_list.sort()

    if len(color_a_dict_sort_list) != len(color_b_dict_sort_list):
        return False

    Same = True
    for i in range(0, len(color_b_dict_sort_list)):
        if not color_b_dict_sort_list[i] == color_a_dict_sort_list[i]:
            Same = False
            break
    return Same


def testing():
    with open("/Users/ngocapu/PycharmProjects/projectmod7/graphs/color_refinement/colorref_smallexample_6_15.grl") as f:
        G = load_graph(f, read_list=True)
        for g in G[0]:
            g = color_refinement_without_initial_color(g)
        for i in range(0, len(G[0]) - 1):
            for j in range (i + 1, len(G[0])):
                print("Compare " + str(i) + " and " + str(j) + " :" + str(compare_two_graph(G[0][i], G[0][j])))


# gen_prime()
testing()
