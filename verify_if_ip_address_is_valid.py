def is_valid_IP(strng):
    
    ip_components = strng.split('.')
    
    if len(ip_components) != 4:
        return False
    
    for char in ip_components:
        if (
            not char.isdigit()
            or (len(char)>1 and char[0] == '0')
            or int(char)>255 or int(char)<0
            ):
            return False
    
    return True