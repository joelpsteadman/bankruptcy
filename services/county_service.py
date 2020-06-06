import csv

from models.County import *

def get_county_data(filepath, year):

    dictionary_of_counties = dict()

    with open(filepath) as csvfile:
        file_reader = csv.reader(csvfile)
        row = []
        while not row: # skip blank rows at the beginning
            row = next(file_reader)

        try:
            while True:
                if row[0].isspace() or row[0]: # row is empty
                    if row[0][0].isnumeric(): # line specifying which court district e.g. 1st
                        next(file_reader)
                    else:
                        state = row[0][0:2]
                        next(file_reader)

                        county_row = next(file_reader)
                        while county_row[0]:
                            code = county_row[1]
                            bankruptcies = 0
                            try:
                                bankruptcies = int(county_row[1].replace(',', ''))
                            except:
                                pass
                            if code in dictionary_of_counties:
                                dictionary_of_counties[code].bankruptcies += bankruptcies
                            else:
                                county = County(code)
                                county.year = year
                                county.state = state
                                county.name = county_row[0].replace(" ", "_")
                                county.bankruptcies = bankruptcies
                                
                                dictionary_of_counties[code] = county

                            county_row = next(file_reader)
                row = next(file_reader)
        except StopIteration:
            pass

    return dictionary_of_counties
