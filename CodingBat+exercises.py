
# coding: utf-8

# In[14]:

from collections import defaultdict

def maxSpan(nums):

#Finds the maximum number of numbers between two of the same number, inclusive. For example: [1,2,2,1,3] returns 4
#since between the two 1s there are 4 numbers (including the 1s) and between the two 2s there are 2 numbers. Therefore
#the max span is 4. 
    
    #Create a dictionary of lists
    number_position = defaultdict(list)
    
    #Enumerate over each number and store its index in the list
    for index, number in enumerate(nums):
        number_position[number].append(index)
        
    max_span = 0
    #Iterate over the number index dictionary and find the max span within it
    for number in number_position:
        span = number_position[number][-1] - number_position[number][0] + 1
        if span > max_span:
            max_span = span
    return max_span


# In[71]:

def withoutString(base, remove):
    
#Remove the occurence of the 'remove' string from the 'base' string. For example: withoutString('Hello', 'lo') will
#return 'Hel'.
    
    #Turn strings into list so they are mutable
    output = list(base)
    span = len(remove)
    overlap = 0
    
    #Iterate over and remove the 'remove string'
    for i in range(len(base) - span + 1):
        
        if len(output) < span:
            break
            
        else:
            if base[i+overlap:i+overlap+span] == remove:
                for j in range(i+overlap,i+overlap+span):
                    output[j] = ''
                overlap += span-1
                
    return ''.join(output)
    


# In[89]:

def sumNumbers(string):
    
#Sum all the occurences of numbers together hidden in a string. For example 'abc123d3' will return 126, since we have
#123 + 3
    numbers = []
    number_span = 0         #this is a placeholder to make sure when we find a 3 digit number eg. we skip the next 3
    digit_span = 0          #this is a placeholder to make sure when we find a 3 digit number eg. we consider it as 
                            #one whole number instead of 3 separate numbers
    
    #Iterate over the string
    for i in range(len(string)):
        
        if i+number_span > len(string):
            break
        
        #Check if string is a number
        elif string[i+number_span].isdigit():
            #Check to see if there are other numbers after it incase is has multiple digits
            for j in range(len(string)):
                digit_span = j
                if j+i+number_span+1>len(string) or not string[j+i+number_span].isdigit():
                    break
            
            #Add the number to the list 'numbers'
            numbers.append(int(string[i+number_span:i+number_span+digit_span]))
            
            number_span += digit_span
        digit_span = 0        
    
    return sum(numbers)
                
            


# In[22]:

from math import log

def canBalance(nums):
    
#This checks the existence of a way to separate an array of numbers into two groups that sum to the same number.
#For example: [1,3,2,2] will return True as a split in the middle leaves 1+3=2+2. However [1,5,2,1] will return False
#as no such split exits. It works by binary search
    
    #Initial starting position is in the middle
    start = int(len(nums)/2)
    
    #Since binary search is o(log(n)) we only need to iterate for this amount
    for i in range(int(log(len(nums),2)+1)):
        
        #Define left and right sum
        left_sum = sum(nums[0:start])
        right_sum = sum(nums[start:len(nums)])
        
        #Boolean checks. If sum is greater on the right then move the starting position to the right. If it is greater 
        #on the left then move the starting position to the left
        if left_sum == right_sum:
            return True
        elif left_sum > right_sum:
            start = start - int(start/2)
        elif left_sum < right_sum:
            start = start + int(start/2)
    
    return False


# In[33]:

def mapShare(dictionary):
    dictionary['b'] = dictionary['a']
    if 'c' in dictionary: del dictionary['c']
    return dictionary


# In[62]:

def remove_duplicates(array):
    
#Removes duplicates in an array
    removed_duplicates = []
    for i in array:
        if i not in removed_duplicates:
            removed_duplicates.append(i)
    return removed_duplicates


# In[43]:

def remove_duplicates_inplace(array):

#Removes duplicates in a sorted array, inplace, without creating a new array.
    check = 0
    for i in range(1,len(array)):
        if array[i] != array[check]:
            check += 1
            array[check] = array[i]
    
    return array[:check+1]


# In[45]:

def wordLen(array):
    
#Outputs a dictionary of the words in an array and their length
    output = {}
    for element in set(array):
        output[element] = len(element)
    return output


# In[58]:

def pairs(array):
    
#Outputs a dictionary of the first and last letter of words in an array
    output = {}
    for element in array:
        output[element[0]] = element[-1]
    return output


# In[53]:

def wordCount(array):
    
#Outputs a dictionary of the number of times a given word occurs in an array
    output = {}
    for element in array:
        if element in output:
            output[element] += 1
        else:
            output[element] = 1
    return output


# In[63]:

def encoder(raw, code_words):
    
#Converts the strings in the 'raw' array into their corresponding 'code_words'. Raw words are assigned to the next 
#available code word. For example: [a,b,a,c] and [1,2,2,4] then the output is [1,2,1,4], since a is assigned 1 and 2 
#has already been assigned to b
    code_words = remove_duplicates(code_words)
    values = {}
    index = 0
    output = []
    
    for element in raw:
        if element not in values:
            values[element] = code_words[index]
            index += 1
        output.append(values[element])
        
    return output


# In[69]:

def blackjack(a,b):
    
#Returns the value closest to 21 without going over
    if a < 0 or b < 0 or type(a) != int or type(b) != int:
        print('Error: must be two integers greater than 0')
    
    if a > 21 and b > 21:
        return 0
    elif a > 21:
        return b
    elif b > 21:
        return a
    
    else:
        if a > b:
            return a
        elif b > a:
            return b
        elif a == b:
            return a
    


# In[127]:

def evenlyspaced(array):
    
#An array of size 3 with one low, middle, and high number is passed through and this function will tell you if they
#are all evenly spaced. For example: [2,6,4] returns True (spaced by 2), while [4,1,3] returns False
    differences = []
    
    for i in range(1,len(array)):
        differences.append(array[0] - array[i])
    
    if (differences[0] > 0 and differences[1] < 0) or (differences[0] < 0 and differences[1] > 0):
        if abs(differences[0]) == abs(differences[1]):
            return True
        else:
            return False
    
    else:
        if differences[0] <= 0 and differences [1] <= 0:
            if max(differences)*2 == min(differences):
                return True
            else:
                return False
        elif differences[0] >= 0 and differences[1] >= 0:
            if max(differences) == min(differences)*2:
                return True
            else: return False
        


# In[132]:

def makeBricks(small, big, goal):
    
#Small bricks have size of 1 and Big bricks have size of 5. This function tells you if it possible to reach the goal
#size with a given number of small bricks and big bricks
    if small >= goal or (goal%5 == 0 and small+5*big >= goal):
        return True
    elif small+5*big < goal:
        return False
    
    else:
        fives = int(goal/5)
        ones = goal%5
        if ones <= small and fives <= big:
            return True
        elif fives > big and ones < small:
            extra_fives = fives - big
            if extra_fives*5 <= small and ones <= small-extra_fives*5:
                return True
        else:
            return False


# In[187]:

from collections import defaultdict

letter_dict = defaultdict(list)

rows, columns = len(board), len(board[0])

for letter in word:
    for row in range(rows):
        for column in range(columns):
            if board[row][column] == letter:
                letter_dict[letter].append([row, column])


# In[185]:

board = [ ["I","L","A","W"],
  ["B","N","G","E"],
  ["I","U","A","O"],
  ["A","S","R","L"] ]
word = 'EARS'


# In[186]:

letter_dict

