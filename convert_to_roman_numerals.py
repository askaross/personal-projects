def roman_numerals(n):

    #returns any number n in it's roman numeral format
    
    divisors = {1000: 0, 900: 0, 500: 0, 400: 0, 100: 0, 90: 0, 50: 0, 
              40: 0, 10: 0, 9: 0, 5: 0, 4: 0, 1: 0}
    symbols = {1: 'I', 4: 'IV', 5: 'V', 9: 'IX', 10: 'X', 40: 'XL', 50: 'L', 90: 'XC', 
              100: 'C', 400: 'CD', 500: 'D', 900: 'CM', 1000: 'M'}
    
    for i in sorted(divisors, reverse=True):
        divisors[i] = int(n/i)
        n -= int(n/i)*i
    
    return ''.join(symbols[i]*divisors[i] for i in sorted(divisors, reverse=True))
