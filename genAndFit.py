from gen import *
from fit import *
from multiprocessing import Pool

#def gen(seed, model_file, nBESIII, nLHCb, dataFolder, nCores = 12):
def genAndFit(fit_model_file, gen_model_file, seed, doMI, dataFolder, nCores=12):
    gen(seed, gen_model_file, 1, 10000, dataFolder, nCores)
    fit(fit_model_file, gen_model_file, seed, doMI, dataFolder, nCores)


def genAndFitN(fit_model_file, gen_model_file, seeds, doMI, dataFolder):
    for seed in seeds:
        genAndFit(fit_model_file, gen_model_file, seed, doMI, dataFolder)


def genAndFitMIMD(seed):
    dataFolder = "/mnt/m/qmi/gauss_shift_dd"
    dataFolder = "."
    gen(seed, "gauss_bias_1_medium.opt", 1, 10000, dataFolder, nCores=1)
#    fit("MI.opt", "gauss_bias_1_medium.opt", seed, True, dataFolder, nCores=1)
    fit("MD.opt", "base.opt", seed, False, dataFolder, nCores=1)


def genAndFitMIMD_10(seed):
    dataFolder = "/mnt/m/qmi/gauss_shift_dd"
    dataFolder = "."
    seeds = range(seed*10, (seed+1)*10)
   # genN(seeds, "base.opt", 1, 10000, dataFolder, nCores=1)
    #genN(seeds, "gauss_bias_1_low.opt", 1, 10000, dataFolder, nCores=1)
    #genN(seeds, "gauss_bias_1_medium.opt", 1, 10000, dataFolder, nCores=1)
    #genN(seeds, "gauss_bias_1_high.opt", 1, 10000, dataFolder, nCores=1)
#    fit("MI.opt", "gauss_bias_1_medium.opt", seed, True, dataFolder, nCores=1)

    fitN("poly_5.opt", f"gauss_bias_1_high.opt", seeds, False, dataFolder, nCores=12)
    #for model in ["gauss_bias_1", "gauss_bias_2"]:
    #    for scale in ["low", "medium", "high"]:
    #        fitN("MI.opt", f"{model}_{scale}.opt", seeds, True, dataFolder, nCores=1)



if __name__=="__main__":



    seeds = range(1)
    pool = Pool(processes=1)
    pool.map(genAndFitMIMD_10, list(seeds))
#    genAndFit("MD.opt", "base.opt", 80, True, ".")    
    

