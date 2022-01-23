from matplotlib import pyplot as plt
import numpy as np
from plotFromRoot import *
from rootTools import *

def plot1DProj(hist, histMC, pull, xlabel,output):
    n, b = hist.to_numpy()
    nMC, bMC = histMC.to_numpy()
    n = n/sum(n)
    nMC = nMC/sum(nMC)
    npull, bpull = pull.to_numpy()
    c,w = centerAndWidths(b)
    fig, ax = plt.subplots(2,1)
    ax[1].set_xlabel(xlabel)
    ax[0].bar(c, n, width=w, color="blue")
    ax[0].plot(c, nMC, color="red")
    ax[1].bar(c, npull, width=w)
    fig.savefig(output, dpi=300)

f = uproot.open("plots.root")
for tag in "KK Kppim Kmpip Kspi0 Kspipi Bp2Dhp Bm2Dhm".split():
    for c in "01 02 12".split():
        hist = f[f"{tag}_s{c}"]
        histMC = f[f"MC_{tag}_s{c}"]
        pull = f[f"Pull_MC_{tag}_s{c}"]
        plot1DProj(hist, histMC, pull, rf"$s_{{{c}}}$", f"{tag}_s{c}.png")
    
    
