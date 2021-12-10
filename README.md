How to run our codes:
- Our algorithms included in the folder algorithms
- To run our code, you can run the file python test.py
- in test.py, there are severals setting which can be maniplulated:
    - prefix: prefix to get to graphs folder
    - more_prefix: can be "" or "project_delivery/" in cases you want to run graphs which are posted on canvas or graph which are posted on delivery day
    - graph: just the name of the graph you want to run

    - flag:
        - flag_output_iso: output only isomorphism classes
        - flag_output_auto: output only automorphism for set of graphs
        - flag_output_iso_auto: output both isomorphism classes and their automorphism
        - flag_output_auto_single: output only one automorphism for single graph (which is the case of basicAut1 and basicAut2)
        - flag_output_graph: writing graph to dot file
        - flag_testing_tree: choosing to test tree and apply polynomial time algorithm for tree cases
        - flag_using_basic_algo: choosing between using basic color refinement and fast color refinement with pruning

- After every test, there will be answers and computation time

- Example:
    - To run basicGI1:
        - settings:
            prefix = "../graphs/"
            more_prefix = "project_delivery/" # "project_delivery/" or ""
            graph = "basicGI1"
            link = prefix + more_prefix + graph + ".grl"

            flag_output_iso = True
            flag_output_auto = False
            flag_output_iso_auto = False
            flag_output_auto_single = False
            flag_output_graph = False
            flag_testing_tree = True

            flag_using_basic_algo = False
        - result:
            Sets of isomorphic graphs:
            [0, 4]
            [1, 2, 5]
            [3, 6]
            [7, 8]
            Running time: 0.10601067543029785

    - To run basicAut1:
        - settings:
            prefix = "../graphs/"
            more_prefix = "project_delivery/" # "project_delivery/" or ""
            graph = "basicAut1"
            link = prefix + more_prefix + graph + ".grl"

            flag_output_iso = False
            flag_output_auto = False
            flag_output_iso_auto = False
            flag_output_auto_single = True
            flag_output_graph = False
            flag_testing_tree = True

            flag_using_basic_algo = False
        - result:
            Graph: Number of automorphisms:
            0:     512
            Running time: 0.22041058540344238

    - To run bigtrees3:
        - settings:
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
        - result:
            Sets of isomorphic graphs:  Number of automorphisms:
            [0, 2]                      2772351862699137701073289910157312
            [1, 3]                      462058643783189616845548318359552
            Running time: 0.1648571491241455
