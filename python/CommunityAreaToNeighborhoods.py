import urllib2
from bs4 import BeautifulSoup
import json

wikipedia_page = urllib2.urlopen('https://en.wikipedia.org/wiki/Community_areas_in_Chicago').read()

soup = BeautifulSoup(wikipedia_page, 'lxml')
tables = soup.findAll('table', {'class': 'wikitable'})

neighborhood_to_community_area = {}

def normalize_string(string):
    return filter(str.isalnum, string.encode('ascii', 'ignore').upper())

one_off_community_area_alternate_names = {
    'THEGOLDCOAST': 'GOLDCOAST',
    'WESTLOOPGATE': 'WESTLOOP',
    'JACKSONPARKHIGHLANDS': 'JACKSONPARK',
    'SHEFFIELDNEIGHBORS': 'SHEFFIELDDEPAUL',
    'MONTCLARE': 'MONTCLAIRE'}

for table in tables:
    table_body = table.find('tbody')
    table_rows = table_body.findAll('tr')
    for row in table_rows[1:]:
        table_data = row.findAll('td')
        community_area = table_data[1].find('a').text
        neighborhoods = table_data[2].findAll('a')
        for neighborhood in neighborhoods:
            formatted_neighborhood = normalize_string(neighborhood.text)
            if formatted_neighborhood in one_off_community_area_alternate_names:
                alternate_community_name = one_off_community_area_alternate_names[formatted_neighborhood]
                neighborhood_to_community_area[alternate_community_name] = normalize_string(community_area)
            else:
                neighborhood_to_community_area[formatted_neighborhood] = normalize_string(community_area)

with open('data/neighborhood_to_community_area.json', 'w') as json_file:
    json.dump(neighborhood_to_community_area, json_file, indent=1)
