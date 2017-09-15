def same_structure_as(original,other):

    #Returns True if both items passed through have the same nested structure
    #and are lists. For example, [0,[0,0],0] has the same nested structure as
    #[1,[1,1],1]. If they don't have the same nested structure then it returns
    #false
    
    if isinstance(original, list) and isinstance(other, list) and len(original) == len(other):
        for o1, o2 in zip(original, other):
            if not same_structure_as(o1, o2): return False
        else: return True
    else: return not isinstance(original, list) and not isinstance(other, list)
