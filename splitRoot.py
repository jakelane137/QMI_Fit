import uproot3 
import numpy as np
fBESIII = uproot3.open("besiii100base.root")
tag = "KK"

signal_tuple = fBESIII[f"Signal_{tag}"]
tag_tuple = fBESIII[f"Tag_{tag}"]

signal_d = {}
tag_d = {}


signal_split = {}
tag_split = {}
NSplit=100
for k in list(signal_tuple.keys()):
    key = k.decode()
    signal_d[key] = np.array(signal_tuple[key].array())
    signal_split[key] = np.split(signal_d[key], NSplit)
for k in list(tag_tuple.keys()):
    key = k.decode()
    tag_d[key] = np.array(tag_tuple[key].array())

    tag_split[key] = np.split(tag_d[key], NSplit)


signal_tree_template = {}
tag_tree_template = {}
for k in list(signal_tuple.keys()):
    key = k.decode()
    signal_tree_template[key] = np.float64
for k in list(tag_tuple.keys()):
    key = k.decode()
    tag_tree_template[key] = np.float64


signal_tree_split = [uproot3.newtree(signal_tree_template) for i in range(NSplit)]
tag_tree_split = [uproot3.newtree(tag_tree_template) for i in range(NSplit)]

for i in range(NSplit):
    
    d_ext_sig = {}
    for k in list(signal_tuple.keys()):
        key = k.decode()
        d_ext_sig[key] = signal_split[key][i]
    signal_tree_split[i].extend(d_ext_sig)
    d_ext_tag = {}
    for k in list(tag_tuple.keys()):
        key = k.decode()
        d_ext_tag[key] = tag_split[key][i]

    tag_tree_split[i].extend(d_ext_tag)
 

