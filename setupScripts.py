import os
def genEnv(model_file, seed, nBESIII, nLHCb, dataFolder, nCores):
    model_pref = model_file.replace(".opt", "")
    return f"MODEL={model_file} NCORES={nCores} SEED={seed} BESIIINEVENTS={nBESIII} LHCBNEVENTS={nLHCb} BESIIIOUTPUT={dataFolder}/besiii{seed}{model_pref}.root LHCBOUTPUT={dataFolder}/lhcb{seed}{model_pref}.root"


def fitEnv(fit_model_file, gen_model_file, seed, dataFolder, nCores=12):
    gen_model = gen_model_file.replace(".opt", "")
    fit_model = fit_model_file.replace(".opt", "")
    return f"MODEL={fit_model_file} NCORES={nCores} PLOTFILE=Fit_{fit_model}_to_{gen_model}_{seed}.root LOGFILE=Fit_{fit_model}_to_{gen_model}_{seed}.log BESIIISAMPLE={dataFolder}/besiii{seed}{gen_model}.root LHCBSAMPLE={dataFolder}/lhcb{seed}{gen_model}.root"

if __name__=="__main__":
    envString = genEnv("poly_0.opt", 0, 1, 10000, "/mnt/m/qmi/gauss_dd_shift/" ,1)
    print(f"{envString} ./gen.sh")