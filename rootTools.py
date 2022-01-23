import uproot
import numpy as np 


def tree2Arr(tree,branch):
    return np.array(tree[branch].array())

def getP4(tree, part):
    p = {}
    for c in "E Px Py Pz".split():
        p[c] = tree2Arr(tree, f"{part}_{c}")
    return p

def addP4(p1, p2):
    p ={}
    for c in p1:
        p[c] = p1[c] + p2[c]
    return p

def mulP4(p1, p2):
    mul12 = [ p1[c] * p2[c] for c in "E Px Py Pz".split()]
    return mul12[0] - sum(mul12[1:])

def getKspipiDalitz(tree):
    p1 = getP4(tree, "_1_K0S0")
    p2 = getP4(tree, "_2_pi#")
    p3 = getP4(tree, "_3_pi~")

    p12 = addP4(p1, p2)
    p13 = addP4(p1, p3)
    p23 = addP4(p2, p3)

    s12 = mulP4(p12, p12)
    s13 = mulP4(p13, p13)
    s23 = mulP4(p23, p23)

    return s12, s13, s23




def getKspipiAmp(tree):
    d = {}
    for k in "a c psi".split():
        R = tree2Arr(tree, f"{k}R")
        I = tree2Arr(tree, f"{k}R")
        d[k] = R + 1j * I
    for k in "dd f df".split():
        d[k]= tree2Arr(tree, f"{k}")
    return d

    
if __name__=="__main__":
    f = uproot.open("besiii0poly_0.root")
    tDalitz = f["Signal_Kppim"]
    tAmp = f["Tag_Kppim_vals"]
    s12, s13, s23 = getKspipiDalitz(tDalitz)
    amp = getKspipiAmp(tAmp)
    print(f"Have {len(s12)} events")
    

