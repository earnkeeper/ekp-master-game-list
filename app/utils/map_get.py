def map_get(map, keys):
    value = map
    
    for key in keys:
        if key not in value:
            return None
        
        value = value[key]
        
    return value