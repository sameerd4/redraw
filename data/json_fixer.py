import json
import csv
import os

STATES = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas',
'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey',
'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon',
'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas',
'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

STATE_ABBREVS = [
  'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL',
  'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME',
  'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH',
  'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI',
  'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI',
  'WY']

STATE_TO_ABBREV = dict(zip(STATES, STATE_ABBREVS))


county_pop_dict = {}

with open('DECENNIALSF12000.P001_data_with_overlays_2020-05-21T225549.csv', encoding='latin1') as f:
    reader = csv.reader(f)
    next(reader)
    for line in reader:
        county = line[1].split(", ")[0]
        state = line[1].split(", ")[1]
        print(county, STATE_TO_ABBREV[state], int(line[2]))
        county_pop_dict[(county, STATE_TO_ABBREV[state])] = int(line[2])


#print(county_pop_dict)

county_vote_dict = {}
with open('data_2008.csv', encoding='latin1') as f:
    reader = csv.reader(f)
    next(reader)
    for line in reader:
        county_vote_dict[(line[1], line[0])] = (int(line[3]), int(line[4]))
#        county_vote_dict.update({line[1] : int(line[3])})

#print(county_vote_dict)
data = {}

print()
print()

va_count = 0

exceptions = ['Alaska', 'Broomfield']
with open('us2008.json') as json_file:
    data = json.load(json_file)
    i = 0
    while i < 3115:
        if 'properties' in data['objects']['counties']['geometries'][i]:
          #  print(data['objects']['counties']['geometries'][i]['properties'])
            county = data['objects']['counties']['geometries'][i]['properties']['name']
            state = data['objects']['counties']['geometries'][i]['properties']['state']

            data['objects']['counties']['geometries'][i]['properties']['dem'] = county_vote_dict[county, state][0]
            data['objects']['counties']['geometries'][i]['properties']['gop'] = county_vote_dict[county, state][1]
            data['objects']['counties']['geometries'][i]['properties']['lib'] = 0
            data['objects']['counties']['geometries'][i]['properties']['oth'] = 0
            data['objects']['counties']['geometries'][i]['properties']['una'] = 0

            population = 0

            if county == 'Washington' and state == 'DC':
                population = county_pop_dict['District of Columbia', state]
                print(county_pop_dict['District of Columbia', state])
            elif state == 'LA':
                population = county_pop_dict[county + ' Parish', state]
                print(county_pop_dict[county + ' Parish', state])
            elif county == 'Baltimore County' and state == 'MD':
                population = county_pop_dict[county, state]
                print(county_pop_dict[county, state])
            elif county == 'Baltimore City' and state == 'MD':
                population = county_pop_dict['Baltimore city', state]
                print(county_pop_dict['Baltimore city', state])    
            elif county == 'St. Louis Co.' and state == 'MO':
                population = county_pop_dict['St. Louis County', state]
                print(county_pop_dict['St. Louis County', state]) 
            elif county == 'St. Louis' and state == 'MO':
                population = county_pop_dict['St. Louis city', state]
                print(county_pop_dict['St. Louis city', state])                 
            elif county == 'Carson City' and state == 'NV':
                population = county_pop_dict['Carson City', state]
                print(county_pop_dict['Carson City', state])
            elif state == 'VA':
                if ' Co.' in county:
                    county_name = county.split(" Co.")
                    population = county_pop_dict[county_name[0] + ' County', state]
                    print(county, county_pop_dict[county_name[0] + ' County', state])
                else:
                    if va_count >= 95:
                        population = county_pop_dict[county + ' city', state]
                        print(county, county_pop_dict[county + ' city', state])
                    else:
                        population = county_pop_dict[county + ' County', state]
                        print(county, county_pop_dict[county + ' County', state])
                
                va_count += 1
            elif county not in exceptions:
                population = county_pop_dict[county + ' County', state]
                print(county, county_pop_dict[county + ' County', state])
            
            data['objects']['counties']['geometries'][i]['properties']['population'] = population
        i += 1

#    data['objects']['counties']['geometries'][0]['properties']['population'] = 43671
#    print(data['objects']['counties']['geometries'][0])
print()
print()
'''
with open('us.json') as json_file:
    data = json.load(json_file)
    for county in data['objects']['counties']['geometries']:
        if 'properties' in county:
            print(county['properties'])
'''
with open('test.json', 'w') as outfile:
    json.dump(data, outfile)
