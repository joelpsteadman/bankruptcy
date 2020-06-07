# bankruptcy

run 'python data_analyzer.py' from this directory for the results below
run 'python data_collector.py' to gather PUMA / county etc data (incomplete)
- Data is collected to puma-output.csv
run 'python learn.py' to test a prediction based on puma-output.csv

## How-To

### Set up more years

* Always name files starting with their year

#### County Bankruptcy Data

- Data for bankruptcies by county and year can be found here: https://www.uscourts.gov/report-name/bankruptcy-filings?tn=&pt=All&t=534&m%5Bvalue%5D%5Bmonth%5D=&y%5Bvalue%5D%5Byear%5D=2018
    - Select bankruptcy from the topic drop-down menu and the year that you want
    - Look for the link for "U.S. Bankruptcy Courts - Business and Nonbusiness Cases Filed, by Chapter of the Bankruptcy Code, District, and County”
    - The PDF will give you a pretty view, but you need the csv file
    - Click on the link then download the CSV
    - Edit the CSV thus:
        - Copy the Circ/Dist and County column to column A
        - Copy the county code column into column B
        - Copy the total non business bankruptcies column to column C
        - Delete all other data
        - Unmerge all cells
        - Remove data from the top few columns (can accept any number of leading blank rows)

## findings

* Average people per household: 1.840791949603207
* Average Family Income Per Year: 35803.37950994028
* Average Household Income Per Year: 46201.31373230794

Entries with family income:  24386 / 48892
Entries with household income:  38038 / 48892
Average People Per Household:  1.840791949603207
Average Family Income Per Year:  $143565.88
Average Household Income Per Year:  $118769.37


Households below $0 budget:  2269
Entries with family income:  24386 / 48892
Entries with household income:  38038 / 48892
Average People Per Household:  1.840791949603207
Average Family Income Per Year:  $143565.88
Average Household Income Per Year:  $118769.37
Average # of variables provided:  3.32140227440072

05/31/2020 07:08:31 AM - [116] INFO: Households below $0 budget: 2679
05/31/2020 07:08:31 AM - [117] INFO: Entries with family income: 24386/48892
05/31/2020 07:08:31 AM - [118] INFO: Entries with household income: 38038/48892
05/31/2020 07:08:31 AM - [119] INFO: Average People Per Household: 1.840792
05/31/2020 07:08:31 AM - [120] INFO: Average Family Income Per Year: $143565.88
05/31/2020 07:08:31 AM - [121] INFO: Average Household Income Per Year: $118769.37
05/31/2020 07:08:31 AM - [122] INFO: Average # of variables provided: 3.163769