
# coding: utf-8

# In[53]:

def make_maxheap(array):
    for i in range(len(array)//2, -1, -1):
        max_heapify(array, i)
    return array

def max_heapify(array, index):
    parent = array[index]
    left_child_index = (index+1)*2-1
    right_child_index = (index+1)*2

    if left_child_index > len(array)-1 and right_child_index > len(array)-1:
        return array

    else:
        left_child = array[left_child_index]

        if right_child_index > len(array)-1:
            right_child = left_child - 100
        else:
            right_child = array[right_child_index]

    if left_child >= right_child and parent < left_child:
        array[index] = left_child
        array[left_child_index] = parent
        return max_heapify(array, left_child_index)

    elif right_child > left_child and parent < right_child:
        array[index] = right_child
        array[right_child_index] = parent
        return max_heapify(array, right_child_index)

    else:
        return array
    


# In[56]:

class maxheap():

    def __init__(self, array):
        array = make_maxheap(array)
      
    def show(self):
        return array
    
    def extract_max(self):
        maximum = array[0]
        array[0] = array[-1]
        del array[-1]
        max_heapify(array, 0)
        
        return maximum
    
    def insert(self, value):
        array.append(value)
        index = len(array)-1
        while True:
            parent_index = index+1//2 - 1
            if parent_index < 0:
                break
            else:
                parent_value = array[parent_index]
                
            if value > parent_value:
                array[parent_index] = value
                array[index] = parent_value
                index = parent_index
            elif value <= parent_value:
                break
                
    def max(self):
        return array[0]
    
    def delete(self, value):
        i = self.search(value)
        array[i] = array[-1]
        del array[-1]
        max_heapify(array, i)
        
        
    def search(self, value):
        for i in range(len(array)):
            if array[i] == value:
                return i
        else:
            raise ValueError('Value not in heap')   
    
    def heap_sort(self):
        output = []
        i = 0
        while i<len(array):
            output.append(self.extract_max)
            i += 1
        return output


