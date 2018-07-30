import pandas as pd
import json

census_data = pd.read_csv('data/census_data.csv')[:-1]
census_data['COMMUNITY AREA NAME'] = census_data['COMMUNITY AREA NAME'].str.replace(' ', '').str.replace('\'', '').str.upper()
census_data = census_data.set_index('COMMUNITY AREA NAME')
census_data['PER CAPITA INCOME PERCENTILE'] = census_data['PER CAPITA INCOME'].rank(pct=True) * 100

with open('data/boundaries.json') as boundaries:
    boundaries_data = json.load(boundaries)

with open('data/neighborhood_to_community_area.json') as neighborhood_to_community_area:
    neighborhood_to_community_area_data = json.load(neighborhood_to_community_area)

with open ('data/chicago_neighborhood_descriptions.json') as chicago_neighborhood_descriptions:
    chicago_neighborhood_descriptions_data = json.load(chicago_neighborhood_descriptions)

neighborhoods = boundaries_data['objects']['boundaries']['geometries']
neighborhoods_with_census_data = []

def normalize_string(string):
    return filter(str.isalnum, string.encode('ascii', 'ignore').upper())

one_off_community_area_mapping = {
    'United Center': 'NEARWESTSIDE',
    'Garfield Park': 'WESTGARFIELDPARK',
    'Museum Campus': 'NEARSOUTHSIDE',
    'Millenium Park': 'LOOP',
    'Grant Park': 'LOOP',
    'Rush & Division': 'NEARNORTHSIDE',
    'Montclare': 'MONTCLAIRE'}

for neighborhood in neighborhoods:
    neighborhood_properties = neighborhood['properties']
    principle_neighborhood = neighborhood_properties['pri_neigh'].split(',')[0]
    formatted_priciple_neighborhood = normalize_string(principle_neighborhood)
    if formatted_priciple_neighborhood in census_data.index:
        community_area_to_search = formatted_priciple_neighborhood
    elif formatted_priciple_neighborhood in neighborhood_to_community_area_data:
        community_area_to_search = neighborhood_to_community_area_data[formatted_priciple_neighborhood]
    elif principle_neighborhood in one_off_community_area_mapping:
        community_area_to_search = one_off_community_area_mapping[principle_neighborhood]
    else:
        continue
    community_area_census_data = census_data.loc[community_area_to_search]
    neighborhood_census_data_dict = {}
    for key, value in community_area_census_data.items():
        formatted_key = key.lower().replace(' ', '_').replace('+', '').replace('\'', '')
        
        neighborhood_census_data_dict[formatted_key] = value
    neighborhood_properties['census_data'] = neighborhood_census_data_dict
    try:
        neighborhood_properties['details'] = chicago_neighborhood_descriptions_data[neighborhood_properties['pri_neigh']]
    except Exception as e:
        pass
    neighborhoods_with_census_data.append(neighborhood)

with open('data/boundaries-with-census-data.json', 'w') as boundaries_with_census_data:
    json.dump(boundaries_data, boundaries_with_census_data, indent=1)
