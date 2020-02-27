from utils.graph import *
from utils.graph_io import load_graph, write_dot
from algorithms.prime import *
import math
import os


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
            v.cur_color_neigh = []
            for u in v.neighbours:
                v.cur_color_neigh.append(u.cur_color)

        for u in graph.vertices:
            for v in graph.vertices:
                if u.label == v.label:
                    continue
                if u.cur_color == v.cur_color and not compare_two_list(u.cur_color_neigh, v.cur_color_neigh):
                    max_color += 1
                    # color_map[(u.cur_color, v.cur_color_mul_neigh)] = max_color
                    for z in graph.vertices:
                        if z.cur_color == u.cur_color and compare_two_list(z.cur_color_neigh, v.cur_color_neigh):
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
    return graph


def gen_prime():
    prime = [2]
    for num in range(3, 20000000000, 2):
        if all(num % i != 0 for i in range(3, int(math.sqrt(num)) + 1, 2)):
            prime.append(num)
        if len(prime) > 2000:
            break
    print(prime)


def compare_two_list(a, b):
    if len(a) != len(b):
        return False

    a.sort()
    b.sort()

    for i in range(0, len(a)):
        if a[i] != b[i]:
            return False
    return True


def compare_two_graph(union: "Graph", a: "Graph", b: "Graph"):
    # color_a = []
    # color_b = []
    # for u in a.vertices:
    #     color_a.append(u.cur_color)
    #
    # for u in b.vertices:
    #     color_b.append(u.cur_color)
    #
    # return compare_two_list(color_a, color_b)

    for v in union.vertices:
        v.cur_color_neigh = []
        for u in v.neighbours:
            v.cur_color_neigh.append(u.cur_color)

    # partition_a = dict()
    partition_b = dict()

    # for v in a.vertices:
    #     if v.cur_color not in partition_a:
    #         partition_a[v.cur_color] = [v]
    #     else:
    #         partition_a[v.cur_color].append(v)

    max_label = 0
    for v in a.vertices:
        max_label = max(max_label, v.label)

    for v in range(max_label + 1, max_label + len(b.vertices) + 1):
        u = union.find_vertex_with_label_int(v)
        if u is not None and u.cur_color not in partition_b:
            partition_b[u.cur_color] = [u]
        else:
            partition_b[u.cur_color].append(u)

    for z in range(0, max_label):
        v = union.find_vertex_with_label_int(z)
        if v is None:
            continue
        same_exist = False
        if v.cur_color not in partition_b:
            return False
        for u in partition_b[v.cur_color]:
            if compare_two_list(v.cur_color_neigh, u.cur_color_neigh):
                same_exist = True
                break
        if not same_exist:
            return False

    return True


def testing():
    with open(os.path.join(os.getcwd(), "../graphs/color_refinement/colorref_smallexample_2_49.grl")) as f:
        G = load_graph(f, read_list=True)
        # for g in G[0]:
        #     g = color_refinement_without_initial_color(g)
        for i in range(0, len(G[0]) - 1):
            for j in range(i + 1, len(G[0])):
                new_graph = G[0][i].__add__(G[0][j])
                new_graph = color_refinement_without_initial_color(new_graph)
                # with open(os.path.join(os.getcwd(), 'union.dot'), 'w') as f:
                #     write_dot(new_graph, f)
                print("Compare " + str(i) + " and " + str(j) + " :" + str(compare_two_graph(new_graph, G[0][i], G[0][j])))


# gen_prime()
testing()
