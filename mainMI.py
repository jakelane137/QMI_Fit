from setupModel import main as setupModel
from gen import *
from fit import *
from pulls import makeAndPlotPulls
setupModel()

seeds = range(25)

def genAndFit(seeds, initial_model, dataFolder):
    for seed in seeds:
        gen(seed, initial_model, 1, 10000, dataFolder)
        fit("MI.opt", initial_model, seed, True, dataFolder)



#fitN("MI.opt", "poly_0.opt", seeds, True, "/mnt/m/qmi/gauss_shift_dd/")
#fitN("MI.opt", "gauss_bias_1_high.opt", seeds, True, "/mnt/m/qmi/gauss_shift_dd/")

#genAndFit(seeds, "poly_0.opt", "/mnt/m/qmi/gauss_shift_dd/")
#genAndFit(seeds, "gauss_bias_1_high.opt", "/mnt/m/qmi/gauss_shift_dd/")
#x, dx, x0, diff_x, pull_x = makePullN("MI.opt", "poly_0.opt", seeds, ".")

def find


if __name__=="__main__":
    seeds = range(50)
    makeAndPlotPulls("MI.opt", "base.opt", seeds, 7)
    makeAndPlotPulls("MD.opt", "base.opt", seeds, 7)

#    seeds = range(25)
    makeAndPlotPulls("MI.opt", "gauss_bias_1_high.opt", seeds, 7)
    makeAndPlotPulls("MD.opt", "gauss_bias_1_high.opt", seeds, 7)


