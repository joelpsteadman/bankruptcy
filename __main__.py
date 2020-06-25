import os # for looping through files in a directory, and getting current directory
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
from Utilities import Logger

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

dict_of_PUMAs_by_year = dict()
dict_of_households_by_year = dict()
dict_of_people_by_year = dict()
dict_of_counties_by_year = dict()
dict_of_cfs_by_year = dict()
years = dict() # making a dict so that it is easy to not create duplicates

year = '0000'

current_path = os.getcwd()

if 'bankruptcy' not in current_path:
    current_path = current_path + '/bankruptcy'

# set up personal logger
logger = Logger()
logger.define_issue_log(os.path.join(current_path, 'files/issues.log'), overwrite=True)

# Set up Population_By_Year
population_by_year_directory = os.path.join(current_path, 'files')
logger.log("Collecting population change data")
filepath = os.path.join(population_by_year_directory, 'Population_By_Year.csv')
population_calculator = Population_Calculator(filepath)

logger.log('Population change data collected')

# Collect household ACS data
# household_ACS_directory = os.path.join(current_path, 'files/Household_ACS')
# logger.log("household_ACS_directory:", household_ACS_directory)
# for file in os.listdir(household_ACS_directory):
#     filename = os.fsdecode(file)
#     year = filename[0:4]
#     years[year] = ''
#     filepath = os.path.join(household_ACS_directory, filename)
#     logger.log("Collecting data from", filepath)
#     if year in dict_of_households_by_year:
#         dict_of_households_by_year[year].update(get_acs_household_data(filepath, year))
#     else:
#         dict_of_households_by_year[year] = get_acs_household_data(filepath, year)

# Collect person ACS data
person_ACS_directory = os.path.join(current_path, 'files/Person_ACS')
for file in os.listdir(person_ACS_directory):
# for file in os.listdir(person_ACS_directory)[0:1]: # just read the first person file to speed up testing time
    filename = os.fsdecode(file)
    year = filename[0:4]
    years[year] = ''
    filepath = os.path.join(person_ACS_directory, filename)
    logger.log("Collecting data from", filepath)
    # numbers = get_responses(filepath, year)
    # logger.log('divorced:', numbers[0], 'insured:', numbers[1], 'black:', numbers[2], 'disabled:', numbers[3], 'veteran:', numbers[4], 'immigrant:', numbers[5], 'unemployed:', numbers[6])
    if year in dict_of_people_by_year:
        dict_of_people_by_year[year].update(get_acs_person_data(filepath, year))
    else:
        dict_of_people_by_year[year] = get_acs_person_data(filepath, year)

# Collect county data
county_bankruptcy_directory = os.path.join(current_path, 'files/County_Bankruptcies')
logger.log("county_bankruptcy_directory:", county_bankruptcy_directory)
for file in os.listdir(county_bankruptcy_directory):
    filename = os.fsdecode(file)
    year = filename[0:4]
    years[year] = ''
    filepath = os.path.join(county_bankruptcy_directory, filename)
    logger.log("Collecting data from", filepath)
    if year in dict_of_counties_by_year:
        dict_of_counties_by_year[year].update(get_county_data(filepath, year))
    else:
        dict_of_counties_by_year[year] = get_county_data(filepath, year)

# Collect county_fragment data
county_to_puma_directory = os.path.join(current_path, 'files')
logger.log("county_to_puma_directory:", county_to_puma_directory)
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
        logger.log('Setting population for cf', i, 'in', year_key, erase=True)

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
            logger.record_issue('No county found for county fragment with code:', cf.county_code)
        year_of_PUMAs = dict_of_PUMAs_by_year[year_key]
        if cf.puma in year_of_PUMAs:
            puma = year_of_PUMAs[cf.puma]
            puma.cfs.append(cf)
            year_of_PUMAs[cf.puma].has_cf = True
        else:
            logger.record_issue('No PUMA found for PUMA id', cf.puma)
        logger.log('Finding a PUMA for cf', i, 'in', year_key, erase=True)
for year_key in dict_of_counties_by_year:
    year_of_counties = dict_of_counties_by_year[year_key]
    i = 0
    for county_key in year_of_counties:
        i += 1
        county = year_of_counties[county_key]
        if not county.used:
            logger.record_issue('County with code:', county.code, 'name:', county.name, 'and', county.bankruptcies, 'bankruptcies not accounted for in county fragments')
        logger.log('Checking that county', i, 'has a cf', erase=True)
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
            logger.record_issue('No PUMA found with id', person.PUMA, 'for person', person.serial_number)
        logger.log('Finding a PUMA for person', i, 'in', year_key, erase=True)
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
#            logger.record_issue('No PUMA found with id', household.PUMA, 'for household', household.id)
#         logger.log('Finding a PUMA for household', i, 'in', year_key, erase=True)
for year_key in dict_of_PUMAs_by_year:
    year_of_PUMAs = dict_of_PUMAs_by_year[year_key]
    i = 0
    for puma_key in year_of_PUMAs:
        i += 1
        puma = year_of_PUMAs[puma_key]
        if not puma.has_cf:
            logger.record_issue('PUMA with name:', puma.name, 'does not have any county fragments')
        if not puma.has_person:
            logger.record_issue('PUMA with name:', puma.name, 'does not have any people')
        # if not puma.has_household:
        #     logger.record_issue('PUMA with name:', puma.name, 'does not have any households')
        logger.log('Checking that PUMA', i, 'in', year_key, 'has people and cfs', erase=True)

columns = ['Divorce', 'Age', 'Education', 'Insurance', 'Black', 'Disabled', 'Veteran', 'Immigrant', 'Unemployed', 'Bankruptcy', 'PUMA']
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
            row = [puma.get_divorced_rate(), puma.get_portion_35_to_54(), puma.get_portion_hs_or_some_college(), puma.get_insured_rate(), puma.get_black_rate(), puma.get_disabled_rate(), puma.get_veteran_rate(), puma.get_immigrant_rate(), puma.get_unemployed_rate(), bankruptcy_rate, puma.name]
            if bankruptcy_rate != 'NA':
                csvwriter.writerow(row)
                if bankruptcy_rate > 0.01:
                    logger.record_issue('Bankruptcy rate is', bankruptcy_rate, 'for puma', puma.name)
            else:
                logger.record_issue('Bankruptcy is NA for puma with name:', puma.name)
        
logger.log('# of issues:', logger.get_num_issues())
logger.log("COMPLETE")
logger.log("COMPLETE")
logger.log("COMPLETE")
logger.log("COMPLETE")