import csv
from enum import Enum

from models.PUMA import *

def get_puma_data(filepath, year):

    dictionary_of_pumas = dict()

    with open(filepath) as csvfile:
        file_reader = csv.reader(csvfile)
        line = next(file_reader)

        class Column(Enum):
            PUMA = line.index('puma12')
            STATE_CODE = line.index('state')
            STATE = line.index('stab')

        next(file_reader) # skip extra header line

        try:
            while True:
                row = next(file_reader)
                id = row[Column.STATE_CODE.value] + row[Column.PUMA.value]
                puma = PUMA(id)
                puma.state = row[Column.STATE.value]
                puma.year = year
                dictionary_of_pumas[id] = puma
        except StopIteration:
            pass

    return dictionary_of_pumas