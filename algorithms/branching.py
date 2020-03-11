import random
from algorithms.color_refinement import *

choosing_color_class_rule = "min" # min max rand first
choosing_vertex_rule = "rand" # rand, first last


def count_isomorphism(union: "Graph", color_map: "dict", a: "Graph", b: "Graph"):
    new_color_map = clone_color_map(color_map)
    # new_color_map = color_refinement_with_initial_color(union, new_color_map)
    new_color_map = color_refinement_with_initial_color_improved(union, new_color_map)

    res = compare_two_graph(union, new_color_map, a, b)

    if res == "False":
        return 0
    elif res == "True":
        return 1

    color_partition_a, color_partition_b, color_partition_union = create_color_partition(new_color_map)

    max_color_label = 0
    for x in new_color_map:
        max_color_label = max(max_color_label, new_color_map[x])

    chosen_color = choose_color(choosing_color_class_rule, color_partition_union, max_color_label)

    u = 0
    if choosing_vertex_rule == "rand":
        u = color_partition_a[chosen_color][random.randint(0, len(color_partition_a[chosen_color]) - 1)]
    elif choosing_vertex_rule == "first":
        u = color_partition_a[chosen_color][0]
    elif choosing_vertex_rule == "last":
        u = color_partition_a[chosen_color][len(color_partition_a[chosen_color]) - 1]

    num = 0
    for v in color_partition_b[chosen_color]:
        tmp_color_map = clone_color_map(new_color_map)
        tmp_color_map[u] = max_color_label + 1
        tmp_color_map[v] = max_color_label + 1
        num += count_isomorphism(union, tmp_color_map, a, b)
    return num


def is_isomorphism(union: "Graph", color_map: "dict", a: "Graph", b: "Graph"):
    new_color_map = clone_color_map(color_map)
    # new_color_map = color_refinement_with_initial_color(union, new_color_map)
    new_color_map = color_refinement_with_initial_color_improved(union, new_color_map)

    res = compare_two_graph(union, new_color_map, a, b)

    if res == "False":
        return False
    elif res == "True":
        return True

    color_partition_a, color_partition_b, color_partition_union = create_color_partition(new_color_map)

    max_color_label = 0
    for x in new_color_map:
        max_color_label = max(max_color_label, new_color_map[x])

    chosen_color = choose_color(choosing_color_class_rule, color_partition_union, max_color_label)

    u = 0
    if choosing_vertex_rule == "rand":
        u = color_partition_a[chosen_color][random.randint(0, len(color_partition_a[chosen_color]) - 1)]
    elif choosing_vertex_rule == "first":
        u = color_partition_a[chosen_color][0]
    elif choosing_vertex_rule == "last":
        u = color_partition_a[chosen_color][len(color_partition_a[chosen_color]) - 1]

    for v in color_partition_b[chosen_color]:
        tmp_color_map = clone_color_map(new_color_map)
        tmp_color_map[u] = max_color_label + 1
        tmp_color_map[v] = max_color_label + 1
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
    for u in b.neighbours:
        if u not in a.neighbours:
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


def choose_color(option, color_partition_union, max_color_label):
    max_color = 0
    if option == "min":
        max_value = 1000000000
        for x in color_partition_union:
            if max_value > len(color_partition_union[x]) > 3:
                max_color = x
                max_value = len(color_partition_union[x])
    elif option == "max":
        max_value = 0
        for x in color_partition_union:
            if len(color_partition_union[x]) > max_value:
                max_color = x
                max_value = len(color_partition_union[x])

    elif option == "first":
        for x in color_partition_union:
            if len(color_partition_union[x]) > 3:
                max_color = x
                break
    elif option == "rand":
        while True:
            tmp = random.randint(0, max_color_label)
            if tmp in color_partition_union and len(color_partition_union) > 3:
                max_color = tmp
                break

    return max_color


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
