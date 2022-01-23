import os
import numpy as np
from matplotlib import pyplot as plt
from plotFromRoot import centerAndWidths
import scipy.stats
from opt2py import param2File, param2Tex
from fit import *
from gen import *
import glob


def makePullFromLog(logFile, gen_model_file):
    x0 = {}
    x = {}
    dx = {}
    diff_x = {}
    pull_x = {}
    gen_model = gen_model_file.split(".opt")[0]

    with open(gen_model_file) as f:
        for line in f:
            a = line.split()

            if "Free" in a or "Fix" in a and len(a)==4:
#                print(line)
                name, flag, v, dv = a
                x0[name] = float(v)

   
    if "MI" in logFile:
        Zfile = f"baseZ.txt"
        with open(Zfile) as f:
            for line in f:
                a = line.split()
                b = a[0]
                c = float(a[1])
                s = float(a[2])
                cP = float(a[3])
                sP = float(a[4])
                x0[f"c_{b}"] = cP
                x0[f"s_{b}"] = sP

    status = -1
                

    with open(logFile) as f:
        for line in f:
            a = line.split()
            if "Free" in line or "PhaseCorrection::C" in line:
                name = a[1]
                flag = a[2]
                v = float(a[3])
                dv = float(a[4])
                x[name] = v
                dx[name] =dv
            if "FitQuality" in line:
                status = int(a[5])
 
    
    for name in x:
        if "PhaseCorrection" in name:
            x0[name] = 0
       else:
            _x0 = x0[name]
        diff_x[name] = x[name] - x0[name]
        if dx[name]!=0:
            pull_x[name] = diff_x[name]/dx[name]
        else:
            pull_x[name] = diff_x[name]
    return x, dx, x0, diff_x, pull_x, status





def makePull(fit_model_file, gen_model_file, seed, folder="."):
    gen_model = gen_model_file.replace(".opt", "")
    fit_model = fit_model_file.replace(".opt", "") 
    logFile = f"{folder}/Fit_{fit_model}_to_{gen_model}_{seed}.log"
    x0 = {}
    x = {}
    dx = {}
    diff_x = {}
    pull_x = {}

    return makePullFromLog(logFile, gen_model_file)


def makePullN(logFiles, gen_model_file):
    x0 = {}
    x = {}
    dx = {}
    diff_x = {}
    pull_x = {}

    _X, _dX, _X0, _diff, _pull, _status = makePullFromLog(logFiles[0], gen_model_file)
    for key in _X:
        x0[key] = []
        x[key] = []
        dx[key] = []
        diff_x[key] = []
        pull_x[key] = []

    max_order = 100
    for i in range(max_order + 1):
        for j in range(max_order + 1 - i):
            key = f"PhaseCorrection::C{i}_{2*j+1}"
            x0[key] =[]
            x[key] =[]
            dx[key] =[]
            diff_x[key] =[]
            pull_x[key] =[]


    for logFile in logFiles:
        _X, _dX, _X0, _diff, _pull, _status = makePullFromLog(logFile, gen_model_file)
        print(_X0.keys())
        print(_X.keys())
        print(_X0)
        print(logFile)
        if _status != 0:
            print(_status)
        for key in _X:
                if "PhaseCorrection" in key:
                    x0[key] += [0]
                else:
                    x0[key] += [_X0[key]]
                x[key] += [_X[key]]
                dx[key] += [_dX[key]]
                diff_x[key] += [_diff[key]]
                pull_x[key] += [_pull[key]]
                print(f"len({key}) = {len(x[key])}")
    return x, dx, x0, diff_x, pull_x


def pullStats(p):
    mu = {}
    sigma = {}
    dmu= {}
    dsigma = {}
    for k in p:
        mu[k] = np.mean(p[k])
        sigma[k] = np.std(p[k])
        dmu[k] = sigma[k]/np.sqrt(len(p[k]))
        dsigma[k] = sigma[k]/np.sqrt(2*len(p[k]))
    return mu, sigma, dmu, dsigma

def plotPulls(p, output, nbins):
    mu, sigma, dmu, dsigma = pullStats(p)
    for k in p:
        if (len(p[k]) > 0):
            fig, ax = plt.subplots(1,1)
            n, b = np.histogram(p[k], bins=nbins, density=True)
            c, w = centerAndWidths(b)
            x = np.linspace(min(c), max(c), 1000)
            pdf = scipy.stats.norm(mu[k], sigma[k])
            y = pdf.pdf(x)
            dy2 = pdf.pdf(x)**2 * ( (x - mu[k])**2 * dmu[k]**2/sigma[k]**4 + ( (x - mu[k])**2 - sigma[k]**2)**2 * dsigma[k]**2/sigma[k]**6 )
            dy = np.sqrt(dy2)
            ax.bar(c, n, width=w)
            ax.plot(x, y, label=rf"""$\mu = {mu[k]:.3f} \pm {dmu[k]:.3f}$
    $\sigma = {sigma[k]:.3f} \pm {dsigma[k]:.3f}$""", color="red")
            ax.plot(x, y - dy, color="red", linestyle="dashed")
            ax.plot(x, y + dy, color="red", linestyle="dashed")
            ax.set_xlabel(rf"${param2Tex(k)}$")
            ax.legend()
            fig.savefig(f"{output}_{param2File(k)}.png", dpi=300)
            plt.close()



def plotVals(x, x0, output, nbins):

    mu, sigma, dmu, dsigma = pullStats(x)
    for k in x:
        if (len(x[k]) > 0):
            fig, ax = plt.subplots(1,1)
            n, b = np.histogram(x[k], bins=nbins, density=True)
            c, w = centerAndWidths(b)
            ax.bar(c, n, width=w, label=rf"""$ \mu = {mu[k]:.3f} \pm {dmu[k]:.3f}$
    $\sigma = {sigma[k]:.3f} \pm {dsigma[k]:.3f}$""", color="red")
            ax.bar([x0[k][0]], [max(n)], width=w, label=rf"${param2Tex(k)} = {x0[k][0]:.3f}$")
            ax.set_xlabel(rf"${param2Tex(k)}$")
            ax.legend()
            fig.savefig(f"{output}_{param2File(k)}.png", dpi=300)
            plt.close()



def makeAndPlotPulls(logFiles, fit_model, initial_model_file,  nbins,  outfolder = "."):
    if len(logFiles)==0:
        return

    initial_model = initial_model_file.replace(".opt", "")
    output = f"{fit_model}_to_{initial_model}"
    x, dx, x0, diff_x, pull_x = makePullN(logFiles, initial_model_file)

    for k in x:
        if(len(x[k]) > 0):
            print(f"Have {len(x[k])} pulls")
            print(f"m({k}) = {np.mean(pull_x[k])} {np.std(pull_x[k])} {np.std(pull_x[k])/np.sqrt(len(x[k]))}")
    os.system(f"mkdir -p {outfolder}/pull")
    os.system(f"mkdir -p {outfolder}/val")
    os.system(f"mkdir -p {outfolder}/err")
    plotPulls(pull_x, f"{outfolder}/pull/{output}", nbins)
    plotVals(x, x0, f"{outfolder}/val/{output}", nbins)
    plotVals(dx, dx, f"{outfolder}/err/{output}", nbins)



def logsFromGrid(job):
    folder = "/afs/cern.ch/work/j/jolane/gangadir/workspace/jolane/LocalXML/"
    #os.system(f"ls {folder}/{job}/*/*")
    raw_logs= glob.glob(f"{folder}/{job}/*/*/*.log")
    ganga_logs= glob.glob(f"{folder}/{job}/*/*/*Ganga*.log")
    logs = list(set(raw_logs) - set(ganga_logs))
    return logs

 
def MIlogsFromGrid(job):
    folder = "/afs/cern.ch/work/j/jolane/gangadir/workspace/jolane/LocalXML/"

    logs= glob.glob(f"{folder}/{job}/*/*/*LHCb.log") 
    return logs

 
def mainMI(start, nBins=20):
    logsMI_base = MIlogsFromGrid(start)
    logsMI_gauss_bias_1_low = MIlogsFromGrid(start+1)
    logsMI_gauss_bias_1_medium = MIlogsFromGrid(start+2)
    logsMI_gauss_bias_1_high = MIlogsFromGrid(start+3)
    logsMI_gauss_bias_2_low = MIlogsFromGrid(start+4)
    logsMI_gauss_bias_2_medium = MIlogsFromGrid(start+5)
    logsMI_gauss_bias_2_high = MIlogsFromGrid(start+6)
    makeAndPlotPulls(logsMI_base, "MI.opt", "base.opt", nBins, "/eos/home-j/jolane/gauss_shift_dd/MI_Results")
    makeAndPlotPulls(logsMI_gauss_bias_1_low, "MI.opt", "gauss_bias_1_low.opt", nBins, "/eos/home-j/jolane/gauss_shift_dd/MI_Results")
    makeAndPlotPulls(logsMI_gauss_bias_1_medium, "MI.opt", "gauss_bias_1_medium.opt", nBins, "/eos/home-j/jolane/gauss_shift_dd/MI_Results")
    makeAndPlotPulls(logsMI_gauss_bias_1_high, "MI.opt", "gauss_bias_1_high.opt", nBins, "/eos/home-j/jolane/gauss_shift_dd/MI_Results")
    makeAndPlotPulls(logsMI_gauss_bias_2_low, "MI.opt", "gauss_bias_2_low.opt", nBins, "/eos/home-j/jolane/gauss_shift_dd/MI_Results")
    makeAndPlotPulls(logsMI_gauss_bias_2_medium, "MI.opt", "gauss_bias_2_medium.opt", nBins, "/eos/home-j/jolane/gauss_shift_dd/MI_Results")
    makeAndPlotPulls(logsMI_gauss_bias_2_high, "MI.opt", "gauss_bias_2_high.opt", nBins, "/eos/home-j/jolane/gauss_shift_dd/MI_Results")

def mainQMI(order, start, nBins=20):
    offset = 0
    logsQMI_base = logsFromGrid(start)
    logsQMI_gauss_bias_1_low = logsFromGrid(start+1)
    logsQMI_gauss_bias_1_medium = logsFromGrid(start+2)
    logsQMI_gauss_bias_1_high = logsFromGrid(start+3)
    print(f"n(gauss_bias_1_high) = {len(logsQMI_gauss_bias_1_high)}")
    logsQMI_gauss_bias_2_low = logsFromGrid(start+4)
    logsQMI_gauss_bias_2_medium = logsFromGrid(start+5)
    logsQMI_gauss_bias_2_high = logsFromGrid(start+6)
    makeAndPlotPulls(logsQMI_base, f"poly_{order}.opt", "base.opt", nBins, f"/eos/home-j/jolane/gauss_shift_dd/QMI_Results_{order}/base")
    makeAndPlotPulls(logsQMI_gauss_bias_1_low, f"poly_{order}.opt", "gauss_bias_1_low.opt", nBins, f"/eos/home-j/jolane/gauss_shift_dd/QMI_Results_{order}/gauss_bias_1/low")
    makeAndPlotPulls(logsQMI_gauss_bias_1_medium, f"poly_{order}.opt", "gauss_bias_1_medium.opt", nBins, f"/eos/home-j/jolane/gauss_shift_dd/QMI_Results_{order}/gauss_bias_1_medium/")
    makeAndPlotPulls(logsQMI_gauss_bias_1_high, f"poly_{order}.opt", "gauss_bias_1_high.opt", nBins, f"/eos/home-j/jolane/gauss_shift_dd/QMI_Results_{order}/gauss_bias_1_high/")
    makeAndPlotPulls(logsQMI_gauss_bias_2_low, f"poly_{order}.opt", "gauss_bias_2_low.opt", nBins, f"/eos/home-j/jolane/gauss_shift_dd/QMI_Results_{order}/gauss_bias_2_low/")
    makeAndPlotPulls(logsQMI_gauss_bias_2_medium, f"poly_{order}.opt", "gauss_bias_2_medium.opt", nBins, f"/eos/home-j/jolane/gauss_shift_dd/QMI_Results_{order}/gauss_bias_2_medium/")
    makeAndPlotPulls(logsQMI_gauss_bias_2_high, f"poly_{order}.opt", "gauss_bias_2_high.opt", nBins, f"/eos/home-j/jolane/gauss_shift_dd/QMI_Results_{order}/gauss_bias_2_high")

def mainMD(start, nBins=20):
    offset = 0
    logsMD_base = logsFromGrid(start)
    logsMD_gauss_bias_1_low = logsFromGrid(start+1)
    logsMD_gauss_bias_1_medium = logsFromGrid(start+2)
    logsMD_gauss_bias_1_high = logsFromGrid(start+3)
    logsMD_gauss_bias_2_low = logsFromGrid(start+4)
    logsMD_gauss_bias_2_medium = logsFromGrid(start+5)
    logsMD_gauss_bias_2_high = logsFromGrid(start+6)
    makeAndPlotPulls(logsMD_base, f"MD.opt", "base.opt", nBins, "/eos/home-j/jolane/gauss_shift_dd/MD_Results")
    makeAndPlotPulls(logsMD_gauss_bias_1_low, f"MD.opt", "gauss_bias_1_low.opt", nBins, "/eos/home-j/jolane/gauss_shift_dd/MD_Results")
    makeAndPlotPulls(logsMD_gauss_bias_1_medium, f"MD.opt", "gauss_bias_1_medium.opt", nBins, "/eos/home-j/jolane/gauss_shift_dd/MD_Results")
    makeAndPlotPulls(logsMD_gauss_bias_1_high, f"MD.opt", "gauss_bias_1_high.opt", nBins, "/eos/home-j/jolane/gauss_shift_dd/MD_Results")
    makeAndPlotPulls(logsMD_gauss_bias_2_low, f"MD.opt", "gauss_bias_2_low.opt", nBins, "/eos/home-j/jolane/gauss_shift_dd/MD_Results")
    makeAndPlotPulls(logsMD_gauss_bias_2_medium, f"MD.opt", "gauss_bias_2_medium.opt", nBins, "/eos/home-j/jolane/gauss_shift_dd/MD_Results")
    makeAndPlotPulls(logsMD_gauss_bias_2_high, f"MD.opt", "gauss_bias_2_high.opt", nBins, "/eos/home-j/jolane/gauss_shift_dd/MD_Results")




if __name__=="__main__":
#    seeds = list(range(2)) + list(range(3,7)) + list(range(8,25))
#    seeds = range(0, 100)

    #Missing some?
    #gen(7, "base.opt", 1, 10000, "/mnt/m/qmi/gauss_shift_dd/")
#    fit("MD.opt", "base.opt", 7, False, "/mnt/m/qmi/gauss_shift_dd/")

#    makeAndPlotPulls("MI.opt", "base.opt", seeds, 7)
#    makeAndPlotPulls("MD.opt", "base.opt", seeds, 7)

#    seeds = range(26)

#    gen(2, "gauss_bias_1_high.opt", 1, 10000, "/mnt/m/qmi/gauss_shift_dd/")
    #fit("MI.opt", "gauss_bias_1_high.opt", 2, True, "/mnt/m/qmi/gauss_shift_dd/")
#    fit("MD.opt", "gauss_bias_1_high.opt", 2, False, "/mnt/m/qmi/gauss_shift_dd/")
 #   makeAndPlotPulls("MI.opt", "base.opt", seeds, 20, "/eos/home-j/jolane/gauss_shift_dd/MI_Results", "/eos/home-j/jolane/gauss_shift_dd/MI_Results")

    #logsMI = MIlogsFromGrid(303)
#    for model in ["gauss_bias_1", "gauss_bias_2"]:
#        for scale in ["low", "medium", "high"]:
#            logs = list(glob.glob(f"Fit_MI_to_{model}_{scale}*.log"))
#            makeAndPlotPulls(logs, "MI", f"{model}_{scale}.opt", 10, ".")
     
#    logs = list(glob.glob(f"Fit_MI_to_base*.log"))
#    makeAndPlotPulls(logs, "MI", f"base.opt", 10, ".")
    model = "poly_5"
    logs = list(glob.glob(f"Fit_{model}_to_gauss_bias_1_high*.log"))[0:9]
    makeAndPlotPulls(logs, model, "gauss_bias_1_high.opt", 10, ".")
 

#    logsMI = MIlogsFromGrid(315)
#    makeAndPlotPulls(logsMI, "MI", "gauss_bias_1_high.opt", 10, "/eos/home-j/jolane/gauss_shift_dd/MI_Results")
#    mainMI(339)
#    mainQMI(7,323)
#    mainQMI(9,330)
#    mainQMI(5,346)
#    mainMD(316)

#    makeAndPlotPulls("MD.opt", "gauss_bias_1_low.opt", seeds, 7)


