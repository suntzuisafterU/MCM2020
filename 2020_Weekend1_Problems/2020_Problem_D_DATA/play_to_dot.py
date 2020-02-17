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
        plays = read_glob_of_plays("data/games/game01*")
        out_path = "data/dotgraphs/game01"

    allplays = reduce(operator.add, plays, [])

    df_dimat = local_dimat_df(allplays)

    DG = nx.DiGraph(df_dimat)

    write_dot(DG, out_path)

    # mat plot lib stuff

    layout = nx_spectral_layout(allplays)
    nx.draw_networkx(DG, layout=layout)

    plt.show()



