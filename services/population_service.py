import csv, os
from enum import Enum

from Utilities import Logger

class Population_Calculator:
    def __init__(self, filepath):
        counties = dict()

        with open(filepath) as csvfile:
            file_reader = csv.reader(csvfile)
            line = next(file_reader)

            class Column(Enum):
                COUNTY_CODE = line.index('COUNTY')
                STATE_CODE = line.index('STATE')
                Y10 = line.index('POPESTIMATE2010')
                Y11 = line.index('POPESTIMATE2011')
                Y12 = line.index('POPESTIMATE2012')
                Y13 = line.index('POPESTIMATE2013')
                Y14 = line.index('POPESTIMATE2014')
                Y15 = line.index('POPESTIMATE2015')
                Y16 = line.index('POPESTIMATE2016')
                Y17 = line.index('POPESTIMATE2017')
                Y18 = line.index('POPESTIMATE2018')

            try:
                while True:
                    row = next(file_reader)
                    county = dict()
                    code = row[Column.STATE_CODE.value] + row[Column.COUNTY_CODE.value]
                    county['2010'] = row[Column.Y10.value]
                    county['2011'] = row[Column.Y11.value]
                    county['2012'] = row[Column.Y12.value]
                    county['2013'] = row[Column.Y13.value]
                    county['2014'] = row[Column.Y14.value]
                    county['2015'] = row[Column.Y15.value]
                    county['2016'] = row[Column.Y16.value]
                    county['2017'] = row[Column.Y17.value]
                    county['2018'] = row[Column.Y18.value]
                    counties[code] = county
            except StopIteration:
                pass
        self.counties = counties

    def get_population(self, code, year, given_population):
        code_without_year = code[0:5]
        try:
            pop_this_year = float(self.counties[code_without_year][year])
            pop_2010 = float(self.counties[code_without_year]['2010'])
            ratio = (pop_this_year / pop_2010)
            return float(given_population) * ratio
        except (KeyError):
            # set up personal logger
            logger = Logger()
            current_path = os.getcwd()
            logger.define_issue_log(os.path.join(current_path, 'files/issues.log'))
            logger.record_issue('No population data for county:', code)
            return given_population