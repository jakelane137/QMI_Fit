import scipy
import sympy

def transformDalitz(s01, s02):
    x = 0.5*(s01 + s02)
    y =0.5*(s02 - s01)
    m1 = 2.2340742171132946
    c1 = -3.1171885586526695
    m2 = 0.8051636393861085
    c2 = -9.54231895051727e-05
    x = m1 * x + c1
    y = m2 * y + c2
    return x, y

    

def correction(C, Order):
    corr = 0
    for i in range(Order+1):
        for j in range(Order -i+1):
            print(f"{i} {j} {corr} {type(corr)}")
            corr += C[f"{i}_{2*j+1}"] * scipy.special.legendre(i) * scipy.special.legendre(j)
    return corr


