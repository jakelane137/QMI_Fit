import os
import numpy as np
from matplotlib import pyplot as plt
import glob
from pulls import  MIlogsFromGrid
from pulls import logsFromGrid
from opt2py import *
import matplotlib.pylab as pylab

name_idx_total = {}
jobId = 373
logs = logsFromGrid(jobId)
def makeCovFromLog(logFile):
    full_matrix = []
    free_index = []
    names = []
    i = 0
    with open(logFile) as f:
        for line in f:
            
            if "Parameter" in line:
                row = []
                a = line.split()
                name = a[1]
                flag = a[2]
                mean = float(a[3])
                err = float(a[4])
                row = []
                print(a)
                for _a in a[5:]:
                    row += [float(_a)]
                if flag == "Free":
                    #free_index += [i]

                    free_index += [i]
                    name_idx_total[name] = i
                i+=1
                full_matrix += [row]
                names += [name]
#    free_cov_matrix = np.matrix(free_cov)
    return  names , full_matrix, free_index


names, full_matrix, free_index = makeCovFromLog(logs[0])

m = np.matrix(full_matrix)
M = np.array(m)
d = np.array(m.diagonal())[0]
idx_nonZero = d.nonzero()[0]
name_idx=[]
M2 = []
 
name_d = {}

i2 = 0
                

for i in idx_nonZero:
#    print(f"len(M[{i}]) = {len(M[i])}")
    name_idx += [i]
    name_d[names[i]] = i2
    i2 +=1

    row = []
    for j in idx_nonZero:
 #       print(f"M[{i}][{j}] = {M[i][j]}")
        row += [M[i][j]]

    M2 += [row]


m2 = np.matrix(M2)
d2 = np.array(m2.diagonal())[0]
corr = np.corrcoef(m2)


corr_ordered = []
names_ordered = []
order = 9
for o in range(order+1):
    for i in range(o +1 ):
        for j in range(o + 1-i):
            name = f"PhaseCorrection::C{i}_{2 * j+1}"
            if i+j==o:
                names_ordered += [name]



names_ordered += ["pCoherentSum::x+"]
names_ordered += ["pCoherentSum::y+"]
names_ordered += ["pCoherentSum::x-"]
names_ordered += ["pCoherentSum::y-"]

for name1 in names_ordered:
    corr_ordered_row = []
    for name2 in names_ordered:
        idx1 = name_d[name1]
        idx2 = name_d[name2]
        corr_ordered_row += [corr[idx1][idx2]]
    corr_ordered += [corr_ordered_row]


corr_ordered = np.array(corr_ordered)

f,a = plt.subplots(1,1)
sc  = a.imshow(corr_ordered)
cb = plt.colorbar(sc, ax=a)
a.set_xticks([i for i in range(len(names_ordered))])
a.set_yticks([i for i in range(len(names_ordered))])
a.set_xticklabels([rf"${param2Tex(name)}$" for name in names_ordered])
a.set_yticklabels([rf"${param2Tex(name)}$" for name in names_ordered])

plt.xticks(rotation=90, fontsize=5)
plt.yticks(fontsize=5)
params = {'legend.fontsize': 'x-small',
#          'figure.figsize': (15, 5),
#        'axes.labelsize': 'x-small',
#         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-small',
         'ytick.labelsize':'x-small'}
pylab.rcParams.update(params)


f.savefig(f"/eos/home-j/jolane/corr{jobId}.png", dpi=300)




