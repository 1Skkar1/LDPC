import numpy as np
from bitstring import BitArray


# LDPC CODE GENERATION 
def generate_code(K, m, v):
    P = []
    arrK = np.arange(K)

    for i in range(0, v):
        arrShuffle = np.random.shuffle(arrK)
        for j in range(0, len(arrK), m):
            P.append(arrShuffle[j:j+m])

    return P

# ENCODING
def encode(K, P, w):
    x = BitArray(w)

    for i in P:
        code = 0
        for j in range(len(i)):
            posW = w[i[j]]
            code = code ^ posW

        x.append(bin(code))

    return x

# DECODING
def decode(K, P, y, q):
    x = ''
    y = y.bin

    for i in range(0, K + len(P)):
        if (int(q[i]) == 0):
            x = x + y[i]
        
        if (int(q[i]) == 1):
            x = x + 'x'
    
    while 'x' in x:
        for i in range(0,len(P)):
            x = checkError(P[i], x, K + i)
    
    return BitArray(bin = x[0:K])

def checkError(P, x, j):
    subP = []
    nErrors = 0
    pos = 0

    for i in range(0,len(P)):
        subP.append(x[P[i]])
        if x[P[i]] == 'x':
            nErrors += 1
            pos = P[i]
    
    if x[j] == 'x':
        nErrors += 1
        pos = j
    
    if nErrors == 1:
        par = str(getParity(x[j], subP))
        xList = list(x)
        xList[pos] = par
        xFix = ''.join(xList)
        return xFix
    
    else:
        return x

def getParity(x, subP):
    par = 0
    
    if x != 'x':
        par = x
    
    for i in range(0,len(subP)):
        if subP[i] != 'x':
            par = int(par) ^ int(subP[i])

    return par