import random
from algorithms.color_refinement import *
from algorithms.branching import *
from algorithms.permv2 import *
from algorithms.basicpermutationgroup import *

choosing_color_class_rule = "min"  # min max rand first
choosing_vertex_rule = "first"  # rand, first last

X = []


def create_permutation(color_map, union: "Graph", a: "Graph"):
    res = []
    color_partition_a, color_partition_b, color_partition_union = create_color_partition(color_map)
    a_len = len(a.vertices)
    for i in range(0, a_len):
        tmp = color_partition_b[color_map[i]][0] - a_len
        res.append(tmp)
    return res


def create_color_map_from_D_I(union: "Graph", D, I, a: "Graph"):
    cur_color = 1
    color_map = dict()
    for i in range(0, len(D)):
        color_map[D[i]] = cur_color
        color_map[I[i] + len(a)] = cur_color
        cur_color += 1

    for x in union.vertices:
        if x.label not in color_map:
            color_map[x.label] = cur_color

    return color_map


return_flag = 0


def count_automorphism(union: "Graph", D: list, I: list, a: "Graph"):
    global return_flag
    global X
    color_map = faster_color_refinement(union, create_color_map_from_D_I(union, D, I, a))

    res = compare_two_graph(union, color_map, a, a)

    if res == "False":
        return 0
    elif res == "True":
        per = permutation(len(a), mapping=create_permutation(color_map, union, a))
        X.append(per)
        return 1

    color_partition_a, color_partition_b, color_partition_union = create_color_partition(color_map)

    max_color_label = 0
    for x in color_map:
        max_color_label = max(max_color_label, color_map[x])

    chosen_color = choose_color(choosing_color_class_rule, color_partition_union, max_color_label)

    u = 0
    if choosing_vertex_rule == "rand":
        u = color_partition_a[chosen_color][random.randint(0, len(color_partition_a[chosen_color]) - 1)]
    elif choosing_vertex_rule == "first":
        u = color_partition_a[chosen_color][0]
    elif choosing_vertex_rule == "last":
        u = color_partition_a[chosen_color][len(color_partition_a[chosen_color]) - 1]

    if u + len(a) in color_partition_b[chosen_color]:
        for i in range(0, len(color_partition_b[chosen_color])):
            if color_partition_b[chosen_color][i] == u + len(a):
                tmp = color_partition_b[chosen_color][0]
                color_partition_b[chosen_color][0] = color_partition_b[chosen_color][i]
                color_partition_b[chosen_color][i] = tmp

    for v in color_partition_b[chosen_color]:
        D.append(u)
        I.append(v - len(a))
        return_flag = count_automorphism(union, D, I, a)
        D.pop()
        I.pop()
        if return_flag == 1:
            DD = D.copy()
            II = I.copy()
            if not compare_two_list(DD, II):
                return 1
    return 0


def is_iso(union: "Graph", D: list, I: list, a: "Graph", b: "Graph"):
    color_map = faster_color_refinement(union, create_color_map_from_D_I(union, D, I, a))

    res = compare_two_graph(union, color_map, a, b)

    if res == "False":
        return False
    elif res == "True":
        return True

    color_partition_a, color_partition_b, color_partition_union = create_color_partition(color_map)

    max_color_label = 0
    for x in color_map:
        max_color_label = max(max_color_label, color_map[x])

    chosen_color = choose_color(choosing_color_class_rule, color_partition_union, max_color_label)

    u = 0
    if choosing_vertex_rule == "rand":
        u = color_partition_a[chosen_color][random.randint(0, len(color_partition_a[chosen_color]) - 1)]
    elif choosing_vertex_rule == "first":
        u = color_partition_a[chosen_color][0]
    elif choosing_vertex_rule == "last":
        u = color_partition_a[chosen_color][len(color_partition_a[chosen_color]) - 1]

    if u + len(a) in color_partition_b[chosen_color]:
        for i in range(0, len(color_partition_b[chosen_color])):
            if color_partition_b[chosen_color][i] == u + len(a):
                tmp = color_partition_b[chosen_color][0]
                color_partition_b[chosen_color][0] = color_partition_b[chosen_color][i]
                color_partition_b[chosen_color][i] = tmp

    for v in color_partition_b[chosen_color]:
        D.append(u)
        I.append(v - len(a))
        res = is_iso(union, D, I, a, b)
        if res:
            return True
        D.pop()
        I.pop()


def calculate_order(gen):
    if len(gen) <= 0:
        return 1
    alpha = FindNonTrivialOrbit(gen)
    orbit_alpha = Orbit(gen, alpha)
    stab_alpha = Stabilizer(gen, alpha)
    return calculate_order(stab_alpha) * len(orbit_alpha)


def membership_testing(gen, f):
    alpha = FindNonTrivialOrbit(gen)
    orbit_alpha, u = Orbit(gen, alpha, returntransversal=True)

    return len(orbit_alpha)


def count_automorphism_final(union: "Graph", D: list, I: list, a: "Graph"):
    global X
    X = []
    count_automorphism(union=union, D=[], I=[], a=a)
    return calculate_order(X)

# H = []
# p = permutation(6, cycles=[[0, 1, 2], [4, 5]])
# q = permutation(6, cycles=[[2, 3]])
# H.append(p)
# H.append(q)
# print(calculate_order(H))
