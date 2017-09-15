#The function fish calculates the maximum size your fish can reach given
#a shoal of other fish of varying sizes according to these specific rules
#1) you fish starts at size 1
#2) you can only eat fish smaller or equal in size to you
#3) you grow in size if you eat a certain weight of fish. the weight you
#   need to reach is calculated by the formula 2*size*(size+1)
#For example: a shoal '1111222233' will return 2, since you eat 4 fish of
#size 1, then 4 fish of size 2, then 2 fish of size three

def fish(shoal):
    size = 1
    while(count_lesser_fish(shoal, size) >= 2*size*(size + 1)):
        size += 1
    return size
    
def count_lesser_fish(shoal, size):
    return sum(int(f) for f in shoal if int(f) <= size)
