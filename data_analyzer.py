import csv
import logging
from Utilities import dollarValueOf
from models.Household import *

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - [%(lineno)d] %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

with open('psam_h54.csv') as csvfile:
    file_reader = csv.reader(csvfile)
    line = next(file_reader)
    # find indexes corresponding to variables that I want
    indices = dict()
    # TODO move to another function in another file
    indices['id'] = line.index('SERIALNO')
    indices['state'] = line.index('ST')
    indices['puma'] = line.index('PUMA')
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

    dictionary_of_households = dict()

    logging.info("ID:\t\tExpenses:\t\tIncome:\t\t_budget:")
    i = 1
    try:
        while True:
        # while i < 10:
            acs_row = next(file_reader)
            household = Household(acs_row, indices)
            dictionary_of_households[acs_row[indices['id']]] = household
            i += 1
    except StopIteration:
        pass

totalPeople = 0
totalFamilyIncome = 0
totalHouseholdIncome = 0
numEntriesThatIncludeFamilyIncome = 0
totalFamilyIncome = 0.0
numEntriesThatIncludeHouseholdIncome = 0
totalHouseholdIncome = 0.0
numBelow_budget = 0
ID = 1
totalNumVars = 0
for household in dictionary_of_households:
    household = dictionary_of_households[household]
    # print("Household income: ", household.income.household_income_py, ", == ''?: ", household.income.household_income_py == '')
    if household.income.family_income_py != '':
        numEntriesThatIncludeFamilyIncome += 1
        totalFamilyIncome += float(household.income.family_income_py)
    if household.income.household_income_py != '':
        numEntriesThatIncludeHouseholdIncome += 1
        totalHouseholdIncome += float(household.income.household_income_py)
    totalPeople += float(household.num_people)
    try:
        totalFamilyIncome += float(household.income.family_income_py)
    except:
        pass
    try:
        totalHouseholdIncome += float(household.income.household_income_py)
    except:
        pass
    add = False
    numVars = household.expenses.num_variables_needed
    try:
        if float(household.family_budget) <= 0:
            numVars += 1
            add = True
    except:
        pass
    try:
        if float(household.household_budget) <= 0:
            numVars += 1
            add = True
    except:
        pass
    if add:
        numBelow_budget += 1
    if household.income.family_income_py != '' and add:
        logging.info("%d\t\t\t%s\t%s\t%s", ID, dollarValueOf(float(household.expenses.total_expenses)), dollarValueOf(float(household.income.family_income_py)/12), dollarValueOf(household.family_budget))
    ID +=1
    numVars = household.expenses.num_variables_needed
    totalNumVars += numVars

# print("Entries with required data to calculate total expenses: ", totalEntriesWithNecessaryData)
logging.info("Households below $0 budget: %d", numBelow_budget)
logging.info("Entries with family income: %d/%d", numEntriesThatIncludeFamilyIncome, len(dictionary_of_households))
logging.info("Entries with household income: %d/%d", numEntriesThatIncludeHouseholdIncome, len(dictionary_of_households))
logging.info("Average People Per Household: %f", totalPeople * 1.0 / len(dictionary_of_households))
logging.info("Average Family Income Per Year: %s", dollarValueOf(totalFamilyIncome * 1.0 / numEntriesThatIncludeFamilyIncome))
logging.info("Average Household Income Per Year: %s", dollarValueOf(totalHouseholdIncome * 1.0 / numEntriesThatIncludeHouseholdIncome))
logging.info("Average # of variables provided: %f", totalNumVars * 1.0 /len(dictionary_of_households))
logging.info("Done")