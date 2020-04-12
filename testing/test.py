import os
import time
from algorithms.color_refinement import *
from algorithms.branching import *
from algorithms.isomorphic_automorphic_tree import *
from utils.graph_io import *
from algorithms.fast_color_refinement import *

def group_testing():
    with open(os.path.join(os.getcwd(), "../graphs/branching/cubes6.grl")) as f:
        G = load_graph(f, read_list=True)

        isomorphism_set = []
        for i in range(0, len(G[0]) - 1):
            for j in range(i + 1, len(G[0])):
                if is_in_same_set(isomorphism_set, i, j):
                    continue
                res = False
                if is_Tree(G[0][i]) and is_Tree(G[0][j]):
                    res = is_isomorphism_tree(G[0][i], G[0][j])
                else:
                    new_graph = G[0][i].__add__(G[0][j])
                    color_map = faster_color_refinement(new_graph, create_color_map(new_graph))
                    res = is_isomorphism(new_graph, color_map, G[0][i], G[0][j])
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

        for sett in isomorphism_set:
            if is_Tree(G[0][sett[0]]):
                res = counting_auth_tree_with_encoding(G[0][sett[0]])
                print(str(sett) + " " + str(res))
            else:
                new_graph = G[0][sett[0]].__add__(G[0][sett[1]])
                color_map = faster_color_refinement(new_graph, create_color_map(new_graph))
                res = count_isomorphism(new_graph, color_map, G[0][sett[0]], G[0][sett[1]])
                print(str(sett) + " " + str(res))


def color_ref_testing():
    with open(os.path.join(os.getcwd(), "../graphs/GraphsFastPartitionRefinement/threepaths10240.gr")) as f:
        G = load_graph(f)
        color_map = faster_color_refinement(G, create_color_map(G))
        # color_partition = create_single_color_partition(color_map)
        # print(color_map)
        # print(color_partition)
        print("-------------------------------------------")
        # color_map = color_refinement_with_initial_color_improved(G, create_color_map(G))
        # color_partition = create_single_color_partition(color_map)
        # print(color_map)
        # print(color_partition)
        # print("-------------------------------------------")
        # color_map = color_refinement_with_initial_color_basic(G, create_color_map(G))
        # color_partition = create_single_color_partition(color_map)
        # print(color_map)
        # print(color_partition)


start_time = time.time()
group_testing()
#color_ref_testing()
print("Running time: " + str(time.time() - start_time))
