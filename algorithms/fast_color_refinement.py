from algorithms.color_refinement import *


def encode_list_to_string(l):
    return '_'.join([str(elem) for elem in l])


def fast_color_refinement_improved(graph: "Graph", color_map: "dict"):
    min_color = 0
    max_color = 0
    for v in graph.vertices:
        max_color = max(max_color, color_map[v.label])
        min_color = min(min_color, color_map[v.label])

    q = []
    for v in graph.vertices:
        if color_map[v.label] not in q:
            q.append(color_map[v.label])

    color_partition = create_single_color_partition(color_map)
    while len(q) > 0:
        cur_color = q.pop(0)
        d = [0] * len(graph.vertices)
        for vv in color_partition[cur_color]:
            v = graph.find_vertex_with_label_int(vv)
            d[v.label] = 0
            for nei in v.neighbours:
                if color_map[nei.label] == cur_color:
                    d[v.label] += 1
        B_to_vertexes = dict()
        B = []
        for v in graph.vertices:
            if (color_map[v.label], d[v.label]) not in B:
                B[(color_map[v.label], d[v.label])] = [v.label]
            else:
                B[(color_map[v.label], d[v.label])].append(v.label)
        for b in B_to_vertexes:
            B.append(b)
        B.sort(key=get_key)
        for i in range(min_color, max_color + 1):
            tmp = 1
            # TODO


def get_key(elem):
    return elem[1] * 100000000 + elem[2]


def faster_color_refinement(graph: "Graph", color_map: "dict"):
    A = dict()
    color_degree = dict()
    max_color_degree = dict()
    max_color = 0

    label_to_vertex_map = dict()
    for v in graph.vertices:
        label_to_vertex_map[v.label] = v

    for v in graph.vertices:
        A[v.label] = []
        max_color_degree[v.label] = 0
        color_degree[v.label] = 0
        max_color = max(max_color, color_map[v.label])

    color_partition = create_single_color_partition(color_map)

    # This creates a stack of all current color that needs to be processed
    stack = []
    for v in graph.vertices:
        if color_map[v.label] not in stack:
            stack.append(color_map[v.label])

    stack.sort()
    colors_adj = []

    while len(stack) > 0:
        current_color = stack.pop(0)

        if len(color_partition[current_color]) <= 1:
            continue

        for v_label in color_partition[current_color]:
            v = label_to_vertex_map[v_label]
            for nei in v.neighbours:
                color_degree[nei.label] += 1
                if color_degree[nei.label] == 1:
                    A[color_map[nei.label]].append(nei)
                if color_map[nei.label] not in colors_adj:
                    colors_adj.append(color_map[nei.label])

                if color_degree[nei.label] > max_color_degree[color_map[nei.label]]:
                    max_color_degree[color_map[nei.label]] = color_degree[nei.label]

        min_color_degree = dict()
        for nei_color in colors_adj:
            if len(color_partition[nei_color]) != len(A[nei_color]):
                min_color_degree[nei_color] = 0
            else:
                min_color_degree[nei_color] = max_color_degree[nei_color]
                for v in A[nei_color]:
                    if color_degree[v.label] < min_color_degree[nei_color]:
                        min_color_degree[nei_color] = color_degree[v.label]

        color_split = []
        for nei_color in colors_adj:
            if min_color_degree[nei_color] < max_color_degree[nei_color]:
                color_split.append(nei_color)
        color_split.sort()

        for color in color_split:
            new_color_to_color_degree_map = dict()
            max_color_degree_value = max_color_degree[color]

            num_color_degree = dict()
            for i in range(1, max_color_degree_value + 1):
                num_color_degree[i] = 0
            num_color_degree[0] = len(color_partition[color]) - len(A[color])
            for v in A[color]:
                num_color_degree[color_degree[v.label]] += 1

            b = 0
            for i in range(1, max_color_degree_value + 1):
                if num_color_degree[i] > num_color_degree[b]:
                    b = i

            in_stack = color in stack
            for i in range(0, max_color_degree_value + 1):
                if num_color_degree[i] >= 1:
                    if i == min_color_degree[color]:
                        new_color_to_color_degree_map[i] = color
                        if not in_stack and b != i:
                            stack.insert(0, new_color_to_color_degree_map[i])
                    else:
                        max_color += 1
                        new_color_to_color_degree_map[i] = max_color
                        if in_stack or i != b:
                            stack.insert(0, new_color_to_color_degree_map[i])

            for v in A[color]:
                if new_color_to_color_degree_map[color_degree[v.label]] != color:
                    if v.label in color_partition[color]:
                        color_partition[color].remove(v.label)
                    next_color = new_color_to_color_degree_map[color_degree[v.label]]
                    if next_color not in color_partition:
                        color_partition[next_color] = [v.label]
                    else:
                        color_partition[next_color].append(v.label)
                    color_map[v.label] = next_color

        for color in colors_adj:
            for v in A[color]:
                color_degree[v.label] = 0
            max_color_degree[color] = 0
            A[color] = []
        colors_adj = []

    return color_map


def fast_color_refinement(graph: "Graph", color_map: "dict"):
    max_color = 0

    for v in graph.vertices:
        max_color = max(max_color, color_map[v.label])

    color_neighbor = dict()
    for v in graph.vertices:
        color_neighbor[v.label] = []
        for u in v.neighbours:
            color_neighbor[v.label].append(color_map[u.label])

    color_partition = create_single_color_partition(color_map)

    color_need_to_process_queue = []

    for color, partition in color_partition.items():
        color_need_to_process_queue.append(color)

    while len(color_need_to_process_queue) > 0:
        current_color = color_need_to_process_queue.pop(0)
        neighbor_type = dict()

        if len(color_partition[current_color]) == 1:
            continue

        for vertex in color_partition[current_color]:
            color_neighbor[vertex].sort()
            if encode_list_to_string(color_neighbor[vertex]) not in neighbor_type:
                neighbor_type[encode_list_to_string(color_neighbor[vertex])] = [vertex]
            else:
                neighbor_type[encode_list_to_string(color_neighbor[vertex])].append(vertex)

        if len(neighbor_type) == 1:
            continue

        neighbor_type_to_new_color = dict()
        max_neighborTypeVertexes, max_neighborType = 100000000, 0
        for neighborType, vertexes in neighbor_type.items():
            if len(vertexes) < max_neighborTypeVertexes:
                max_neighborTypeVertexes = len(vertexes)
                max_neighborType = neighborType

        for neighborType, vertexes in neighbor_type.items():
            if neighborType == max_neighborType:
                neighbor_type_to_new_color[neighborType] = current_color
                continue
            max_color += 1
            color_partition[max_color] = []
            neighbor_type_to_new_color[neighborType] = max_color

        for neighborType, newColor in neighbor_type_to_new_color.items():
            # if not newColor == current_color:
            color_need_to_process_queue.append(newColor)

        for neighborType, vertexes in neighbor_type.items():
            for vertex in vertexes:
                new_color = neighbor_type_to_new_color[neighborType]
                if new_color == current_color:
                    continue
                color_partition[current_color].remove(vertex)
                color_partition[new_color].append(vertex)
                color_map[vertex] = new_color
                zz = graph.find_vertex_with_label_int(vertex)
                for z_neigh in zz.neighbours:
                    if color_map[z_neigh.label] not in color_need_to_process_queue:
                        color_need_to_process_queue.append(color_map[z_neigh.label])
                    color_neighbor[z_neigh.label].remove(current_color)
                    color_neighbor[z_neigh.label].append(new_color)

    return color_map
