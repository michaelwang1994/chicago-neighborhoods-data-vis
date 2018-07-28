def normalize_string(string):
    return filter(str.isalnum, string.encode('ascii', 'ignore').upper())

one_off_community_area_alternate_names = {
    'THEGOLDCOAST': 'GOLDCOAST',
    'WESTLOOPGATE': 'WESTLOOP',
    'JACKSONPARKHIGHLANDS': 'JACKSONPARK',
    'SHEFFIELDNEIGHBORS': 'SHEFFIELDDEPAUL',
    'MONTCLARE': 'MONTCLAIRE'}