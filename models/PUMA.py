import statistics

class PUMA:
    
    # @param counties is a list of County objects
    def __init__(self, id):
        self.id = id
        self.has_cf = False # TODO redundant?
        self.has_person = False
        self.has_household = False
        self.people = []
        self.households = []
        self.cfs = []
    
    def get_median_age(self):
        list_of_ages = []
        for person in self.people:
            list_of_ages.append(int(person.age))
        return statistics.median(list_of_ages)
    
    def get_portion_35_to_54(self):
        num_in_age_range = 0
        for person in self.people:
            age = int(person.age)
            if age >= 35 and age <= 54:
                num_in_age_range += 1
        return num_in_age_range / len(self.people)
    
    def get_portion_40_to_44(self):
        num_in_age_range = 0
        for person in self.people:
            age = int(person.age)
            if age >= 40 and age <= 44:
                num_in_age_range += 1
        return num_in_age_range / len(self.people)

    def get_divorced_rate(self):
        num_divorced = 0
        for person in self.people:
            if person.divorced:
                num_divorced += 1
        return float(num_divorced) / len(self.people)

    def get_highschool_graduation_rate(self):
        num_graduated = 0
        for person in self.people:
            education = person.education
            if education.isnumeric() and int(education) > 15:
                num_graduated += 1
        return float(num_graduated) / len(self.people)

    def get_portion_hs_or_some_college(self):
        num = 0
        for person in self.people:
            education = person.education
            if education.isnumeric() and int(education) > 15 and int(education) < 20:
                num += 1
        return float(num) / len(self.people)

    def get_in_the_red_rate(self):
        num_in_red = 0
        num_with_vars = 0
        for household in self.households:
            try:
                if float(household.family_budget) < 0 or float(household.household_budget) <= 0:
                    num_in_red += 1
                num_with_vars += 1
            except:
                pass
        if num_with_vars == 0:
            return 'NA'
        else:
            return float(num_in_red) / num_with_vars

    def get_bankruptcy_rate(self):
        num_bankrupt = 0.0
        total_population = 0.0
        for cf in self.cfs:
            try:
                county = cf.county
                total_population += float(cf.population)
                num_bankrupt += float(county.get_bankruptcy_rate()) * float(cf.population)
            except:
                pass
        if total_population == 0.0:
            return 'NA'
        else:
            res = num_bankrupt / total_population
            if res >= 1:
                return res
            else:
                return num_bankrupt / total_population

    def get_insured_rate(self):
        num_insured = 0
        for person in self.people:
            if person.insured:
                num_insured += 1
        return float(num_insured) / len(self.people)

    def get_black_rate(self):
        num_black = 0
        for person in self.people:
            if person.black:
                num_black += 1
        return float(num_black) / len(self.people)

    def get_disabled_rate(self):
        num_disabled = 0
        for person in self.people:
            if person.disabled:
                num_disabled += 1
        return float(num_disabled) / len(self.people)

    def get_veteran_rate(self):
        num_veteran = 0
        total = 0
        for person in self.people:
            if not person.veteran == 'NA':
                total += 1
                if person.veteran:
                    num_veteran += 1
        return float(num_veteran) / total

    def get_immigrant_rate(self):
        num_immigrant = 0
        for person in self.people:
            if person.immigrant:
                num_immigrant += 1
        return float(num_immigrant) / len(self.people)

    def get_unemployed_rate(self):
        num_unemployed = 0
        for person in self.people:
            if person.unemployed:
                num_unemployed += 1
        return float(num_unemployed) / len(self.people)