import os

from fit import fit

def preamble():
    string = f"""EventType D0 K0S0 pi- pi+
TagTypes  {{
    \"KK D0{{K+,K-}} 1000\"
    \"Kspi0 D0{{K0S0,pi0}} 1000\"
    \"Kppim D0{{K+,pi-}} 5000\"
    \"Kmpip D0{{K-,pi+}} 5000\"
    \"Kspipi D0{{K0S0,pi-,pi+}} 1000\"
}}

BTagTypes {{
    \"Bm2Dhm Bp2Dhp 0 -1 1 1\" 
    \"Bp2Dhp Bp2Dhp 1 1 1 1\" 
}}

D0{{K+,K-}} Fix 1 0 Fix 0 0
D0{{K0S0,pi0}} Fix 1 0 Fix 0 0
D0{{K-,pi+}} Fix 1 0 Fix 0 0
D0{{K+,pi-}} Fix 0 0 Fix 0 0
Dbar0{{K+,K-}} Fix 1 0 Fix 0 0
Dbar0{{K0S0,pi0}} Fix -1 0 Fix 0 0
Dbar0{{K-,pi+}} Fix 0 0 Fix 0 0
Dbar0{{K+,pi-}} Fix 1 0 Fix 0 0

pCoherentSum::x+ Free 0.05 1
pCoherentSum::y+ Free -0.557 1
pCoherentSum::x- Free -0.382 1
pCoherentSum::y- Free 0.409 1


PhaseCorrection::debug false
testPhaseCorr false
makeCPConj true
useCache false
Minimiser::PrintLevel 2
Minimiser::debug false
NIntMods {{
    0.01
    2
}}
staggerFit true
"""
    return string


def MI(nBins):
    MIString = """nEventsRefFrac
"""
    for i in range(1,nBins+1):
        MIString += f"c_{i} Fix 0 1\n"
        MIString += f"s_{i} Fix 0 1\n"
    return MIString


def MD():
    MDString = """PhaseCorrection::PolyType antiSym_legendre
PhaseCorrection::Order 0
LASSO::lambda Fix 0 0
PhaseCorrection::C0_1 Fix 0 0
"""
    return MDString


def baseModel(baseModelFile):
    string = ""
    with open(baseModelFile ) as f:
        for line in f:
            string += line
    return string

def gaussBias(muX, muY, sigmaX, sigmaY, scale):
    string = f"""PhaseCorrection::PolyType Gaussian
PhaseCorrection::GaussScale Fix {scale} 0
PhaseCorrection::GaussMuX Fix {muX} 0
PhaseCorrection::GaussSigmaX Fix {sigmaX} 0
PhaseCorrection::GaussMuY Fix {muY} 0
PhaseCorrection::GaussSigmaY Fix {sigmaY} 0
PhaseCorrection::GaussErfFactor Fix 0.05 0
PhaseCorrection::GaussLinearW- Fix 1 0
PhaseCorrection::GaussQuadraticW- Fix 0.0001 0
"""
    return string

def poly(order, Lambda=0):
    string = f"""PhaseCorrection::PolyType antiSym_legendre
PhaseCorrection::Order {order}
LASSO::lambda Fix {Lambda} 0
"""
    for i in range(order+1):
        for j in range(order+1 - i):
            string += f"PhaseCorrection::C{i}_{2*j+1} Free 0 1\n"
    return string


def writeModel(modelString, output):
    with open(output, "w") as f:
        f.write(modelString)

def main():
    gauss_loc_1 = {"muX":1.0,"muY":1.25, "sigmaX":0.025, "sigmaY":0.5}
    gauss_loc_2 = {"muX":0.75,"muY":2.5, "sigmaX":0.1, "sigmaY":0.1}
    gauss_biases = {"gauss_bias_1":gauss_loc_1, "gauss_bias_2":gauss_loc_2}
    scales = {"low":0.1, "medium":0.5, "high":1}
    orders = range(20+1)
    base = baseModel("kspipi.opt")
    for biasName in gauss_biases:
        for scale in scales:
           modelString = preamble() + base + gaussBias(gauss_biases[biasName]["muX"], gauss_biases[biasName]["muY"],gauss_biases[biasName]["sigmaX"],gauss_biases[biasName]["sigmaY"],scales[scale])
           writeModel(modelString, f"{biasName}_{scale}.opt")
    for order in orders:
        fitModelString = preamble() + base + poly(order, 0)
        writeModel(fitModelString, f"poly_{order}.opt")
    MIModel = preamble() + base + MI(8)
    writeModel(MIModel, "MI.opt")
    MDModel = preamble() + base + MD()
    writeModel(MDModel, "MD.opt")
    writeModel(MDModel, "base.opt")

    base2 = baseModel("babar.opt")
    secondModel = preamble() + base2 + MD()
    writeModel(secondModel, "base2.opt")

    for order in orders:
        fitModelString = preamble() + base2 + poly(order, 0)
        writeModel(fitModelString, f"poly_{order}_2.opt")

if __name__=="__main__":
    main()
           
