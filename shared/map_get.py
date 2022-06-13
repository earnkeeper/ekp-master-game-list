def map_get(map, keys):
    value = map
    
    for key in keys:
        if type(key) == int:
            if type(value) != list:
                return None
            if key >= len(value):
                return None
            return value[key]
        
        if key not in value:
            return None
        
        value = value[key]
        
    return value