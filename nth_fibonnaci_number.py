def matrix_mult(X, Y):
    return [[sum(a*b for a,b in zip(X_row,Y_col)) for Y_col in zip(*Y)] for X_row in X]

def matrix_power(M, n):
    if n == 1:
        return M
    elif n%2:
        return matrix_mult(M, matrix_power(M, n-1))
    P = matrix_power(M, n/2)
    return matrix_mult(P, P)

def fib(n):
    sign = 1
    
    if n<0:
        if n%2 == 0: sign=-1
        n *= -1
    
    if n == 0:
        return 0
    elif n == 1:
        return 1 * sign
    
    else:
        F1 = [[0],[1]]
        T = [[0,1],[1,1]]
        return (matrix_mult(matrix_power(T, n-1), F1))[1][0] * sign