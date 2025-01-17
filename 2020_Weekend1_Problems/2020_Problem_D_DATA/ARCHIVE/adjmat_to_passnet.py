
import re
from d import *

# for each index in the mat
# first index is Origin player
# second index is Destination player

def directed_network(m):
    print("source,target,weight")
    for src,src_row in enumerate(m.diadjmat):
        for dst,cardinality in enumerate(src_row):
            src_name = m.idx_to_name[src]
            dst_name = m.idx_to_name[dst]
            print(f"{src_name},{dst_name},{cardinality}")

def color_node_by_pos():
    pass

def print_nodes_with_colors():
    pass

def undirected_network(m):
    print("source,target,weight")
    for src,src_row in enumerate(m.uadjmat):
        src_name = m.idx_to_name[src]
        for k in range(src):
            dst_name = m.idx_to_name[k]
            cardinality = m.uadjmat[src, k]
            if cardinality > 0:
                print(f"{src_name},{dst_name},{cardinality}")


if __name__ == '__main__':
    # directed_network()
    undirected_network()
