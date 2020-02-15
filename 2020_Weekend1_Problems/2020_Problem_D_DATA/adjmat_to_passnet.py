
from d import *

# for each index in the mat
# first index is Origin player
# second index is Destination player

def directed_network():
    for src,src_row in enumerate(diadjmat):
        for dst,cardinality in enumerate(src_row):
            src_name = idx_to_name[src]
            dst_name = idx_to_name[dst]
            print(f"{src_name},{dst_name},{cardinality}")


def undirected_network():
    for src,src_row in enumerate(uadjmat):
        src_name = idx_to_name[src]
        for k in range(src):
            dst_name = idx_to_name[k]
            cardinality = uadjmat[src, k]
            if cardinality > 0:
                print(f"{src_name},{dst_name},{cardinality}")


if __name__ == '__main__':
    # directed_network()
    undirected_network()
