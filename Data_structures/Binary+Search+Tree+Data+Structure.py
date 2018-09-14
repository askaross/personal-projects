
# coding: utf-8

class BSNode():
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.left_child = None
        self.right_child = None
    
    def search(self, key):
        if key is None:
            raise ValueError('None is not a valid key')
        
        if self.key == key:
            return self
        
        else:
            if key > self.key and self.right_child != None:
                return self.right_child.search(key)
            
            elif key < self.key and self.left_child != None:
                return self.left_child.search(key)
            
            else:
                raise ValueError('Key not in the BST')
    
    def find_min(self):
        if self.left_child is None:
            return self
        else:
            return self.left_child.find_min()
        
    def next_larger(self):

        if self.right_child:
            return self.right_child.find_min()
        
        elif self.right_child is None:
            current = self
            while current.parent:
                if current.parent.left_child == current:
                    return current.parent
                else:
                    current = current.parent
            
            return ValueError('No larger element')
    
    def insert(self, key):
        new_node = BSNode(key)
        
        current = self
        
        while True:
            if key >= current.key:
                if current.right_child is None:
                    new_node.parent = current
                    current.right_child = new_node
                    break
                else:
                    current = current.right_child
            
            elif key < current.key:
                if current.left_child is None:
                    new_node.parent = current
                    current.left_child = new_node
                    break
                else:
                    current = current.left_child
    
    def delete(self):
        if self.right_child is None or self.left_child is None:

            if self.parent is None:
                if self.right_child:
                    self.right_child.parent = None
                elif self.left_child:
                    self.left_child.parent = None
    
            if self.parent.right_child is self:
                self.parent.right_child = self.right_child or self.left_child
                if self.parent.right_child is not None:
                    self.parent.right_child.parent = self.parent
            
            else:
                self.parent.left_child = self.right_child or self.left_child
                if self.parent.left_child is not None:
                    self.parent.left_child.parent = self.parent
            
        else:
            replacement = self.next_larger()
            self.key = replacement.key
            return replacement.delete()
         


