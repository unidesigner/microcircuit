

def extract_value_customdict(dictionary, property, value='value', name='name'):
    for k, v in dictionary[value].items():
        if v[name] == property:
            return k
    return None
