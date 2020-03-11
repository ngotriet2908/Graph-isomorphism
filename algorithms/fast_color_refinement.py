from algorithms.color_refinement import *


def encode_list_to_string(l):
    return '_'.join([str(elem) for elem in l])


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
                    color_neighbor[z_neigh.label].remove(current_color)
                    color_neighbor[z_neigh.label].append(new_color)

    return color_map
