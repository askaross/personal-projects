from math import pi

#takes n in base 10 and returns it in any base (default is pi
##with optional x decimals)

def converter(n, decimals=0, base=pi):
    answer = []
    if n < 0: 
        n = n*(-1) 
        answer.append('-')
    if n < 1:
        answer.append(0)
    
    p = 0
    while True:
        if base**p <= n: p = p + 1
        else: break
    
    divisor, multiplier = 0, 0
    base_greater_than_9 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'                           
                            
    for i in reversed(range((decimals*-1),p)):
        divisor = 0
        if i == -1:
            answer.append('.')
            
        divisor = int(n / (base**i))
        multiplier = divisor
        
        if divisor > 9:
            divisor = base_greater_than_9[divisor - 10]
            
        answer.append(divisor)
        n = n - ((base**i) * multiplier)
    
    return ''.join(str(number) for number in answer)
