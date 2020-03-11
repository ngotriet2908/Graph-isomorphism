from utils.graph import *
from utils.utils import *


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


def color_refinement_with_initial_color_basic(graph: "Graph", color_map: "dict"):
    max_color = 0

    for v in graph.vertices:
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


def color_refinement_with_initial_color_improved(graph: "Graph", color_map: "dict"):
    max_color = 0

    for v in graph.vertices:
        max_color = max(max_color, color_map[v.label])

    color_neighbor = dict()
    for v in graph.vertices:
        color_neighbor[v.label] = []
        for u in v.neighbours:
            color_neighbor[v.label].append(color_map[u.label])

    color_partition = create_single_color_partition(color_map)

    while True:
        changed = False
        will_remove = []
        remove_color = 0
        for color, partition in color_partition.items():
            if len(partition) < 2:
                continue
            for i in range(0, len(partition) - 1):
                for j in range(i + 1, len(partition)):
                    u = partition[i]
                    v = partition[j]
                    if u == v:
                        continue

                    if not compare_two_list(color_neighbor[u], color_neighbor[v]):
                        max_color += 1
                        remove_color = color
                        color_partition[max_color] = []
                        for z in partition:
                            if compare_two_list(color_neighbor[z], color_neighbor[v]):
                                will_remove.append(z)
                        changed = True
                        break

                if changed:
                    break
            if changed:
                break
        if not changed:
            break
        else:
            for now_remove in will_remove:
                color_partition[remove_color].remove(now_remove)
                color_map[now_remove] = max_color
                color_partition[max_color].append(now_remove)
                zz = graph.find_vertex_with_label_int(now_remove)
                for z_neigh in zz.neighbours:
                    color_neighbor[z_neigh.label].remove(remove_color)
                    color_neighbor[z_neigh.label].append(max_color)
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
