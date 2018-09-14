from math import exp

def isVector(x: list):
    if x and not False in [type(z) == list for z in x] and ((len(x) == 1 and x[0]) or not False in [len(z) == 1 for z in x]):
        return True
    else:
        return False

def isMatrix(A: list):
    if not False in [type(z) == list for z in A]:
        for z in range(len(A)):
            for y in range(z, len(A)):
                if len(A[z]) != len(A[y]):
                    return False
        return True
    else:
        return False

def sumVectors(A: list, b: list):
    #Error messages
    if not isVector(A):
        raise ValueError("first input is not a vector")
    if not isVector(b):
        raise ValueError("second input is not a vector")
    if len(A) != len(b):
        raise ValueError("vectors must be the same size: {} not equal to {}".format(len(A), len(b)))

    #Body of code
    if len(A) == 1:
        output = [[A[0][i] + b[0][i] for i in range(len(A[0]))]]
    else:
        output = [[A[i][0] + b[i][0]] for i in range(len(A))]
    return output

def vectorMatrix(A: list, b: list):
    #Error messages
    if not isMatrix(A):
        raise ValueError("first input is not a matrix")
    if not isVector(b):
        raise ValueError("second input is not a vector")
    if len(A[0]) != len(b):
        raise ValueError("row size of matrix ({}) is not equal to column size of vector ({})".format(len(A[0]), len(b)))

    #Body of code
    if len(b) == 1:
        output = [[0 for m in range(len(b[0]))] for n in range(len(A))]
        for n in range(len(A)):
            for m in range(len(b[0])):
                output[n][m] = A[n][0]*b[0][m]
    else:
        output = [[0] for n in range(len(A))]
        for n in range(len(A)):
            product = [A[n][i]*b[i][0] for i in range(len(b))]
            output[n] = [sum(product)]

    return output

def transpose(A: list):
    #Error messages
    if not isMatrix(A):
        raise ValueError("input is not a matriz")

    #Body of code
    output = [list(tup) for tup in zip(*A)]
    return output

def ReLU(b: list):
    #Error messages
    if not isVector(b):
        raise ValueError("input is not a vector")

    #Body of code
    if len(b) == 1:
        output = [max(0, b[0][m]) for m in range(len(b[0]))]
    else:
        output = [[max(0, b[n][0])] for n in range(len(b))]
    return output

def softmax(b: list):
    #Error messages
    if not isVector(b):
        raise ValueError("input is not a vector")

    #Body of code
    sumExp = sum([exp(b[x][0]) for x in range(len(b))])
    output = [[exp(b[x][0])/sumExp] for x in range(len(b))]
    return output

softmax([[1],[2],[3]])
