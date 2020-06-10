import csv
import numbers

from models.CountyFragment import *
from enum import Enum

def get_cf_data(filepath, year):

    dictionary_of_cfs = dict()

    with open(filepath) as csvfile:
        file_reader = csv.reader(csvfile)
        line = next(file_reader)

        class Column(Enum):
            PUMA = line.index('puma12')
            COUNTY_CODE = line.index('county')
            STATE_CODE = line.index('state')
            STATE = line.index('stab')
            COUNTY_NAME = line.index('cntyname')
            POPULATION = line.index('pop10')
            WEIGHT = line.index('afact')

        next(file_reader) # skip extra header line

        try:
            while True:
                row = next(file_reader)

                puma = row[Column.STATE_CODE.value] + row[Column.PUMA.value] + year
                county_code = row[Column.COUNTY_CODE.value] + year
                name = puma + '_' + county_code
                cf = CountyFragment(name)
                cf.puma = puma
                cf.county_code = county_code
                cf.state = row[Column.STATE.value]
                cf.county_name = row[Column.COUNTY_NAME.value]
                cf.population = row[Column.POPULATION.value]
                cf.weight = row[Column.WEIGHT.value]
                dictionary_of_cfs[name] = cf
        except StopIteration:
            pass

    return dictionary_of_cfs