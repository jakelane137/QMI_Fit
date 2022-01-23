import numpy as np
from modelToArray import *
import zfit
from PhaseCorrection import *
import pandas as pd
from Psi3770 import *
from BtoDh import *
from gen import *

model_file = "base.opt"
dataFolder = "."
model_pref = model_file.replace(".opt", "")
seed = 0
nBESIII=1
nLHCb=2000
BESIII_File = f"{dataFolder}/besiii{seed}{model_pref}.root"
LHCB_File = f"{dataFolder}/lhcb{seed}{model_pref}.root"
#gen(seed=seed, model_file=model_file, nBESIII=nBESIII, nLHCb=nLHCb, dataFolder=dataFolder)
tag = "KK"
#makeAmpFolder(model_file, model_pref, BESIII_File, f":Signal_{tag}", tag)
tag = "Bp2Dhp"
#makeAmpFolder(model_file, model_pref, LHCB_File, f":{tag}", tag)


tag = "KK"
data_KK_amp_df = pd.DataFrame(tupleToDict(f"{model_pref}/besiii{seed}{model_pref}{tag}_values.root"))
tag = "Bp2Dhp"
data_Bp2Dhp_amp_df = pd.DataFrame(tupleToDict(f"{model_pref}/lhcb{seed}{model_pref}{tag}_values.root"))
norm_amp_df = pd.DataFrame(tupleToDict(f"{model_pref}/Norm.root"))


amp_KK = amplitude(data_KK_amp_df, norm_amp_df)

C = {}
Order = 9
for i in range(Order +1):
    for j in range(Order +1-i):
        C[f"{i}_{2*j+1}"] = zfit.Parameter(f"C{i}_{2*j+1}",0)
        C[f"{i}_{2*j+1}"] = 0

corr = correction(C, Order)

