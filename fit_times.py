from matplotlib import pyplot as plt
import numpy as np
def getParams(order):
    return 0.5*(order +1)*(order+2)

def str2Time(t):
    m = t.split("m")[0]
    s = t.split("m")[1].split("s")[0]
    return float(m)*60 + float(s)


def mAndc(x, y):
    m = -(np.mean(y) * np.mean(x) - np.mean(x * y))/np.std(x)**2
    c = np.mean(y) - m * np.mean(x)
    return m, c


x = []
t= []
with open("fit_times.txt") as f:
    for line in f:
        a = line.split()
        o = int(a[0])
        nP = getParams(o)
        t += [str2Time(a[1])]
        x += [nP]

x= np.array(x)
t= np.array(t)
f,a=plt.subplots(1,1)
a.scatter(x, t)
m, c = mAndc(x, t)
X = np.linspace(0, 9, 9)
X = getParams(X)

Y = m * X + c
a.plot(X, Y)
f.savefig("fit_times.png", dpi=300)

