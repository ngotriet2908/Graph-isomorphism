from utils.graph import *
from utils.graph_io import load_graph, write_dot
import math
import os
import random
import time
import queue


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


def compare_two_list(a, b):
    if len(a) != len(b):
        return False

    a.sort()
    b.sort()

    for i in range(0, len(a)):
        if a[i] != b[i]:
            return False

    return True


def count_isomorphism(union: "Graph", color_map: "dict", a: "Graph", b: "Graph"):
    new_color_map = clone_color_map(color_map)
    new_color_map = color_refinement_with_initial_color(union, new_color_map)

    res = compare_two_graph(union, new_color_map, a, b)

    if res == "False":
        return 0
    elif res == "True":
        return 1

    color_partition_a, color_partition_b, color_partition_union = create_color_partition(new_color_map)

    # max_color, max_value = 0, 0
    # for x in color_partition_union:
    #     if len(color_partition_union[x]) > max_value:
    #         max_color = x
    #         max_value = len(color_partition_union[x])

    max_color, max_value = 0, 100000000
    for x in color_partition_union:
        if max_value > len(color_partition_union[x]) > 3:
            max_color = x
            max_value = len(color_partition_union[x])

    max_color_label = 0
    for x in new_color_map:
        max_color_label = max(max_color_label, new_color_map[x])

    u = color_partition_a[max_color][random.randint(0, len(color_partition_a[max_color]) - 1)]
    num = 0
    for v in color_partition_b[max_color]:
        tmp_color_map = clone_color_map(new_color_map)
        tmp_color_map[u] = max_color + 1
        tmp_color_map[v] = max_color + 1
        num += count_isomorphism(union, tmp_color_map, a, b)
    return num


def encode_tree(graph: "Graph", u: "Vertex", level):
    if len(u.neighbours) == 1:
        return "01"
    else:
        sub_encode = []
        for v in u.neighbours:
            if level[v.label] > level[u.label]:
                sub_encode.append(encode_tree(graph, v, level))
        sub_encode.sort()
        res = ""
        for x in sub_encode:
            res += x
        return "0" + res + "1"


def is_isomorphism_tree(a: "Graph", b: "Graph"):
    root_a = find_root_tree(a)
    root_b = find_root_tree(b)
    level_a,_ = level_tree(a, root_a)
    level_b,_ = level_tree(b, root_b)
    encode_a = encode_tree(a, root_a, level_a)
    encode_b = encode_tree(b, root_b, level_b)
    return encode_a == encode_b


def is_isomorphism(union: "Graph", color_map: "dict", a: "Graph", b: "Graph"):
    new_color_map = clone_color_map(color_map)
    new_color_map = color_refinement_with_initial_color(union, new_color_map)

    res = compare_two_graph(union, new_color_map, a, b)

    if res == "False":
        return False
    elif res == "True":
        return True

    color_partition_a, color_partition_b, color_partition_union = create_color_partition(new_color_map)

    # max_color, max_value = 0, 0
    # for x in color_partition_union:
    #     if len(color_partition_union[x]) > max_value:
    #         max_color = x
    #         max_value = len(color_partition_union[x])

    max_color, max_value = 0, 100000000
    for x in color_partition_union:
        if max_value > len(color_partition_union[x]) > 3:
            max_color = x
            max_value = len(color_partition_union[x])

    max_color_label = 0
    for x in new_color_map:
        max_color_label = max(max_color_label, new_color_map[x])

    u = color_partition_a[max_color][random.randint(0, len(color_partition_a[max_color]) - 1)]
    for v in color_partition_b[max_color]:
        tmp_color_map = clone_color_map(new_color_map)
        tmp_color_map[u] = max_color + 1
        tmp_color_map[v] = max_color + 1
        tmp_res = is_isomorphism(union, tmp_color_map, a, b)
        if tmp_res:
            return True


def is_Twins(a: "Vertex", b: "Vertex"):
    false_twins = False
    if a in b.neighbours and b in a.neighbours:
        false_twins = True
    for u in a.neighbours:
        if u not in b.neighbours:
            return -1
    if false_twins:
        return 0
    return 1


def count_twins(union: "Graph"):
    has_twins = [False] * len(union.vertices)
    twins = []
    for u in union.vertices:
        for v in union.vertices:
            if u.label == v.label:
                continue
            if is_Twins(u, v) == 1:
                has_twins[u.label] = True
                has_twins[v.label] = True
                if len(twins) == 0:
                    twins.append([u.label, v.label])
                    continue

                flag = False
                for z in twins:
                    if u.label in z:
                        flag = True
                        break
                if flag:
                    for i in range(0, len(twins)):
                        if u.label in twins[i] and v.label not in twins[i]:
                            twins[i].append(v.label)
                            continue

                flag = False
                for z in twins:
                    if v.label in z:
                        flag = True
                        break
                if flag:
                    for i in range(0, len(twins)):
                        if v.label in twins[i] and u.label not in twins[i]:
                            twins[i].append(u.label)
                            continue
                twins.append([u.label, v.label])

    return twins, has_twins


def count_false_twins(union: "Graph"):
    has_false_twins = [False] * len(union.vertices)
    false_twins = []
    for u in union.vertices:
        for v in union.vertices:
            if u.label == v.label:
                continue
            if is_Twins(u, v) == 0:
                has_false_twins[u.label] = True
                has_false_twins[v.label] = True
                if len(false_twins) == 0:
                    false_twins.append([u.label, v.label])
                    continue

                flag = False
                for z in false_twins:
                    if u.label in z:
                        flag = True
                        break
                if flag:
                    for i in range(0, len(false_twins)):
                        if u.label in false_twins[i] and v.label not in false_twins[i]:
                            false_twins[i].append(v.label)
                            continue

                flag = False
                for z in false_twins:
                    if v.label in z:
                        flag = True
                        break
                if flag:
                    for i in range(0, len(false_twins)):
                        if v.label in false_twins[i] and u.label not in false_twins[i]:
                            false_twins[i].append(u.label)
                            continue
                false_twins.append([u.label, v.label])

    return false_twins, has_false_twins


def compare_two_graph(union: "Graph", color_map: "dict", a: "Graph", b: "Graph"):
    max_label = 0

    for v in a.vertices:
        max_label = max(max_label, v.label)

    color_a = []
    color_b = []
    for v in range(max_label + 1, max_label + len(b.vertices) + 1):
        u = union.find_vertex_with_label_int(v)
        color_a.append(color_map[u.label])

    for v in range(0, max_label + 1):
        u = union.find_vertex_with_label_int(v)
        color_b.append(color_map[u.label])

    return compare_two_list_with_equal(color_a, color_b)


def has_cycle_at_v(graph: "Graph", v: "Vertex", visited, p):
    visited[v.label] = True
    for u in v.neighbours:
        if not visited[u.label]:
            if has_cycle_at_v(graph, u, visited, v.label):
                return True
        elif u.label != p:
            return True
    return False


def is_Tree(graph: "Graph"):
    visited = [False] * len(graph.vertices)
    if has_cycle_at_v(graph, graph.find_vertex_with_label_int(0), visited, -1):
        return False
    for i in graph.vertices:
        if not visited[i.label]:
            return False
    return True


def level_tree(graph: "Graph", root: "Vertex"):
    level = [0] * len(graph.vertices)
    trace = [-1] * len(graph.vertices)
    visited = [False] * len(graph.vertices)
    q = []
    q.append(root.label)
    level[root.label] = 0
    visited[root.label] = True
    while len(q) > 0:
        u = graph.find_vertex_with_label_int(q.pop(0))
        for v in u.neighbours:
            if not visited[v.label]:
                q.append(v.label)
                level[v.label] = level[u.label] + 1
                visited[v.label] = True
                trace[v.label] = u.label
    return level, trace


def find_root_tree(graph: "Graph"):
    d, trace = level_tree(graph, graph.vertices[0])
    max_d, root_1 = 0, 0
    for i in range(0, len(d)):
        if d[i] > max_d:
            max_d = d[i]
            root_1 = i
    d, trace = level_tree(graph, graph.find_vertex_with_label_int(root_1))
    max_d, root_2 = 0, 0
    for i in range(0, len(d)):
        if d[i] > max_d:
            max_d = d[i]
            root_2 = i

    route = [root_2]
    while trace[root_2] != root_1:
        root_2 = trace[root_2]
        route.append(root_2)

    return graph.find_vertex_with_label_int(route[len(route) // 2])


def multipli_tree(graph: "Graph", level, u: "Vertex", color_map, giaithua):
    if len(u.neighbours) == 1 and level[u.label] != 0:
        return 1
    res = 1
    child = []
    for v in u.neighbours:
        if level[v.label] > level[u.label]:
            child.append(v)
    for c in child:
        res *= multipli_tree(graph, level, c, color_map, giaithua)
    color = []
    for c in child:
        color.append(color_map[c.label])
    color.sort()
    # print(color)
    per = 1
    for i in range(0, len(color) - 1):
        if color[i] == color[i + 1]:
            per += 1
        else:
            res *= giaithua[per]
            per = 1
    res *= giaithua[per]
    return res


def counting_auth_tree(graph: "Graph"):
    new_graph = graph.clone_graph()
    color_map = color_refinement_with_initial_color(new_graph, create_color_map(new_graph))
    root = new_graph.find_vertex_with_label_int(0)
    color_partition = create_single_color_partition(color_map)

    for v in color_partition:
        if len(color_partition[v]) == 1:
            root = new_graph.find_vertex_with_label_int(color_partition[v][0])
    tmp_root = find_root_tree(graph)
    if len(color_partition[color_map[tmp_root.label]]) == 1:
        root = tmp_root

    level, trace = level_tree(new_graph, root)
    giaithua = [1]
    max_nei = 0
    for v in new_graph.vertices:
        max_nei = max(max_nei, len(v.neighbours))
    for i in range(1, max_nei + 5):
        giaithua.append(i * giaithua[i - 1])

    return multipli_tree(new_graph, level, root, color_map, giaithua)


def testing():
    # with open(os.path.join(os.getcwd(), "../graphs/color_refinement/colorref_smallexample_6_15.grl")) as f:
    with open(os.path.join(os.getcwd(), "../graphs/branching/bigtrees1.grl")) as f:
        G = load_graph(f, read_list=True)
        # for g in G[0]:
        #     g = color_refinement_without_initial_color(g)
        for i in range(0, len(G[0]) - 1):
            for j in range(i + 1, len(G[0])):
                # print("Is graph " + str(i) + " a tree ?: " + str(is_Tree(G[0][i])))
                # print("Is graph " + str(j) + " a tree ?: " + str(is_Tree(G[0][j])))

                new_graph = G[0][i].__add__(G[0][j])
                color_map = color_refinement_with_initial_color(new_graph, create_color_map(new_graph))
                # with open(os.path.join(os.getcwd(), 'union.dot'), 'w') as f:
                #     write_dot(new_graph, f)
                # print(create_color_partition(color_map))
                res = is_isomorphism(new_graph, color_map, G[0][i], G[0][j])
                if res:
                    print("Compare " + str(i) + " and " + str(j) + " :" + str(res))


def testing_counting_tree():
    # with open(os.path.join(os.getcwd(), "../graphs/color_refinement/colorref_smallexample_6_15.grl")) as f:
    with open(os.path.join(os.getcwd(), "../graphs/branching/bigtrees3.grl")) as f:
        G = load_graph(f, read_list=True)
        # for g in G[0]:
        #     g = color_refinement_without_initial_color(g)
        for i in range(0, len(G[0]) - 1):
            for j in range(i + 1, len(G[0])):
                # print("Is graph " + str(i) + " a tree ?: " + str(is_Tree(G[0][i])))
                # print("Is graph " + str(j) + " a tree ?: " + str(is_Tree(G[0][j])))

                new_graph = G[0][i].__add__(G[0][j])
                color_map = color_refinement_with_initial_color(new_graph, create_color_map(new_graph))
                # with open(os.path.join(os.getcwd(), 'union.dot'), 'w') as f:
                #     write_dot(new_graph, f)
                # print(create_color_partition(color_map))
                res = is_isomorphism_tree(G[0][i], G[0][j])
                if res:
                    start_time_aut = time.time()
                    print("Compare " + str(i) + " and " + str(j) + " : " + str(res) +
                          " " + str(counting_auth_tree(G[0][i])))


def testing_tree():
    with open(os.path.join(os.getcwd(), "../graphs/branching/trees36.grl")) as f:
        G = load_graph(f)
        color_map = color_refinement_with_initial_color(G, create_color_map(G))
        print(color_map)
        # for g in G[0]:


start_time = time.time()
testing_counting_tree()
print("Running time: " + str(time.time() - start_time))
