
# coding: utf-8

# In[157]:

class Node():
    
    def __init__(self, value):
        self.value = value
        self.next = None 
        self.prev = None
    
    def next_node(self, node2):
        self.next = node2
        node2.prev = self
    
    def prev_node(self, node2):
        self.prev = node2
        node2.next = self


# In[254]:

class linked_list():
    
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0
    
    def add_node(self, node):
        node = Node(node)
        if self.head == None:
            self.head = node
            
        if self.tail != None:
            self.tail.next_node(node)
        
        self.tail = node
        self.length += 1
        
    def traverse(self, index):
        start = self.head
        for i in range(index, 0, -1):
            start = start.next
        return start
    
    def insert(self, node, index):
        node = Node(node)
        if index == 0:
            node.next_node(self.head)
            self.head = node
            
        elif index == self.length:
            node.prev_node(self.tail)
            self.tail = node  
            
        else:
            previous = self.traverse(index-1)
            next = previous.next

            previous.next_node(node)
            next.prev_node(node)
        
        self.length += 1
    
    def delete(self, index):
        
        if index == 0:
            node = self.head.next
            node.prev = None
            self.head = node
        
        elif index == self.length:
            node = self.tail.prev
            node.next = None
            self.tail = node
        
        else:
            node = self.traverse(index)
            node1 = node.prev
            node2 = node.next
            
            node1.next_node(node2)
        
        self.length -= 1

    def show(self):
        start = self.head
        linky = [start.value]
        for i in range(self.length-1):
            start = start.next
            linky.append(start.value)
        return linky
    
    def search(self, val):
        current = self.head
        i = 0
        while True:
            if current == None:
                return print('Value not in list')
            elif current.value == val:
                return i
            else:
                current = current.next
                i += 1
    
    def del_value(self, val):
        index = self.search(val)
        self.delete(index)


# In[255]:

def make_linked_list(array):
    linky = linked_list()
    for i in array:
        linky.add_node(i)
    return linky


# In[256]:

array = [1,2,3,4,5,6,7,8,9]
linky = make_linked_list(array)


# In[260]:

linky.show()


# In[ ]:



