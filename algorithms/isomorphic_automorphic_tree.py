from algorithms.color_refinement import *


def encode_tree_with_array(graph: "Graph", root: "Vertex", level):
    decoding = [""] * len(graph.vertices)

    def encode_tree(graph: "Graph", u: "Vertex", level):
        if len(u.neighbours) == 1:
            decoding[u.label] = "01"
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
            decoding[u.label] = "0" + res + "1"
            return "0" + res + "1"

    res = encode_tree(graph, root, level)
    return res, decoding


def is_isomorphism_tree(a: "Graph", b: "Graph"):
    root_a = find_root_tree(a)
    root_b = find_root_tree(b)
    level_a, _ = level_tree(a, root_a)
    level_b, _ = level_tree(b, root_b)
    encode_a, _ = encode_tree_with_array(a, root_a, level_a)
    encode_b, _ = encode_tree_with_array(b, root_b, level_b)
    return encode_a == encode_b


visited = []


def is_Tree(graph: "Graph"):
    global visited
    visited = [False] * len(graph.vertices)
    parent = [-1] * len(graph.vertices)
    if has_cycle_at_v_wo_recursion(graph, graph.find_vertex_with_label_int(0), parent):
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


def counting_auth_tree_with_encoding(graph: "Graph"):
    new_graph = graph.clone_graph()
    root = find_root_tree(graph)
    level, trace = level_tree(new_graph, root)
    giaithua = [1]
    max_nei = 0
    for v in new_graph.vertices:
        max_nei = max(max_nei, len(v.neighbours))
    for i in range(1, max_nei + 5):
        giaithua.append(i * giaithua[i - 1])
    _, encoding_map = encode_tree_with_array(new_graph, root, level)

    return multipli_tree(new_graph, level, root, encoding_map, giaithua)


def has_cycle_at_v(graph: "Graph", v: "Vertex", p):
    global visited
    visited[v.label] = True
    for u in v.neighbours:
        if not visited[u.label]:
            if has_cycle_at_v(graph, u, v.label):
                return True
        elif u.label != p:
            return True
    return False


def has_cycle_at_v_wo_recursion(graph: "Graph", s: "Vertex", parent):
    global visited
    q = []
    q.append(s)
    while len(q) > 0:
        u = q.pop()
        visited[u.label] = True
        for v in u.neighbours:
            if not visited[v.label]:
                q.append(v)
                parent[v.label] = u.label
            elif v.label != parent[u.label]:
                return True
    return False
