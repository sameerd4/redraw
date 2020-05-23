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

with open('cencounts.csv', encoding='latin1') as f:
    reader = csv.reader(f)
    next(reader)
    for line in reader:
        county = line[11][3:]
        abbrev = line[11][:2]
        if line[9] != '.':
            print(county, abbrev, int(line[9]))
            county_pop_dict[(county, abbrev)] = int(line[9])

        

print(county_pop_dict)

county_vote_dict = {}
with open('mit_2000.csv', encoding='latin1') as f:
    reader = csv.reader(f)
    next(reader)
    count = 0
    for line in reader:
#        if count % 3 == 0:
            county = line[3]
            abbrev = line[2]
            dem_vote = int(line[8])
#            print(line)
            line = next(reader)
            rep_vote = int(line[8])
#            print(line)
            line = next(reader)

            if line[8] != "NA":
                grn_vote = int(line[8])
            else:
                grn_vote = 0

            line = next(reader)
            if line[8] != "NA":
                oth_vote = int(line[8])
            else:
                oth_vote = 0
#            print(line)
#            print(county, abbrev, dem_vote, rep_vote, grn_vote, oth_vote)
            county_vote_dict[county, abbrev] = (dem_vote, rep_vote, grn_vote, oth_vote)

#        count += 3


#        county_vote_dict[(line[1], line[0])] = (int(line[3]), int(line[4]))
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

            if county == "Alaska" and state == "AK":
                print("Alaska, AK")
                data['objects']['counties']['geometries'][i]['properties']['dem'] = 79004
                data['objects']['counties']['geometries'][i]['properties']['gop'] = 167398
                data['objects']['counties']['geometries'][i]['properties']['lib'] = 0
                data['objects']['counties']['geometries'][i]['properties']['grn'] = 28747
                data['objects']['counties']['geometries'][i]['properties']['oth'] = 10411
                data['objects']['counties']['geometries'][i]['properties']['una'] = 0

            elif county == 'Jackson' and state == 'MO':
                print("Jackson County, MO and Kansas City, MO")
#                print(county_vote_dict[county, state])
                total_jackson_dem = county_vote_dict[county, state][0] + county_vote_dict["Kansas City", state][0]
                total_jackson_gop = county_vote_dict[county, state][1] + county_vote_dict["Kansas City", state][1]
                total_jackson_grn = county_vote_dict[county, state][2] + county_vote_dict["Kansas City", state][2]
                total_jackson_oth = county_vote_dict[county, state][3] + county_vote_dict["Kansas City", state][3]
                print(total_jackson_dem, total_jackson_gop, total_jackson_oth)
                data['objects']['counties']['geometries'][i]['properties']['dem'] = total_jackson_dem
                data['objects']['counties']['geometries'][i]['properties']['gop'] = total_jackson_gop
                data['objects']['counties']['geometries'][i]['properties']['lib'] = 0
                data['objects']['counties']['geometries'][i]['properties']['oth'] = total_jackson_oth
                data['objects']['counties']['geometries'][i]['properties']['una'] = 0
            elif county == 'Washington' and state == 'DC':
                print("Washington, DC")
                data['objects']['counties']['geometries'][i]['properties']['dem'] = county_vote_dict["District of Columbia", state][0]
                data['objects']['counties']['geometries'][i]['properties']['gop'] = county_vote_dict["District of Columbia", state][1]
                data['objects']['counties']['geometries'][i]['properties']['lib'] = 0
                data['objects']['counties']['geometries'][i]['properties']['grn'] = county_vote_dict["District of Columbia", state][2]
                data['objects']['counties']['geometries'][i]['properties']['oth'] = county_vote_dict["District of Columbia", state][3]
                data['objects']['counties']['geometries'][i]['properties']['una'] = 0

            elif county == 'La Salle' and state == 'IL':
                print("La Salle, IL")
                data['objects']['counties']['geometries'][i]['properties']['dem'] = county_vote_dict["LaSalle", state][0]
                data['objects']['counties']['geometries'][i]['properties']['gop'] = county_vote_dict["LaSalle", state][1]
                data['objects']['counties']['geometries'][i]['properties']['lib'] = 0
                data['objects']['counties']['geometries'][i]['properties']['grn'] = county_vote_dict["LaSalle", state][2]
                data['objects']['counties']['geometries'][i]['properties']['oth'] = county_vote_dict["LaSalle", state][3]
                data['objects']['counties']['geometries'][i]['properties']['una'] = 0                

            elif county == 'Baltimore County' and state == 'MD':
                print("Baltimore County, MD")
                data['objects']['counties']['geometries'][i]['properties']['dem'] = county_vote_dict["Baltimore", state][0]
                data['objects']['counties']['geometries'][i]['properties']['gop'] = county_vote_dict["Baltimore", state][1]
                data['objects']['counties']['geometries'][i]['properties']['lib'] = 0
                data['objects']['counties']['geometries'][i]['properties']['grn'] = county_vote_dict["Baltimore", state][2]
                data['objects']['counties']['geometries'][i]['properties']['oth'] = county_vote_dict["Baltimore", state][3]
                data['objects']['counties']['geometries'][i]['properties']['una'] = 0      

            elif county == 'Shannon' and state == 'SD':
                print("Baltimore County, MD")
                data['objects']['counties']['geometries'][i]['properties']['dem'] = county_vote_dict["Oglala Lakota", state][0]
                data['objects']['counties']['geometries'][i]['properties']['gop'] = county_vote_dict["Oglala Lakota", state][1]
                data['objects']['counties']['geometries'][i]['properties']['lib'] = 0
                data['objects']['counties']['geometries'][i]['properties']['grn'] = county_vote_dict["Oglala Lakota", state][2]
                data['objects']['counties']['geometries'][i]['properties']['oth'] = county_vote_dict["Oglala Lakota", state][3]
                data['objects']['counties']['geometries'][i]['properties']['una'] = 0     
            else:
                if county != "Broomfield":
                    print(county_vote_dict[county, state])
                    data['objects']['counties']['geometries'][i]['properties']['dem'] = county_vote_dict[county, state][0]
                    data['objects']['counties']['geometries'][i]['properties']['gop'] = county_vote_dict[county, state][1]
                    data['objects']['counties']['geometries'][i]['properties']['lib'] = 0
                    data['objects']['counties']['geometries'][i]['properties']['grn'] = county_vote_dict[county, state][2]
                    data['objects']['counties']['geometries'][i]['properties']['oth'] = county_vote_dict[county, state][3]
                    data['objects']['counties']['geometries'][i]['properties']['una'] = 0

            population = 0

            if county == 'Washington' and state == 'DC':
                population = county_pop_dict['District of Columbia', state]
                print(county_pop_dict['District of Columbia', state])
            elif state == 'AK':
                population = 622091
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

with open('2000test.json', 'w') as outfile:
    json.dump(data, outfile)
