#Running the function next_bigger() on a specific number will find the next
#largest number using the same digits from the original. 
#For example, the number 91854 has its next largest number as 94581
#If there is no next largest (eg. 999) then it returns -1

def swap_first_with_higher(digits):
    """
    >>> swap_first_with_higher(list('59853'))
    ['8', '9', '5', '5', '3']

    """
    for pos in range(len(digits) - 1, 0, -1):
        if digits[0] < digits[pos]:
            digits[0], digits[pos] = digits[pos], digits[0]
            break
    return digits


def reversed_tail(digits):
    """
    >>> reversed_tail(list('89553'))
    ['8', '3', '5', '5', '9']

    """
    return [digits[0]] + digits[1:][::-1]


def next_bigger(num):
    """
    >>> next_biggest(59853)
    83559

    >>> next_biggest(111)
    -1

    >>> next_biggest(11211)
    12111

    """
    digits = list(str(num))
    for pos in range(len(digits) - 1, 0, -1):
        if digits[pos-1] < digits[pos]:
            left = digits[:pos-1]
            right = reversed_tail(swap_first_with_higher(digits[pos-1:]))
            return int(''.join(left + right))

    return -1
