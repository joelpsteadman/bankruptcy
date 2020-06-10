import numbers

class Property:
    def __init__(self, acres, bath, num_bedrooms, num_units, num_rooms, tenure, property_value, when_structure_built, num_vehicles):
        self.acres = acres
        self.bath = bath
        self.num_bedrooms = num_bedrooms
        self.num_units = num_units
        self.num_rooms = num_rooms
        self.tenure = tenure
        self.property_value = property_value
        self.when_structure_built = when_structure_built
        self.num_vehicles = num_vehicles


class Income:
    def __init__(self, ag_sales, family_income_py, household_income_py):
        self.ag_sales = ag_sales
        self.family_income_py = family_income_py
        self.household_income_py = household_income_py


class Expenses:
    def __init__(self, electric_cost_pm, fuel_cost_pm, gas_cost_pm, insurance_cost_py, mobile_home_cost_py, insurance_included, first_mortgage_cost_pm, include_tax, meals_included, rent_pm, secondary_mortgages_pm, water_cost_py, when_structure_built, gross_rent_pm):
        self.electric_cost_pm = electric_cost_pm
        self.fuel_cost_pm = fuel_cost_pm
        self.gas_cost_pm = gas_cost_pm
        self.insurance_cost_py = insurance_cost_py
        self.mobile_home_cost_py = mobile_home_cost_py
        self.insurance_included = insurance_included
        self.first_mortgage_cost_pm = first_mortgage_cost_pm
        self.include_tax = include_tax
        self.meals_included = meals_included
        self.rent_pm = rent_pm
        self.secondary_mortgages_pm = secondary_mortgages_pm
        self.water_cost_py = water_cost_py
        self.when_structure_built = when_structure_built
        self.gross_rent_pm = gross_rent_pm
        self.total_expenses = self.get_total_expenses()

    def get_total_expenses(self):
        # def safeAdd(total, addition):
        total = 0
        self.num_variables_needed = 10
        # self.hasNecessaryExpenseData = True
        # addition is a (str) variable, the int value of which needs to be added to the total
        # bottom_codes is the highest numeric option for the ACS variable that does not correspond to a numeric value
        def value_with_bottom_coding(addition, bottom_codes):
            if addition == '':
                self.num_variables_needed -= 1
            try:
                if int(addition) > bottom_codes:
                    return int(addition)
            except:
                pass
            return 0

        total += value_with_bottom_coding(self.electric_cost_pm, 2)
        total += value_with_bottom_coding(self.fuel_cost_pm, 2)
        total += value_with_bottom_coding(self.gas_cost_pm, 3)
        total += (value_with_bottom_coding(self.insurance_cost_py, 0) / 12)
        total += (value_with_bottom_coding(self.mobile_home_cost_py, 0) / 12)
        total += value_with_bottom_coding(self.first_mortgage_cost_pm, 0)
        if value_with_bottom_coding(self.gross_rent_pm, 0) > 0:
            total += value_with_bottom_coding(self.gross_rent_pm, 0)
        else:
            total += value_with_bottom_coding(self.rent_pm, 0)
        total += value_with_bottom_coding(self.secondary_mortgages_pm, 0)
        total += (value_with_bottom_coding(self.water_cost_py, 0) / 12)
        # print("Total = ", total)
        return total


class Demographics:
    def __init__(self, family_type_and_employment, percent_household_income_that_is_rent):
        self.family_type_and_employment = family_type_and_employment
        self.percent_household_income_that_is_rent = percent_household_income_that_is_rent


class Household:
    def __init__(self, acs_row, indices):
        self.id = acs_row[indices['id']]
        self.puma = acs_row[indices['state']] + acs_row[indices['puma']]
        self.state = acs_row[indices['state']]
        self.num_people = acs_row[indices['num_people']]
        self.property = Property(acs_row[indices['acres']], acs_row[indices['bath']], acs_row[indices['num_bedrooms']], acs_row[indices['num_units']], acs_row[indices['num_rooms']],
                                 acs_row[indices['tenure']], acs_row[indices['property_value']], acs_row[indices['when_structure_built']], acs_row[indices['num_vehicles']])
        self.income = Income(
            acs_row[indices['ag_sales']], acs_row[indices['family_income_py']], acs_row[indices['household_income_py']])
        self.expenses = Expenses(acs_row[indices['electric_cost_pm']], acs_row[indices['fuel_cost_pm']], acs_row[indices['gas_cost_pm']], acs_row[indices['insurance_cost_py']], acs_row[indices['mobile_home_cost_py']], acs_row[indices['insurance_included']], acs_row[indices['first_mortgage_cost_pm']],
                                 acs_row[indices['include_tax']], acs_row[indices['meals_included']], acs_row[indices['rent_pm']], acs_row[indices['secondary_mortgages_pm']], acs_row[indices['water_cost_py']], acs_row[indices['when_structure_built']], acs_row[indices['gross_rent_pm']])
        self.demographics = Demographics(
            acs_row[indices['family_type_and_employment']], acs_row[indices['percent_household_income_that_is_rent']])
        self.family_budget = None
        self.household_budget = None
        if self.income.family_income_py.isnumeric():
            self.family_budget = (float(self.income.family_income_py) / 12) - self.expenses.total_expenses
        if self.income.household_income_py.isnumeric():
            self.household_budget = (float(self.income.household_income_py) / 12) - self.expenses.total_expenses


        # try:
        #     self.family_budget = (float(self.income.family_income_py) / 12) - self.expenses.total_expenses
        # except:
        #     pass
        # try:
        #     print('household_income_py: ', household_income_py)
        #     self.household_budget = (float(self.income.household_income_py) / 12) - self.expenses.total_expenses
        # except:
        #     pass

    def set_year(self, year):
        self.year = year
        self.puma = self.puma + year

    def to_string(self):
        str = "Household: " + self.id
        str += "\n- PUMA: " + self.puma
        str += "\n- Number of People: " + self.num_people
        str += "\n- Property: "
        str += "\n  - Acres of land: " + self.property.acres
        str += "\n  - Bath and/or Shower Available: " + self.property.bath
        str += "\n  - Number of Bedrooms: " + self.property.num_bedrooms
        str += "\n  - Number of Units in Building: " + self.property.num_units
        str += "\n  - Number of Rooms: " + self.property.num_rooms
        str += "\n  - Tenure: " + self.property.tenure
        str += "\n  - Property Value: " + self.property.property_value
        str += "\n  - When Structure Was Built: " + self.property.when_structure_built
        str += "\n  - Number of Vehicles: " + self.property.num_vehicles
        str += "\n- Income: "
        str += "\n  - Agricultural Sales: " + self.income.ag_sales
        str += "\n  - Family Income Per Year: " + self.income.family_income_py
        str += "\n  - Household Income Per Year: " + self.income.household_income_py
        str += "\n- Expenses: "
        str += "\n  - Monthly Electric Bill: " + self.expenses.electric_cost_pm
        str += "\n  - Monthly Fuel _costs: " + self.expenses.fuel_cost_pm
        str += "\n  - Monthly Gas Bill: " + self.expenses.gas_cost_pm
        str += "\n  - Annual Insurance _costs: " + self.expenses.insurance_cost_py
        str += "\n  - Annual Mobile Home _costs: " + self.expenses.mobile_home_cost_py
        str += "\n  - Insurance _included in First _mortgage? " + \
            self.expenses.insurance_included
        str += "\n  - First _mortgage Per Month: " + self.expenses.first_mortgage_cost_pm
        str += "\n  - First _mortgage Includes Tax? " + self.expenses.include_tax
        str += "\n  - Meals _included in Rent? " + self.expenses.meals_included
        str += "\n  - Rent Per Month: " + self.expenses.rent_pm
        str += "\n  - Secondary _mortgage Payments Per Month: " + \
            self.expenses.secondary_mortgages_pm
        str += "\n  - Water Bill Per Year: " + self.expenses.water_cost_py
        str += "\n  - When Structure Built: " + self.expenses.when_structure_built
        str += "\n  - Gross Rent Per Month: " + self.expenses.gross_rent_pm
        str += "\n- Demographics: "
        str += "\n  - Family Type and Employment: " + \
            self.demographics.family_type_and_employment
        str += "\n  - Percent of Household Income Going to Rent: " + \
            self.demographics.percent_household_income_that_is_rent
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
#     Family type and employment status
#     Gross rent as a percentage of household income past 12 months

# calculateExpenses()
