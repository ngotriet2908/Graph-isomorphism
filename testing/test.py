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
graph = "cographs1"
link = prefix + graph + ".grl"

flag_output_iso      = True
flag_output_auto     = True
flag_output_iso_auto = True

def group_testing():
    with open(os.path.join(os.getcwd(), link)) as f:
        G = load_graph(f, read_list=True)
        output_iso_auto(G[0])


def auto_testing():
    with open(os.path.join(os.getcwd(), link)) as f:
        G = load_graph(f, read_list=True)
        output_automorphism(G[0])


def iso_testing():
    with open(os.path.join(os.getcwd(), link)) as f:
        G = load_graph(f, read_list=True)
        output_isomorphism(G[0])


start_time = time.time()
if flag_output_iso:
    iso_testing()
if flag_output_auto:
    auto_testing()
if flag_output_iso_auto:
    group_testing()
print("Running time: " + str(time.time() - start_time))
