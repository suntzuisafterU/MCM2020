import sys

from functools import *
import operator

import matplotlib.pyplot as plt

from globals import *
from connectivity_matrix import *

# accept a play or glob and build one big DiMat


if __name__ == '__main__':
    # and the following code block is not needed
    # but we want to see which module is used and
    # if and why it fails
    try:
        import pygraphviz
        from networkx.drawing.nx_agraph import write_dot

        print("using package pygraphviz")
    except ImportError:
        try:
            import pydot
            from networkx.drawing.nx_pydot import write_dot

            print("using package pydot")
        except ImportError:
            print()
            print("Both pygraphviz and pydot were not found ")
            print("see  https://networkx.github.io/documentation/latest/reference/drawing.html")
            print()
            raise

    if len(sys.argv) > 2:
        if len(sys.argv) == 1:
            print("Enter more args man")
            exit(-69)
        plays = read_glob_of_plays(sys.argv[1])
        out_path = sys.argv[2]
    else:
        plays = read_glob_of_plays("data/games/game*")
        out_path = "data/dotgraphs/allgames"

    allplays = reduce(operator.add, plays, [])

    df_dimat = local_dimat_df(allplays)

    DG = nx.DiGraph(df_dimat)

    threshold = 20
    degs = [d for d in DG.degree()]
    to_remove = (n for n, d in degs if d < threshold)
    DG.remove_nodes_from( to_remove )

    write_dot(DG, out_path)

    # mat plot lib stuff

    spectral_layout = nx.spectral_layout(DG)
    sprint_layout = nx.spring_layout(DG)

    E = [e for e in DG.edges]
    colors = [DG.get_edge_data(*e)['weight'] for e in E]
    print(colors)




    for name in plt.cm.cmaps_listed:
        print(name)

    options = {
        "layout" :  spectral_layout,
        "node_color": "#A0CBE2",
        "edge_color": colors,
        "width": 4,
        "edge_cmap": plt.cm.get_cmap("magma")
    }
    nx.draw_networkx(DG, **options)
    plt.show()



