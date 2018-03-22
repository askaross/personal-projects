
# coding: utf-8

# In[4]:

def merge_sort(array):
    if len(array) == 1:
        return array
    
    mid = len(array) // 2
    L = merge_sort(array[:mid])
    R = merge_sort(array[mid:])
    return merge(L, R)
    
def merge(L, R):

    out = []
    i, j = 0, 0
    while True:
        if i >= len(L) or j >= len(R):
            out.extend(R[j:]) or out.extend(L[i:])
            break

        elif L[i] >= R[j]:
            out.append(L[i])
            i += 1
        
        elif L[i] < R[j]:
            out.append(R[j])
            j += 1
    
    return out


# In[6]:

merge_sort([1,2,3,4,5,6,7,8,9,10])


# In[ ]:



