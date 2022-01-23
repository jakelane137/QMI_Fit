import uproot
import numpy as np

from rootTools import *

ref_file = uproot.open("ref_equal.root")
besiiiFile = uproot.open("besiii0poly_0.root")
lhcbFile = uproot.open("lhcb0poly_0.root")
nBins = 8
bins = [i for i in range(1,nBins +1 )] + [-i for i in range(1, nBins +1)]
s12R={}
s13R = {}
for b in bins:
    k = b
    if b<0:
        k = f"m{abs(b)}"
    s12R[f"{b}"] = np.array(ref_file[f"bin{k}"]["s01"].array())
    s13R[f"{b}"] = np.array(ref_file[f"bin{k}"]["s02"].array())

s12 = {}
s13 = {}
s23 = {}


for tag in "KK Kspi0 Kppim Kmpip".split():
    _s12, _s13, _s23 = getKspipiDalitz(besiiiFile[f"Signal_{tag}"])
    s12[tag] = _s12
    s13[tag] = _s13
    s23[tag] = _s23


s12[f"Kspipi_Signal"], s13[f"Kspipi_Signal"], s23["Kspipi_Signal"] = getKspipiDalitz(besiiiFile[f"Signal_Kspipi"])
#s12[f"Kspipi_Tag"], s13[f"Kspipi_Tag"], s23["Kspipi_Tag"] = getKspipiDalitz(besiiiFile[f"Tag_Kspipi"])


for tag in "Bp2Dhp Bm2Dhm".split():
    _s12, _s13, _s23 = getKspipiDalitz(lhcbFile[f"{tag}"])
    s12[tag] = _s12
    s13[tag] = _s13



ds = lambda x, y, x0, y0: min((x - x0)**2 + (y - y0)**2)

bin_Bp = [bins[np.argmin([ds(s12["Bp2Dhp"][i], s13["Bp2Dhp"][i], s12R[f"{b}"], s13R[f"{b}"]) for b in bins])] for i in range(len(s12["Bp2Dhp"]))]


