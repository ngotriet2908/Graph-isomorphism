import os
import time
from algorithms.color_refinement import *
from algorithms.branching import *
from algorithms.isomorphic_automorphic_tree import *
from utils.graph_io import *


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
                # with open(os.path.join(os.getcwd(), 'name.dot'), 'w') as f:
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
                # with open(os.path.join(os.getcwd(), 'name.dot'), 'w') as f:
                #     write_dot(new_graph, f)
                # print(create_color_partition(color_map))
                res = is_isomorphism_tree(G[0][i], G[0][j])
                if res:
                    start_time_aut = time.time()
                    print(
                        "Compare " + str(i) + " and " + str(j) + " : " + str(counting_auth_tree_with_encoding(G[0][i])))


def testing_tree():
    with open(os.path.join(os.getcwd(), "../graphs/branching/trees36.grl")) as f:
        G = load_graph(f)
        color_map = color_refinement_with_initial_color(G, create_color_map(G))
        print(color_map)
        # for g in G[0]:


start_time = time.time()
testing_counting_tree()
print("Running time: " + str(time.time() - start_time))
