import csv

from models.Household import *

# TODO update to match the better syntax used in person_service

# @param filepath takes a file path as a string
# @param year the year that this ACS data is from
# @return returns a dictionary of Household objects
def get_acs_household_data(filepath, year):

    dictionary_of_households = dict()

    with open(filepath) as csvfile:
        file_reader = csv.reader(csvfile)
        line = next(file_reader)
        # find indexes corresponding to variables that I want
        indices = dict()
        # TODO move to another function in another file
        indices['id'] = line.index('SERIALNO')
        indices['state'] = line.index('ST')
        indices['puma'] = line.index('ST') + line.index('PUMA')
        indices['num_people'] = line.index('NP')
        indices['acres'] = line.index('ACR')
        indices['ag_sales'] = line.index('AGS')
        indices['bath'] = line.index('BATH')
        indices['num_bedrooms'] = line.index('BDSP')
        indices['num_units'] = line.index('BLD')
        indices['electric_cost_pm'] = line.index('ELEP')
        indices['fuel_cost_pm'] = line.index('FULP')
        indices['gas_cost_pm'] = line.index('GASP')
        indices['insurance_cost_py'] = line.index('INSP')
        indices['mobile_home_cost_py'] = line.index('MHP')
        indices['insurance_included'] = line.index('MRGI')
        indices['first_mortgage_cost_pm'] = line.index('MRGP')
        indices['include_tax'] = line.index('MRGT')
        indices['num_rooms'] = line.index('RMSP')
        indices['meals_included'] = line.index('RNTM')
        indices['rent_pm'] = line.index('RNTP')
        indices['secondary_mortgages_pm'] = line.index('SMP')
        indices['tenure'] = line.index('TEN')
        indices['property_value'] = line.index('VALP')
        indices['num_vehicles'] = line.index('VEH')
        indices['water_cost_py'] = line.index('WATP')
        indices['when_structure_built'] = line.index('YBL')
        indices['family_type_and_employment'] = line.index('FES')
        indices['family_income_py'] = line.index('FINCP')
        indices['gross_rent_pm'] = line.index('GRNTP')
        indices['percent_household_income_that_is_rent'] = line.index('GRPIP')
        indices['household_income_py'] = line.index('HINCP')

        # logging.info("ID:\t\tExpenses:\t\tIncome:\t\t_budget:")
        try:
            while True:
            # while i < 10:
                acs_row = next(file_reader)
                household = Household(acs_row, indices)
                id = str(acs_row[indices['id']]) + str(acs_row[indices['state']]) + year
                dictionary_of_households[id] = household
        except StopIteration:
            pass
        
    return dictionary_of_households