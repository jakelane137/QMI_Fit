import os
from matplotlib import pyplot as plt
import numpy as np
def printZ(model_file):
    output = model_file.replace(".opt", "Z.txt")
    os.system(f"MI --printZ true --DataSample null --printZOut {output} --EventType 'D0 K0S0 pi- pi+' {model_file}")


def plotZ(model_file):
    z_file = model_file.replace(".opt", "Z.txt")
    output = model_file.replace(".opt", "Z.png")
    c = []
    s = []
    b = []
    cP = []
    sP = []
    with open(z_file) as f:
        for line in f:
            a = line.split()
            _b, _c, _s, _cP, _sP = a
            b += [int(_b)]
            c += [float(_c)]
            s +=[float(_s)]
            cP += [float(_cP)]
            sP += [float(_sP)]
    fig, ax = plt.subplots(1,1)
    t = np.linspace(0, 2 * np.pi, 1000)
    ax.plot(np.cos(t), np.sin(t), color="blue")
    ax.scatter(c, s, marker=".", color="blue" ,label=r"$c_i + i s_i$ from $\Delta \delta_D$")
    ax.scatter(cP, sP, marker="x", color="red", label=r"$c_i + i s_i$ from $\Delta \delta_D + f_{bias}$")
    for i in range(len(c)):
        ax.annotate(str(b[i]), (c[i], s[i]))
        ax.annotate(str(b[i]), (cP[i], sP[i]))
    ax.set_xlabel(r"$c_i$")
    ax.set_ylabel(r"$s_i$")
    ax.legend()
    ax.set_aspect("equal")
    fig.savefig(output, dpi=300)
    plt.close()



def printZAll():
    printZ("base.opt")
    plotZ("base.opt")
    for bias in "gauss_bias_1 gauss_bias_2".split():
        for scale in "low medium high".split():
            printZ(f"{bias}_{scale}.opt")
            plotZ(f"{bias}_{scale}.opt")


if __name__=="__main__":
    printZAll()

