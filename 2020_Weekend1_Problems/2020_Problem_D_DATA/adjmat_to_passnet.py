
from d import *

# for each index in the mat
# first index is Origin player
# second index is Destination player

for src,src_row in enumerate(diadjmat):
    for dst in src_row:
        src_name = idx_to_name[src]
        dst_name = idx_to_name[dst]
        print(f"{src_name},{dst_name},{diadjmat[src,dst]}")
