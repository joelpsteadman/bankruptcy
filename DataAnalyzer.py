import csv
from Utilities import dollarValueOf
from Household import Household

with open('psam_h54.csv') as csvfile:
    file_reader = csv.reader(csvfile)
    line = next(file_reader)
    # find indexes corresponding to variables that I want
    indices = dict()
    # TODO move to another function in another file
    indices['id'] = line.index('SERIALNO')
    indices['puma'] = line.index('PUMA')
    indices['numPeople'] = line.index('NP')
    indices['acres'] = line.index('PUMA')
    indices['agSales'] = line.index('ACR')
    indices['bath'] = line.index('AGS')
    indices['numBedrooms'] = line.index('BATH')
    indices['numUnits'] = line.index('BDSP')
    indices['electricCostPM'] = line.index('BLD')
    indices['snap'] = line.index('ELEP')
    indices['fuelCostPM'] = line.index('FULP')
    indices['gasCostPM'] = line.index('GASP')
    indices['insuranceCostPY'] = line.index('INSP')
    indices['mobileHomeCostPY'] = line.index('MHP')
    indices['insuranceIncluded'] = line.index('MRGI')
    indices['firstMortgageCostPM'] = line.index('MRGP')
    indices['includeTax'] = line.index('MRGT')
    indices['numRooms'] = line.index('RMSP')
    indices['mealsIncluded'] = line.index('RNTM')
    indices['rentPM'] = line.index('RNTP')
    indices['secondaryMortgagesPM'] = line.index('SMP')
    indices['tenure'] = line.index('TEN')
    indices['propertyValue'] = line.index('VALP')
    indices['numVehicles'] = line.index('VEH')
    indices['waterCostPY'] = line.index('WATP')
    indices['whenStructureBuilt'] = line.index('YBL')
    indices['familyTypeAndEmployment'] = line.index('FES')
    indices['familyIncomePY'] = line.index('FINCP')
    indices['grossRentPM'] = line.index('GRNTP')
    indices['percentHouseholdIncomeThatIsRent'] = line.index('GRPIP')
    indices['householdIncomePY'] = line.index('HINCP')

    dictionary_of_households = dict()

    print("ID:\t\tExpenses:\t\tIncome:\t\tBudget:")
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
# totalEntriesWithNecessaryData = 0
totalFamilyIncome = 0
totalHouseholdIncome = 0
numEntriesThatIncludeFamilyIncome = 0
totalFamilyIncome = 0.0
numEntriesThatIncludeHouseholdIncome = 0
totalHouseholdIncome = 0.0
numBelowBudget = 0
ID = 1
totalNumVars = 0
for household in dictionary_of_households:
    household = dictionary_of_households[household]
    # print("Household income: ", household.income.householdIncomePY, ", == ''?: ", household.income.householdIncomePY == '')
    if household.income.familyIncomePY != '':
        numEntriesThatIncludeFamilyIncome += 1
        totalFamilyIncome += float(household.income.familyIncomePY)
    if household.income.householdIncomePY != '':
        numEntriesThatIncludeHouseholdIncome += 1
        totalHouseholdIncome += float(household.income.householdIncomePY)
    totalPeople += float(household.numPeople)
    try:
        totalFamilyIncome += float(household.income.familyIncomePY)
    except:
        pass
    try:
        totalHouseholdIncome += float(household.income.householdIncomePY)
    except:
        pass
    # print("Budget based on family income: ", household.familyBudget)
    # print("Budget based on household income: ", household.householdBudget)
    add = False
    numVars = household.expenses.numVariablesINeed
    try:
        if float(household.familyBudget) <= 0:
            numVars += 1
            add = True
    except:
        pass
    try:
        if float(household.householdBudget) <= 0:
            numVars += 1
            add = True
    except:
        pass
    if add:
        numBelowBudget += 1
    if household.income.familyIncomePY != '' and add:
        print(ID, "\t\t\t", dollarValueOf(float(household.expenses.totalExpenses)), "\t", dollarValueOf(float(household.income.familyIncomePY)/12), "\t", dollarValueOf(household.familyBudget))
    ID +=1
    numVars = household.expenses.numVariablesINeed
    totalNumVars += numVars
    # if household.expenses.hasNecessaryExpenseData:
    #     totalEntriesWithNecessaryData += 1

# print("Entries with required data to calculate total expenses: ", totalEntriesWithNecessaryData)
print("Households below $0 budget: ", numBelowBudget)
print("Entries with family income: ", numEntriesThatIncludeFamilyIncome, "/", len(dictionary_of_households))
print("Entries with household income: ", numEntriesThatIncludeHouseholdIncome, "/", len(dictionary_of_households))
print("Average People Per Household: ", totalPeople * 1.0 / len(dictionary_of_households))
print("Average Family Income Per Year: ", dollarValueOf(totalFamilyIncome * 1.0 / numEntriesThatIncludeFamilyIncome))
print("Average Household Income Per Year: ", dollarValueOf(totalHouseholdIncome * 1.0 / numEntriesThatIncludeHouseholdIncome))
print("Average # of variables provided: ", totalNumVars * 1.0 /len(dictionary_of_households))
print("Done")