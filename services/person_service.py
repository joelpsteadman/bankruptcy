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
            RACBLK = line.index('RACBLK') # 0 = not black; 1 = black
            DIS = line.index('DIS') # 1 = disabled; 2 = not disabled
            MIL = line.index('MIL') # 1-3 = veteran
            WAOB = line.index('WAOB') # 1-2 = non-immigrant
            NWAB = line.index('NWAB') # 1 = temp work absence; 2 = no

        try:
            while True:
                acs_row = next(file_reader)

                serial_number = acs_row[Column.SERIALNO.value]
                person = Person(serial_number)
                state = acs_row[Column.ST.value]
                person.state = state # TODO make an enum of state names and use it here
                person.puma = state + acs_row[Column.PUMA.value] + year
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
                if acs_row[Column.RACBLK.value] == '1':
                    person.black = True
                else:
                    person.black = False
                if acs_row[Column.DIS.value] == '1':
                    person.disabled = True
                else:
                    person.disabled = False
                mil = acs_row[Column.MIL.value]
                if mil == '1' or mil == '2' or mil == '3':
                    person.veteran = True
                else:
                    person.veteran = False
                if acs_row[Column.WAOB.value] == '1' or acs_row[Column.WAOB.value] == '2':
                    person.immigrant = False
                else:
                    person.immigrant = True
                nwab = acs_row[Column.NWAB.value]
                if nwab == '1':
                    person.unemployed = True
                elif nwab == '2' or nwab == 'b':
                    person.unemployed = False
                else:
                    person.unemployed = 'NA'
                id = serial_number + state + year
                dictionary_of_people[id] = person
        except StopIteration:
            pass

    return dictionary_of_people
    

def get_responses(filepath, year):

    numbers = list()

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
            RACBLK = line.index('RACBLK') # 0 = not black; 1 = black
            DIS = line.index('DIS') # 1 = disabled; 2 = not disabled
            MIL = line.index('MIL') # 1-3 = veteran
            WAOB = line.index('WAOB') # 1-2 = non-immigrant
            NWAB = line.index('NWAB') # 1 = temp work absence; 2 = no

        total = 0
        divorced = 0
        insured = 0
        black = 0
        disabled = 0
        veteran = 0
        immigrant = 0
        unemployed = 0
        try:
            while True:
                acs_row = next(file_reader)

                total += 1
                # education += 1
                if acs_row[Column.MAR.value]: # has a value
                    divorced += 1
                if acs_row[Column.HICOV.value]: # has a value
                    insured += 1
                if acs_row[Column.RACBLK.value]: # has a value
                    black += 1
                if acs_row[Column.DIS.value]: # has a value
                    disabled += 1
                if acs_row[Column.MIL.value]: # has a value
                    veteran += 1
                if acs_row[Column.WAOB.value]: # has a value
                    immigrant += 1
                if acs_row[Column.NWAB.value] and not acs_row[Column.NWAB.value] == '3': # has a value, and was reported
                    unemployed += 1
        except StopIteration:
            pass

    numbers = [float(divorced) / total, float(insured) / total, float(black) / total, float(disabled) / total, float(veteran) / total, float(immigrant) / total, float(unemployed) / total]
    return numbers