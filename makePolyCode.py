from setupModel import writeModel


def makePoly(order):
    strings = []
    for i in range(order+1):
        for j in range(order + 1 - i):
            strings += [f"m_mps[\"PhaseCorrection::C{i}_{2*j+1}\"]->mean() * std::legendre({i}, x) * std::legendre({2 * j+1}, y)"]
        
    string = f"""case {order}:
    return """
    for s in strings[:len(strings)-1] : 
        string +=f"{s} + "
    string += strings[len(strings) - 1] + ";\nbreak;"

    return string
def makePolyFL(order):
    strings = []
    for i in range(order+1):
        for j in range(order + 1 - i):
            strings += [f"m_mps[\"PhaseCorrection::C{i}_{2*j+1}\"]->mean() * fastLegendre(x,{i}) * fastLegendre(y,{2 * j+1})"]
        
    string = f"""case {order}:
    return """
    for s in strings[:len(strings)-1] : 
        string +=f"{s} + "
    string += strings[len(strings) - 1] + ";\nbreak;"

    return string




string = ""
for o in range(10):
    string += makePoly(o) + "\n"

stringFL = ""
for o in range(10):
    stringFL += makePolyFL(o) + "\n"



with open("polyCode.txt", "w") as f:
    f.write(string)
with open("polyCodeFL.txt", "w") as f:
    f.write(stringFL)




