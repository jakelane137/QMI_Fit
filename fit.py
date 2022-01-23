#!/bin/python3
from setupScripts import *
import os
def fit(fit_model_file, gen_model_file, seed, doMI, dataFolder, nCores=1):
    print(f"Fitting {gen_model_file} generated events with {fit_model_file}, seed = {seed}")
    env = fitEnv(fit_model_file, gen_model_file, seed, dataFolder, nCores)
    if doMI:
        cmd = os.system(f"{env} ./fitMI.sh")
    else:
        cmd = os.system(f"{env} ./fit.sh")

def fitN(fit_model_file, gen_model_file, seeds, doMI, dataFolder, nCores=12):
    for seed in seeds:
        fit(fit_model_file, gen_model_file, seed, doMI, dataFolder, nCores)





        

if __name__=="__main__":
   # seeds = range(100)
   # fitN("MD.opt", "base.opt", seeds, False, "/mnt/m/qmi/gauss_shift_dd/")

    seeds = range(100)
#    fitN("poly_3.opt", "gauss_bias_1_high.opt", seeds, False, "/mnt/m/qmi/gauss_shift_dd/")
    #fitN("MD.opt", "gauss_bias_1_high.opt", seeds, False, "/mnt/m/qmi/gauss_shift_dd/")
#    fitN("MI.opt", "base.opt", seeds, True, ".")
    #fit("MI.opt", "gauss_bias_1_low.opt", 0, True, ".")
    #fitN("MD.opt", "base.opt", seeds, False, ".")
#    fitN("MI.opt", "base.opt", seeds, True, ".")
    fit("poly_10.opt", "gauss_bias_1_high.opt", 80, False, ".")
#    fitN("MD.opt", "poly_0.opt", [0], False)
#    fitN("poly_0.opt", "poly_0.opt", [0], False)

