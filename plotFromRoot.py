from matplotlib import pyplot as plt
import uproot
import numpy as np 
from rootTools import *

from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import argparse

def colorMapWhiteZero():
    viridis = cm.get_cmap('viridis', 256)
    newcolors = viridis(np.linspace(0, 1, 256))
    white = np.array([256/256, 256/256, 256/256, 1])
    newcolors[:1, :] = white
    newcmp = ListedColormap(newcolors)
    return newcmp

def centerAndWidths(b):
    c = 0.5*(b[1:]+b[:-1])
    w = 0.7*(c[1] - c[0])
    return c, w

def plotDalitzHist1D(x, nbins, output, xlabel=r"$s_{01}$"):
    n, b1 = np.histogram(x, bins=nbins, density=True)
    print(f"N(n) = {len(n)} N(b1) = {len(b1)}")
    c1, w1 = centerAndWidths(b1)

    print(f"N(c1) = {len(c1)}")
    fig, ax = plt.subplots(1,1)
#    sc = ax.scatter(c1, c2, c=n,s=w1)

    ax.bar(c1, n1, width=w1)
    ax.set_xlabel(xlabel)



    fig.savefig(f"{output}", dpi=300)
    plt.close()


def plotDalitzHist2D(s12, s13, nbins, output):
    n, b1, b2 = np.histogram2d(s12, s13, bins=nbins, density=True)
    print(f"N(n) = {len(n)} N(b1) = {len(b1)}")
    c1, w1 = centerAndWidths(b1)
    c2, w2 = centerAndWidths(b2)
    print(f"N(c1) = {len(c1)}")
    fig, ax = plt.subplots(1,1)
#    sc = ax.scatter(c1, c2, c=n,s=w1)
    extent = (min(c1), max(c1), min(c2), max(c2))
    sc = ax.imshow(n, extent=extent, cmap=colorMapWhiteZero(), origin="lower")
    ax.set_xlabel(r"$s_{12}$")
    ax.set_ylabel(r"$s_{13}$")
    plt.colorbar(sc, ax=ax)
    ax.set_aspect("equal")
    fig.savefig(f"{output}", dpi=300)
    plt.close()


def plotAmpVal2D(s12, s13, z, output):
    diff13 = max(s13) -  min(s13)
    fig, ax = plt.subplots(1,1)
    sc = ax.scatter(s12, s13, c=z, s = 1, marker=".", alpha=1)
    plt.colorbar(sc, ax=ax)
    ax.set_aspect("equal")
    plt.savefig(f"{output}", dpi=300)
    plt.close()



def doPlots(rootFile, Output, tagName, isBESIII):
    f = uproot.open(rootFile)
    tDalitzName = ""
    tAmpName = ""
    if isBESIII:
        tDalitzName = f"Signal_{tagName}"
        tAmpName = f"Tag_{tagName}_vals"
    else:
        tDalitzName = f"{tagName}"
        tAmpName = f"{tagName}_vals"

    tDalitz = f[tDalitzName]
    tAmp = f[tAmpName]
    s12, s13, s23 = getKspipiDalitz(tDalitz)
    amp = getKspipiAmp(tAmp)
    
    
    plotDalitzHist1D(s12,int(0.05*len(s12)), f"{Output}_s12.png", r"$s_{12}$")
    plotDalitzHist1D(s13,int(0.05*len(s13)), f"{Output}_s13.png", r"$s_{13}$")
    plotDalitzHist1D(s23,int(0.05*len(s23)), f"{Output}_s23.png", r"$s_{23}$")
    plotDalitzHist2D(s12, s13, int(0.05*len(s12)), f"{Output}_s12_s13.png")
    plotAmpVal2D(s12, s13, amp["dd"], f"{Output}_dd.png")
    plotAmpVal2D(s12, s13, amp["f"], f"{Output}_f.png")
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file",default="besiii.root", nargs="?")
    parser.add_argument("output",default="besiii", nargs="?")
    parser.add_argument("tag",default="KK", nargs="?")
    parser.add_argument("isBESIII",default=True, nargs="?")
    args = parser.parse_args()
    print(args.file)
    print(args.output)
    doPlots(args.file, args.output, args.tag, args.isBESIII)

if __name__=="__main__":
    main()
    

