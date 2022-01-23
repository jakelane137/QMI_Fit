import os
import numpy as np
import uproot
import pandas as pd


def makeAmpFolder(optFile, folder, dataSample, input_prefix, output_prefix):
    os.system(f"mkdir -p {folder}")
    outputDataAmp = dataSample.replace(".root", f"{output_prefix}_values.root")
    cmd = f"ampToTuple --DataSample {dataSample}{input_prefix} --OutputDataAmp {folder}/{outputDataAmp} --OutputNormAmp {folder}/Norm.root {optFile}"
    os.system(cmd)

def treeToDict(t):
    d = {}
    for key in list(t.keys()):
        d[key] = np.array(t[key].array())
    
    return d


def tupleToDict(fileName):
    f = uproot.open(fileName)
    v = f["Values"]
    d = treeToDict(v)
    return d



class amplitude:
    def __init__(self, d, dNorm):
        self.values = d
        self.values_norm = dNorm
        self.A = self.values["aR"] + 1j * self.values["aI"]
        self.C = self.values["cR"] + 1j * self.values["cI"]
        self.norm_A = self.values_norm["aR"] + 1j * self.values_norm["aI"]
        self.norm_C = self.values_norm["cR"] + 1j * self.values_norm["cI"]

        self.sum_A = sum(np.abs(self.values["aR"] + 1j * self.values["aI"]), 2)
        self.sum_C = sum(np.abs(self.values["cR"] + 1j * self.values["cI"]), 2)

        self.sum_norm_A = sum(np.abs(self.values_norm["aR"] + 1j * self.values_norm["aI"]), 2)
        self.sum_norm_C = sum(np.abs(self.values_norm["cR"] + 1j * self.values_norm["cI"]), 2)





        

        