import csv
import numbers

from models.Person import *
from enum import Enum

def get_acs_person_data(filepath, year):

    dictionary_of_people = dict()

    with open(filepath) as csvfile:
        file_reader = csv.reader(csvfile)
        line = next(file_reader)

        class Column(Enum):
            SERIALNO = line.index('SERIALNO')
            ST = line.index('ST')
            PUMA = line.index('PUMA')
            AGEP = line.index('AGEP')
            SCHL = line.index('SCHL')
            MAR = line.index('MAR')
            HICOV = line.index('HICOV')

        try:
            while True:
                acs_row = next(file_reader)

                serial_number = acs_row[Column.SERIALNO.value]
                person = Person(serial_number)
                state = acs_row[Column.ST.value]
                person.state = state # TODO make an enum of state names and use it here
                person.puma = state + acs_row[Column.PUMA.value] 
                person.age = acs_row[Column.AGEP.value]
                person.education = acs_row[Column.SCHL.value]
                if acs_row[Column.MAR.value] == '3':
                    person.divorced = True
                else:
                    person.divorced = False
                if acs_row[Column.HICOV.value] == '1':
                    person.insured = True
                else:
                    person.insured = False
                id = serial_number + state + year
                dictionary_of_people[id] = person
        except StopIteration:
            pass

    return dictionary_of_people