def find_matches(exst, new):
    '''
    Compares items of new with items of exst by existing parameters
    Returns a part of new where all keys match some item in exst
    '''
    matches = []
    for new_item in new:
        for exst_item in exst:
            if all(new_item[key] == exst_item[key] for key in new_item):
                matches.append(new_item)
                break  # Stop checking once a match is found
    return matches


def find_non_matches(exst, new):
    '''
    Compares items of new with items of exst by existing parameters
    Returns a part of new where there's
    no direct match by all params with any item of exst
    '''
    non_matches = []
    for new_item in new:
        match_found = False
        for exst_item in exst:
            if all(new_item[key] == exst_item[key] for key in new_item):
                match_found = True
                break  # Stop checking once a match is found
        if not match_found:
            non_matches.append(new_item)
    return non_matches


def trim_keys(dicts, keys_to_keep):
    '''Trim unnecessary keys from a list of dictionaries.'''
    if len(dicts) == 0:
        return []
    else:
        return [{
            key: d[key]
            for key in keys_to_keep if key in d
        } for d in dicts]


def smart_in(item, dictionary, k2keep: list):
    return (item in trim_keys(dictionary, k2keep))
