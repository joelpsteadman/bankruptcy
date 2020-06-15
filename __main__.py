import os # for looping through files in a directory, and getting current directory
import logging
import sys, csv

from models.PUMA import *
from models.CountyFragment import *
from models.County import *
from models.Household import *
from services.household_service import *
from services.person_service import *
from services.county_service import *
from services.county_fragment_service import *
from services.puma_service import *
from services.population_service import Population_Calculator

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - [%(lineno)d] %(levelname)s: %(message)s', datefmt='%I:%M:%S %p')

dict_of_PUMAs_by_year = dict()
dict_of_households_by_year = dict()
dict_of_people_by_year = dict()
dict_of_counties_by_year = dict()
dict_of_cfs_by_year = dict()
years = dict() # making a dict so that it is easy to not create duplicates

year = '0000'

current_path = os.getcwd()
logging.debug("current_path: %s", current_path)

if 'bankruptcy' not in current_path:
    current_path = current_path + '/bankruptcy'

# Set up Population_By_Year
population_by_year_directory = os.path.join(current_path, 'files')
logging.debug("Collecting population change data")
filepath = os.path.join(population_by_year_directory, 'Population_By_Year.csv')
population_calculator = Population_Calculator(filepath)

issue_log = os.path.join(current_path, 'files/issues.log')

with open(issue_log, 'w') as file:
    file.write('')

logging.debug('Population change data collected')

# Collect household ACS data
# household_ACS_directory = os.path.join(current_path, 'files/Household_ACS')
# logging.debug("household_ACS_directory: %s", household_ACS_directory)
# for file in os.listdir(household_ACS_directory):
#     filename = os.fsdecode(file)
#     year = filename[0:4]
#     years[year] = ''
#     filepath = os.path.join(household_ACS_directory, filename)
#     logging.info("Collecting data from %s", filepath)
#     if year in dict_of_households_by_year:
#         dict_of_households_by_year[year].update(get_acs_household_data(filepath, year))
#     else:
#         dict_of_households_by_year[year] = get_acs_household_data(filepath, year)

# Collect person ACS data
person_ACS_directory = os.path.join(current_path, 'files/Person_ACS')
logging.debug("person_ACS_directory: %s", person_ACS_directory)
for file in os.listdir(person_ACS_directory):
# for file in os.listdir(person_ACS_directory)[0:1]: # just read the first person file to speed up testing time
    filename = os.fsdecode(file)
    year = filename[0:4]
    years[year] = ''
    filepath = os.path.join(person_ACS_directory, filename)
    logging.info("Collecting data from %s", filepath)
    # numbers = get_responses(filepath, year)
    # logging.debug('divorced: %s, insured: %s, black: %s, disabled: %s, veteran: %s, immigrant: %s', numbers[0], numbers[1], numbers[2], numbers[3], numbers[4], numbers[5])
    if year in dict_of_people_by_year:
        dict_of_people_by_year[year].update(get_acs_person_data(filepath, year))
    else:
        dict_of_people_by_year[year] = get_acs_person_data(filepath, year)

# Collect county data
county_bankruptcy_directory = os.path.join(current_path, 'files/County_Bankruptcies')
logging.debug("county_bankruptcy_directory: %s", county_bankruptcy_directory)
for file in os.listdir(county_bankruptcy_directory):
    filename = os.fsdecode(file)
    year = filename[0:4]
    years[year] = ''
    filepath = os.path.join(county_bankruptcy_directory, filename)
    logging.info("Collecting data from %s", filepath)
    if year in dict_of_counties_by_year:
        dict_of_counties_by_year[year].update(get_county_data(filepath, year))
    else:
        dict_of_counties_by_year[year] = get_county_data(filepath, year)

# Collect county_fragment data
county_to_puma_directory = os.path.join(current_path, 'files')
logging.debug("county_to_puma_directory: %s", county_to_puma_directory)
filepath = os.path.join(county_to_puma_directory, 'PUMA_to_county.csv')
for year in years:
    dict_of_cfs_by_year[year] = get_cf_data(filepath, year)

# Collect puma data
for year in years:
    dict_of_PUMAs_by_year[year] = get_puma_data(filepath, year)

for year_key in dict_of_cfs_by_year:
    cfs = dict_of_cfs_by_year[year_key]
    i = 0
    for cf_key in cfs:
        i += 1
        cf = cfs[cf_key]
        cf.population = population_calculator.get_population(cf.county_code, year_key, cf.population)
        b = '1.' + str(i)
        print (b, end="\r")

for year_key in dict_of_cfs_by_year:
    year_of_cfs = dict_of_cfs_by_year[year_key]
    i = 0
    for cf_key in year_of_cfs:
        i += 1
        cf = year_of_cfs[cf_key]
        # cf.population = Population_Calculator.get_population(cf.county_code)
        # county.population += float(cf.population)
        year_of_counties = dict_of_counties_by_year[year_key]
        if cf.county_code in year_of_counties:
            county = year_of_counties[cf.county_code]
            cf.county = county
            county.population += float(cf.population)
            county.used = True
        else:
            # logging.warning('No county found for county fragment with code %s', cf.county_code)
            with open(issue_log, 'a') as file:
                s = 'No county found for county fragment with code: ' + cf.county_code + '\n'
                file.write(s)
        year_of_PUMAs = dict_of_PUMAs_by_year[year_key]
        if cf.puma in year_of_PUMAs:
            puma = year_of_PUMAs[cf.puma]
            puma.cfs.append(cf)
            year_of_PUMAs[cf.puma].has_cf = True
        else:
            # logging.warning('No PUMA found for PUMA id %s', cf.puma)
            with open(issue_log, 'a') as file:
                s = 'No PUMA found for PUMA id ' + cf.puma + '\n'
                file.write(s)
        b = '2.' + str(i)
        print (b, end="\r")
for year_key in dict_of_counties_by_year:
    year_of_counties = dict_of_counties_by_year[year_key]
    i = 0
    for county_key in year_of_counties:
        i += 1
        county = year_of_counties[county_key]
        if not county.used:
            # logging.warning('County with code: %s, name: %s, and %d bankruptcies not accounted for in county fragments', county.code, county.name, county.bankruptcies)
            with open(issue_log, 'a') as file:
                s = 'County with code: ' + county.code + ' not accounted for in county fragments' + '\n'
                file.write(s)
        b = '3.' + str(i)
        print (b, end="\r")
for year_key in dict_of_people_by_year:
    year_of_people = dict_of_people_by_year[year_key]
    i = 0
    for person_key in year_of_people:
        i += 1
        person = year_of_people[person_key]
        year_of_PUMAs = dict_of_PUMAs_by_year[year_key]
        if person.puma in year_of_PUMAs:
            puma = year_of_PUMAs[person.puma]
            puma.people.append(person)
            puma.has_person = True
        else:
            # logging.warning('No PUMA found with id %s for person %s', person.puma, person.serial_number)
            with open(issue_log, 'a') as file:
                s = 'No PUMA found with id: ' + person.puma + ' for person...' + '\n'
                file.write(s)
        b = 'Setting up Person ' + str(i) + ' for ' + year_key + '    '
        print (b, end="\r")
# for year_key in dict_of_households_by_year:
#     year_of_households = dict_of_households_by_year[year_key]
#     i = 1
#     for household_key in year_of_households:
#         i += 1
#         household = year_of_households[household_key]
#         year_of_PUMAs = dict_of_PUMAs_by_year[year_key]
#         if household.puma in year_of_PUMAs:
#             puma = year_of_PUMAs[household.puma]
#             puma.households.append(household)
#             puma.has_household = True
#         else:
#             # logging.warning('No PUMA found with id %s for household %s', household.puma, household.id)
#             with open(issue_log, 'a') as file:
#                 s = 'No PUMA found with id: ' + household.puma + ' for household...' + '\n'
#                 file.write(s)
#         b = '4.' + str(i)
#         print (b, end="\r")
for year_key in dict_of_PUMAs_by_year:
    year_of_PUMAs = dict_of_PUMAs_by_year[year_key]
    i = 0
    for puma_key in year_of_PUMAs:
        i += 1
        puma = year_of_PUMAs[puma_key]
        if not puma.has_cf:
            # logging.warning('PUMA with id: %s does not have any a county fragments', puma.id)
            with open(issue_log, 'a') as file:
                s = 'PUMA with id: ' + puma.id + ' does not have any county fragments' + '\n'
                file.write(s)
        if not puma.has_person:
            # logging.warning('PUMA with id: %s does not have any people', puma.id)
            with open(issue_log, 'a') as file:
                s = 'PUMA with id: ' + puma.id + ' does not have any people' + '\n'
                file.write(s)
        if not puma.has_household:
            with open(issue_log, 'a') as file:
                s = 'PUMA with id: ' + puma.id + ' does not have any households' + '\n'
                file.write(s)
        #     logging.warning('PUMA with id: %s does not have any households', puma.id)
        b = 'Setting up PUMA ' + str(i) + ' for ' + year_key + '    '
        print (b, end="\r")

columns = ['Divorce', 'Age', 'Education', 'Insurance', 'Black', 'Disabled', 'Veteran', 'Immigrant', 'Unemployed', 'Bankruptcy']
# name of output file  
filename = "./files/puma-output.csv"
# writing to csv file  
with open(filename, 'w') as csvfile:  
    # creating a csv writer object  
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(columns)
    for year_key in dict_of_PUMAs_by_year:
        year_of_PUMAs = dict_of_PUMAs_by_year[year_key]
        for puma_key in year_of_PUMAs:
            puma = year_of_PUMAs[puma_key]
            
            bankruptcy_rate = puma.get_bankruptcy_rate()
            row = [puma.get_divorced_rate(), puma.get_portion_35_to_54(), puma.get_portion_hs_or_some_college(), puma.get_insured_rate(), puma.get_black_rate(), puma.get_disabled_rate(), puma.get_veteran_rate(), puma.get_immigrant_rate(), puma.get_unemployed_rate(), bankruptcy_rate]
            if bankruptcy_rate != 'NA':
                csvwriter.writerow(row)
                if bankruptcy_rate > 0.01:
                    with open(issue_log, 'a') as file:
                        s = 'Bankruptcy rate is ' + str(bankruptcy_rate) + ' for puma ' + puma.id + '\n'
                        file.write(s)
            else:
                with open(issue_log, 'a') as file:
                    s = 'Bankruptcy is NA for puma with id: ' + puma.id + '\n'
                    file.write(s)

        
logging.info("COMPLETE")
logging.info("COMPLETE")
logging.info("COMPLETE")
logging.info("COMPLETE")