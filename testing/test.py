import os
import time
from algorithms.color_refinement import *
from algorithms.branching import *
from algorithms.isomorphic_automorphic_tree import *
from utils.graph_io import *
from algorithms.fast_color_refinement import *
from algorithms.count_auth import *
from utils.output_result import *

prefix = "../graphs/"
more_prefix = "" # "project_delivery/" or ""
graph = "bigtrees3"
link = prefix + more_prefix + graph + ".grl"

flag_output_iso = False
flag_output_auto = False
flag_output_iso_auto = True
flag_output_auto_single = False
flag_output_graph = False
flag_testing_tree = True

flag_using_basic_algo = False


def group_testing():
    with open(os.path.join(os.getcwd(), link)) as f:
        G = load_graph(f, read_list=True)
        output_iso_auto(G[0], flag_testing_tree, flag_using_basic_algo)

        if flag_output_graph:
            with open(os.path.join(os.getcwd(), graph + '.dot'), 'w') as f:
                write_dot(G[0][0], f)


def auto_testing():
    with open(os.path.join(os.getcwd(), link)) as f:
        G = load_graph(f, read_list=True)
        output_automorphism(G[0])

        if flag_output_graph:
            with open(os.path.join(os.getcwd(), graph + '.dot'), 'w') as f:
                write_dot(G[0][0], f)


def auto_testing_single_test():
    with open(os.path.join(os.getcwd(), prefix + more_prefix + graph + ".gr")) as f:
        G = load_graph(f)
        output_automorphism([G])

        if flag_output_graph:
            with open(os.path.join(os.getcwd(), graph + '.dot'), 'w') as f:
                write_dot(G[0][0], f)


def iso_testing():
    with open(os.path.join(os.getcwd(), link)) as f:
        G = load_graph(f, read_list=True)
        # output_isomorphism(G[0])
        output_isomorphism_improved(G[0])

        if flag_output_graph:
            with open(os.path.join(os.getcwd(), graph + '.dot'), 'w') as f:
                write_dot(G[0][0], f)


start_time = time.time()
if flag_output_iso:
    iso_testing()
if flag_output_auto:
    auto_testing()
if flag_output_iso_auto:
    group_testing()
if flag_output_auto_single:
    auto_testing_single_test()

print("Running time: " + str(time.time() - start_time))
