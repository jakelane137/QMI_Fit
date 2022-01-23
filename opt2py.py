def param2Tex(name):
    if "PhaseCorrection::C" in name:
        ij = name.split("PhaseCorrection::C")[-1]
        i = ij.split("_")[0]
        j = ij.split("_")[1]
        return f"C_{{{i}, {j}}}"
    if "pCoherentSum::" in name:
        vS = name.split("pCoherentSum::")
        return f"{vS[0]}_{{{vS[1]}}}"
    else:
        return name

def param2File(name):
    if "PhaseCorrection::C" in name:
        ij = name.split("PhaseCorrection::C")[-1]
        i = ij.split("_")[0]
        j = ij.split("_")[1]
        return f"C_{i}_{j}"
    if "pCoherentSum::" in name:
        vS = name.replace("+","p").replace("-","m").split("pCoherentSum::")
        return f"{vS[0]}{vS[1]}"
    else:
        return name


