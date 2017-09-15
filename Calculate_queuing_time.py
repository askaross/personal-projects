def queue_time(customers, n):

    #Returns the time it takes for all customers to leave a queue given a number
    #of tills n, and a list of customers with the time it takes for each customer
    #to finish at a till. The assumption is that the next customer moves straight
    #to a till as soon as it opens
    #For example [10,2,3,4] with 2 tills will take 10 units of time, since 2,3,4
    #all finish in the second till before 10 finishes.
    
    if customers == [] or n == 0:
        return 0
    elif n >= len(customers):
        return max(customers)
    else: 
        tills = customers[:n]
        minimum = 0
        for c in customers[n:]:
            minimum = min(tills)
            min_idx = tills.index(minimum)
            tills[min_idx] = tills[min_idx] + c
    return max(tills)
