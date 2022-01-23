import os
def fit():
    lambdas = [25,50,100]
    for l in lambdas:
        os.system(f"sed \"s/LAMBDA/{l}/g\" fit.tmpl.opt  > fit.opt ; python3 fit.py | grep BIC >> lasso.txt")

def plot():
    x = []
    y = []
    with open("lasso.txt") as f:
        for line in f:
            a = line.split()
            x += [float(a[0])]
            y += [float(a[1])]
    from matplotlib import pyplot as plt
    import numpy as np
    idx = np.argmin(y)
    print(f"BIC({x[idx]}) = {y[idx]}")
    f,a = plt.subplots(1,1)
    a.scatter(x, y)

    f.savefig("lasso.png", dpi=300)

plot()