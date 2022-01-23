from setupScripts import *
import os

def gen(seed, model_file, nBESIII, nLHCb, dataFolder, nCores = 12):
    print(f"Generating {nBESIII + nLHCb} ({nBESIII} BESIII + {nLHCb} LHCb) events with {model_file}, the files will be in {dataFolder}")
    env = genEnv(model_file, seed, nBESIII, nLHCb, dataFolder, nCores)
    cmd = os.system(f"{env} ./gen.sh")

def genN(seeds, model_file, nBESIII, nLHCb, dataFolder, nCores=12):
    for seed in seeds:
        gen(seed, model_file, nBESIII, nLHCb, dataFolder, nCores)


def genThreaded(seed, model_file, nBESIII, nLHCb, dataFolder, nCores = 12):
    print(f"Generating {nBESIII + nLHCb} ({nBESIII} BESIII + {nLHCb} LHCb) events with {model_file}, the files will be in {dataFolder}")
    env = genEnv(model_file, seed, nBESIII, nLHCb, dataFolder, nCores)
    cmd = os.system(f"{env} ./gen.sh &")


def genNThreaded(model_file, nBESIII, nLHCb, dataFolder, nCores=12):
    for core in range(nCores):
        seed = core
        genThreaded(seed, model_file, nBESIII, nLHCb, dataFolder, nCores=1)

    







if __name__=="__main__":
    gauss_loc_1 = {"muX":1.0,"muY":1.25, "sigmaX":0.025, "sigmaY":0.5}
    gauss_loc_2 = {"muX":0.75,"muY":2.5, "sigmaX":0.1, "sigmaY":0.1}
    gauss_biases = {"gauss_bias_1":gauss_loc_1, "gauss_bias_2":gauss_loc_2}
    seeds = range(20,100)
    scales = ["low", "medium", "high"]
    nBESIII = 1
    nLHCb = 10000
    dataFolder = "/mnt/m/qmi/gauss_shift_dd/"
    dataFolder = "."
    modelFile = "base.opt"
#    gen(100, modelFile, 100*nBESIII, 100*nLHCb, dataFolder)
    #genN(seeds, modelFile, nBESIII, nLHCb, dataFolder)


    for biasName in ["gauss_bias_2"]:
        for scale in scales: 
            modelFile = f"{biasName}_{scale}.opt"

            #gen(100, modelFile, 100*nBESIII, 100*nLHCb, dataFolder)
#
            genN(seeds, modelFile, nBESIII, nLHCb, dataFolder)
