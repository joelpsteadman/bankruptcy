import os # for looping through files in a directory, and getting current directory
import logging
import os, sys, csv
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from models.PUMA import *
from models.CountyFragment import *
from models.County import *
from models.Household import *
from services.household_service import *
from services.person_service import *
from services.county_service import *
from services.county_fragment_service import *
from services.puma_service import *

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - [%(lineno)d] %(levelname)s: %(message)s', datefmt='%I:%M:%S %p')

dict_of_PUMAs = dict()
dict_of_households = dict()
dict_of_people = dict()
dict_of_counties = dict()
dict_of_cfs = dict()

year = '0000'

current_path = os.getcwd()
logging.debug("current_path: %s", current_path)

# Collect household ACS data
household_ACS_directory = os.path.join(current_path, 'files/Household_ACS')
logging.debug("household_ACS_directory: %s", household_ACS_directory)
for file in os.listdir(household_ACS_directory):
    filename = os.fsdecode(file)
    year = filename[0:4]
    logging.debug('year: %s', year)
    filepath = os.path.join(household_ACS_directory, filename)
    logging.info("Collecting data from %s", filepath)
    dict_of_households.update(get_acs_household_data(filepath, year))

    logging.debug('# of households created: %s', len(dict_of_households))

# Collect person ACS data
person_ACS_directory = os.path.join(current_path, 'files/Person_ACS')
logging.debug("person_ACS_directory: %s", person_ACS_directory)
for file in os.listdir(person_ACS_directory):
    filename = os.fsdecode(file)
    year = filename[0:4]
    logging.debug('year: %s', year)
    filepath = os.path.join(person_ACS_directory, filename)
    logging.info("Collecting data from %s", filepath)
    dict_of_people.update(get_acs_person_data(filepath, year))

    logging.debug('# of people created: %s', len(dict_of_people))

# Collect county data
county_bankruptcy_directory = os.path.join(current_path, 'files/County_Bankruptcies')
logging.debug("county_bankruptcy_directory: %s", county_bankruptcy_directory)
for file in os.listdir(county_bankruptcy_directory):
    filename = os.fsdecode(file)
    year = filename[0:4]
    logging.debug('year: %s', year)
    filepath = os.path.join(county_bankruptcy_directory, filename)
    logging.info("Collecting data from %s", filepath)
    dict_of_counties.update(get_county_data(filepath, year))

    logging.debug('# of counties created: %s', len(dict_of_counties))

# Collect county_fragment data
county_to_puma_directory = os.path.join(current_path, 'files')
logging.debug("county_to_puma_directory: %s", county_to_puma_directory)
filepath = os.path.join(county_to_puma_directory, 'PUMA_to_county.csv')
dict_of_cfs = get_cf_data(filepath)

logging.debug('# of CFs created: %s', len(dict_of_cfs))

# Collect puma data
dict_of_PUMAs = get_puma_data(filepath, year)

logging.debug('# of PUMAs created: %s', len(dict_of_PUMAs))

for cf_key in dict_of_cfs:
    cf = dict_of_cfs[cf_key]
    if cf.county_code in dict_of_counties:
        county = dict_of_counties[cf.county_code]
        cf.county = county
        county.population += float(cf.population)
        county.used = True
    else:
        logging.warning('No county found for county fragment with code %s', cf.county_code)
    if cf.puma in dict_of_PUMAs:
        puma = dict_of_PUMAs[cf.puma]
        puma.cfs.append(cf)
        dict_of_PUMAs[cf.puma].has_cf = True
    else:
        logging.warning('No PUMA found for PUMA id %s', cf.puma)
for county_key in dict_of_counties:
    county = dict_of_counties[county_key]
    if not county.used:
        logging.warning('County with code: %s, name: %s, and %d bankruptcies not accounted for in county fragments', county.code, county.name, county.bankruptcies)
for person_key in dict_of_people:
    person = dict_of_people[person_key]
    if person.puma in dict_of_PUMAs:
        puma = dict_of_PUMAs[person.puma]
        puma.people.append(person)
        puma.has_person = True
    else:
        logging.warning('No PUMA found with id %s for person %s', person.puma, person.serial_number)
for household_key in dict_of_households:
    household = dict_of_households[household_key]
    if household.puma in dict_of_PUMAs:
        puma = dict_of_PUMAs[household.puma]
        puma.households.append(household)
        puma.has_household = True
    else:
        pass
        # logging.warning('No PUMA found with id %s for household %s', household.puma, household.id)

for puma_key in dict_of_PUMAs:
    puma = dict_of_PUMAs[puma_key]
    if not puma.has_cf:
        logging.warning('PUMA with id: %s does not have any a county fragments', puma.id)
    if not puma.has_person:
        logging.warning('PUMA with id: %s does not have any people', puma.id)
    # if not puma.has_household:
    #     logging.warning('PUMA with id: %s does not have any households', puma.id)

columns = ['PUMA-ID', 'Bankruptcy_Rate', 'Median_Age', 'Divorce_Rate', 'In_The_Red_Rate', 'Insured_Rate', '35_to_54', '40_to_44', 'High_School_Grad', 'HS_or_some_college', 'Num_People', 'Num_Households']  
# name of output file  
filename = "./files/puma-output.csv"
# writing to csv file  
with open(filename, 'w') as csvfile:  
    # creating a csv writer object  
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(columns) 
    for puma_key in dict_of_PUMAs:
        puma = dict_of_PUMAs[puma_key]
        households = 0
        try:
            households = len(puma.households)
        except:
            pass
        people = 0
        try:
            people = len(puma.people)
        except:
            pass
        
        row = [puma_key, puma.get_bankruptcy_rate(), puma.get_median_age(), puma.get_divorced_rate(), puma.get_in_the_red_rate(), puma.get_insured_rate(), puma.get_portion_35_to_54(), puma.get_portion_40_to_44(), puma.get_highschool_graduation_rate(), puma.get_portion_hs_or_some_college(), people, households]
        csvwriter.writerow(row) 
        
logging.info("COMPLETE")
logging.info("COMPLETE")
logging.info("COMPLETE")
logging.info("COMPLETE")