def pick_peaks(arr):

    #Finds the positions and values of any peaks in an array.
    #For example [1,2,3,2,1] has a peak at position 2, with a value of 3.
    #Plateaus are dealt with as follows:
    #[1,2,2,2,1] will return position 1, value 2, since this is the first
    #occurence of the plateau. [1,2,2,2] however will return an empty list
    
    pos, peaks = [], []
    for i in range(1,len(arr)-1):
        if arr[i-1] < arr[i] > arr[i+1]:
            pos.append(i)
            peaks.append(arr[i])
        elif arr[i-1] < arr[i] >= arr[i+1]: 
            for j in range(i+2, len(arr)):
                if arr[j] > arr[i]:
                    break
                elif arr[j] < arr[i]:
                    pos.append(i)
                    peaks.append(arr[i])
                    break
    return {'pos': pos, 'peaks': peaks}
