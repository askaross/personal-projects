def is_valid_coordinates(coordinates):

    #Returns True if the coordinates entered as a string arevalid coordinates
    #and False otherwise
    #For example "63.18, -81.45623" are valid coordinates
    #"91.3, -22.456.123.1" are invalid coordinates
    
    try: 
        float(coordinates[:coordinates.index(',')])
        float(coordinates[coordinates.index(',')+1:])
        if (coordinates.count(',') == 1 and 
        coordinates.count('.') <= 2 and
        coordinates.count('e') == 0 and
        0 <= abs(float(coordinates[:coordinates.index(',')])) <= 90 and
        0 <= abs(float(coordinates[coordinates.index(',')+1:])) <= 180):
            return True
        else:
            return False
    except ValueError:
        return False
