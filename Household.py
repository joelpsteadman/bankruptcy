class Property:
    def __init__(self, acres, bath, numBedrooms, numUnits, numRooms, tenure, propertyValue, whenStructureBuilt, numVehicles):
        self.acres = acres
        self.bath = bath
        self.numBedrooms = numBedrooms
        self.numUnits = numUnits
        self.numRooms = numRooms
        self.tenure = tenure
        self.propertyValue = propertyValue
        self.whenStructureBuilt = whenStructureBuilt
        self.numVehicles = numVehicles


class Income:
    def __init__(self, agSales, familyIncomePY, householdIncomePY):
        self.agSales = agSales
        self.familyIncomePY = familyIncomePY
        self.householdIncomePY = householdIncomePY


class Expenses:
    def __init__(self, electricCostPM, fuelCostPM, gasCostPM, insuranceCostPY, mobileHomeCostPY, insuranceIncluded, firstMortgageCostPM, includeTax, mealsIncluded, rentPM, secondaryMortgagesPM, waterCostPY, whenStructureBuilt, grossRentPM):
        self.electricCostPM = electricCostPM
        self.fuelCostPM = fuelCostPM
        self.gasCostPM = gasCostPM
        self.insuranceCostPY = insuranceCostPY
        self.mobileHomeCostPY = mobileHomeCostPY
        self.insuranceIncluded = insuranceIncluded
        self.firstMortgageCostPM = firstMortgageCostPM
        self.includeTax = includeTax
        self.mealsIncluded = mealsIncluded
        self.rentPM = rentPM
        self.secondaryMortgagesPM = secondaryMortgagesPM
        self.waterCostPY = waterCostPY
        self.whenStructureBuilt = whenStructureBuilt
        self.grossRentPM = grossRentPM
        self.totalExpenses = self.getTotalExpenses()

    def getTotalExpenses(self):
        # def safeAdd(total, addition):
        total = 0
        self.numVariablesINeed = 10
        # self.hasNecessaryExpenseData = True
        # addition is a (str) variable, the int value of which needs to be added to the total
        # bottomCodes is the highest numeric option for the ACS variable that does not correspond to a numeric value
        def valueWithBottomCoding(addition, bottomCodes):
            if addition == '':
                self.numVariablesINeed -= 1
                # print(addition, " is not present, so expenses cannot be accurately calculated")
                # self.hasNecessaryExpenseData = False
            try:
                if int(addition) > bottomCodes:
                    # print("Total for ", addition, "  = ", int(addition))
                    return int(addition)
            except:
                pass
            return 0

        total += valueWithBottomCoding(self.electricCostPM, 2)
        total += valueWithBottomCoding(self.fuelCostPM, 2)
        total += valueWithBottomCoding(self.gasCostPM, 3)
        total += (valueWithBottomCoding(self.insuranceCostPY, 0) / 12)
        total += (valueWithBottomCoding(self.mobileHomeCostPY, 0) / 12)
        total += valueWithBottomCoding(self.firstMortgageCostPM, 0)
        if valueWithBottomCoding(self.grossRentPM, 0) > 0:
            total += valueWithBottomCoding(self.grossRentPM, 0)
        else:
            total += valueWithBottomCoding(self.rentPM, 0)
        total += valueWithBottomCoding(self.secondaryMortgagesPM, 0)
        total += (valueWithBottomCoding(self.waterCostPY, 0) / 12)
        # print("Total = ", total)
        return total


class Demographics:
    def __init__(self, snap, familyTypeAndEmployment, percentHouseholdIncomeThatIsRent):
        self.snap = snap
        self.familyTypeAndEmployment = familyTypeAndEmployment
        self.percentHouseholdIncomeThatIsRent = percentHouseholdIncomeThatIsRent


class Household:
    def __init__(self, acs_row, indices):
        self.id = acs_row[indices['id']]
        self.puma = acs_row[indices['puma']]
        self.numPeople = acs_row[indices['numPeople']]
        self.property = Property(acs_row[indices['acres']], acs_row[indices['bath']], acs_row[indices['numBedrooms']], acs_row[indices['numUnits']], acs_row[indices['numRooms']],
                                 acs_row[indices['tenure']], acs_row[indices['propertyValue']], acs_row[indices['whenStructureBuilt']], acs_row[indices['numVehicles']])
        self.income = Income(
            acs_row[indices['agSales']], acs_row[indices['familyIncomePY']], acs_row[indices['householdIncomePY']])
        self.expenses = Expenses(acs_row[indices['electricCostPM']], acs_row[indices['fuelCostPM']], acs_row[indices['gasCostPM']], acs_row[indices['insuranceCostPY']], acs_row[indices['mobileHomeCostPY']], acs_row[indices['insuranceIncluded']], acs_row[indices['firstMortgageCostPM']],
                                 acs_row[indices['includeTax']], acs_row[indices['mealsIncluded']], acs_row[indices['rentPM']], acs_row[indices['secondaryMortgagesPM']], acs_row[indices['waterCostPY']], acs_row[indices['whenStructureBuilt']], acs_row[indices['grossRentPM']])
        self.demographics = Demographics(
            acs_row[indices['snap']], acs_row[indices['familyTypeAndEmployment']], acs_row[indices['percentHouseholdIncomeThatIsRent']])
        self.familyBudget = None
        self.householdBudget = None
        # if self.expenses.hasNecessaryExpenseData:
        if self.income.familyIncomePY != '':
            self.familyBudget = (float(self.income.familyIncomePY) / 12) - self.expenses.totalExpenses
        if self.income.householdIncomePY:
            self.householdBudget = (float(self.income.householdIncomePY) / 12) - self.expenses.totalExpenses

    def toString(self):
        str = "Household: " + self.id
        str += "\n- PUMA: " + self.puma
        str += "\n- Number of People: " + self.numPeople
        str += "\n- Property: "
        str += "\n  - Acres of land: " + self.property.acres
        str += "\n  - Bath and/or Shower Available: " + self.property.bath
        str += "\n  - Number of Bedrooms: " + self.property.numBedrooms
        str += "\n  - Number of Units in Building: " + self.property.numUnits
        str += "\n  - Number of Rooms: " + self.property.numRooms
        str += "\n  - Tenure: " + self.property.tenure
        str += "\n  - Property Value: " + self.property.propertyValue
        str += "\n  - When Structure Was Built: " + self.property.whenStructureBuilt
        str += "\n  - Number of Vehicles: " + self.property.numVehicles
        str += "\n- Income: "
        str += "\n  - Agricultural Sales: " + self.income.agSales
        str += "\n  - Family Income Per Year: " + self.income.familyIncomePY
        str += "\n  - Household Income Per Year: " + self.income.householdIncomePY
        str += "\n- Expenses: "
        str += "\n  - Monthly Electric Bill: " + self.expenses.electricCostPM
        str += "\n  - Monthly Fuel Costs: " + self.expenses.fuelCostPM
        str += "\n  - Monthly Gas Bill: " + self.expenses.gasCostPM
        str += "\n  - Annual Insurance Costs: " + self.expenses.insuranceCostPY
        str += "\n  - Annual Mobile Home Costs: " + self.expenses.mobileHomeCostPY
        str += "\n  - Insurance Included in First Mortgage? " + \
            self.expenses.insuranceIncluded
        str += "\n  - First Mortgage Per Month: " + self.expenses.firstMortgageCostPM
        str += "\n  - First Mortgage Includes Tax? " + self.expenses.includeTax
        str += "\n  - Meals Included in Rent? " + self.expenses.mealsIncluded
        str += "\n  - Rent Per Month: " + self.expenses.rentPM
        str += "\n  - Secondary Mortgage Payments Per Month: " + \
            self.expenses.secondaryMortgagesPM
        str += "\n  - Water Bill Per Year: " + self.expenses.waterCostPY
        str += "\n  - When Structure Built: " + self.expenses.whenStructureBuilt
        str += "\n  - Gross Rent Per Month: " + self.expenses.grossRentPM
        str += "\n- Demographics: "
        str += "\n  - SNAP Recipient? " + self.demographics.snap
        str += "\n  - Family Type and Employment: " + \
            self.demographics.familyTypeAndEmployment
        str += "\n  - Percent of Household Income Going to Rent: " + \
            self.demographics.percentHouseholdIncomeThatIsRent
        return str

        # print("PUMA for ", acs_row[indices['id']], " is: ", self.puma)

# Serial_Number
# Num of person records in household
# PUMA
# Property:
#     acres of land
#     bathtub / shower? (bool)
#     num of bedrooms
#     units in structure
#     Number of Rooms
#     Property value
#     When structure first built
#     Tenure (do you own, rent,..?)
#     Num of Vehicles
# Income:
#     sales of agricultural products
#     Family income (past 12 months)
#     Household income (past 12 months)
# Expenses:
#     Electricity - monthly
#     Other fuel - yearly
#     Gas - monthly
#     Fire/hazard/flood insurance (yearly amount)
#     Mobile home costs (yearly amount)
#     First mortgage payment includes fire/hazard/flood insurance? (bool)
#     First mortgage payment (monthly amount)
#     First mortgage payment includes real estate taxes? (bool)
#     Meals included in rent?
#     Rent - monthly
#     Total payment on all second and junior mortgages and home equity loans (monthly amount)
#     Water (yearly cost)
#     Gross rent (monthly amount)
#     Selected monthly owner costs (sum of house payment stuff)
#     Property taxes (yearly amount)
# Demographics:
#     SNAP recipientcy? (bool)
#     Family type and employment status
#     Gross rent as a percentage of household income past 12 months

# calculateExpenses()
