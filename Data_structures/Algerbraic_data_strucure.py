class Cons:

    #Cons is a data structure that contains an item and a pointer to the next
    #item. If it is the last item then the pointer is None.
    #It also has a number of methods:
    
    #to_array - converts the Cons data structure to an array
    #from_array - converts an array to the Cons data structure
    #filter - filters all elements from the Cons data structure that satisfy
    #         a given function
    #map - maps all elements in the Cons data structure to a given function
    
    def __init__(self, head, tail):
        self.head = head
        self.tail = tail

    def to_array(self):
       tail = self.tail
       new_tail = (tail.to_array() if tail is not None else [])
       return [self.head] + new_tail

    @classmethod
    def from_array(cls, arr):
        head = None
        for x in arr[::-1]: head = Cons(x, head)
        return head
    
    def filter(self, fn):
        return Cons.from_array([x for x in self.to_array() if fn(x)])
  
    def map(self, fn):
        return Cons.from_array([fn(x) for x in self.to_array()])

