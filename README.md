# Bankruptcy Analysis at the Community Level

*Written in Python 3*

## How-To:

### Set Up Data:
* ACS person data:
    * Create a folder called 'Person_ACS' in the files/ folder
    * Get single year ACS Person Files from this [census website](https://www.census.gov/programs-surveys/acs/data/pums.html).
    * Rename those files to start with the year they are from (e.g. 2018_pus-a.csv)
    * Place ACS person files in the Person_ACS folder
    * (2012 and on uses the same census data for population)
* Bankruptcy by County:
    * Create a folder called 'County_Bankruptcies' in the files/ folder
    * Get bankruptcy data by county from this [US Courts site](https://www.uscourts.gov/report-name/bankruptcy-filings?tn=&pt=All&t=534&m%5Bvalue%5D%5Bmonth%5D=&y%5Bvalue%5D%5Byear%5D=2018) for each year that you want
        * Select bankruptcy from the topic drop-down menu and the year that you want
        * Look for the link for "U.S. Bankruptcy Courts - Business and Nonbusiness Cases Filed, by Chapter of the Bankruptcy Code, District, and County”
        * The PDF will give you a pretty view, but you need the csv file
        * Click on the link then download the CSV (sometimes the this needs done a couple times before a non corrupted version is downloaded?)
        * Edit the CSV in the following way:
            * Copy the Circ/Dist and County column to column A
            * Copy the county code column into column B
            * Copy the total non business bankruptcies column to column C
            * Delete all other data
            * Remove data from the top few columns (can accept any number of leading blank rows)
    * Rename those files to start with the year they are from (e.g. 2018_county_bankruptcies.csv)
    * Place county bankruptcy files in the County_Bankruptcies folder
    * (2013 and has the county code included which is necessary for this program to work)
* **Important Note:** You need to have the same years represented for person ACS data, and US Courts data
* Run `python __main__.py` or `python ../bankruptcy` from /bankruptcy to gather PUMA / county etc data (for all years that you provide in the files section)
    * Data is collected to puma-output.csv
    * Takes 10+ minutes to run depending on computer hardware

### Run Analysis
* Run `python learn.py` to test a prediction based on [puma-output.csv](./files/puma-output.csv)
    * Requires the open source packages pandas, numpy, and sklearn which can be installed using pip
    * To check whether you have pip installed run `pip --version` and to install it run `sudo easy_install pip`
    * To install these packages run `pip install numpy`, `pip install pandas`, and `pip install sklearn`

---

## Results

Taking into account (in order of predictive power) divorce(1), age(2), health insurance(3), and education(4), with 2013 - 2018 census, ACS, and bankruptcy data, my model is able to predict bankrupcty rate of a PUMA on average to within 111 people on average per 100,000 (vs 115 when predicting with the mean), is 33% off from the true value on average (vs 34%), and out predicts the mean 55.5% of the time (R^2: 0.043)

1) Percent of a PUMA'S population that is currently divorced (rather than single, widowed, etc)
    - min: 3%
    - max: 23%
    - Higher divorce rate is correlated with higher bankruptcy (R^2 - .030)
2) Percent of a PUMA's population that is between the ages of 35 and 54
    - min: 5%
    - max: 34%
    - This rate is correlated with higher bankruptcy (R^2 - .023)
3) Percent of a PUMA's population that has health insurance
    - min: 45%
    - max: 99%
    - This rate is inversely related with higher bankruptcy (R^2 - .015)
4) Percent of a PUMA's population that has just a high school degree of some college
    - min: 12%
    - max: 64%
    - This rate is correlated with higher bankruptcy (R^2 - .010)

### June 10, 2020 Results:
len(df)  14103 ; len(training_set):  11282 ; len(testing_set): 2821
R^2:  0.04275453607429536
Mean error:  114.61877787853518
Prediction error:  [111.24480827]
Prediction error %:  0.32739957667083
mean error %:  0.33532343964654443
Prediction beats mean  0.5558312655086849 % of the time
median error:  110.07931018951957
Prediction error:  [111.24480827]
Prediction error %:  0.32739957667083
median error %:  0.32493936932453793
Prediction beats median  0.4551577454803261 % of the time

### June 15, 2020 Results:
len(df)  14103 ; len(training_set):  7051 ; len(testing_set): 7052
R^2:  0.12527309888662286
Mean error:  115.92694050268592
Prediction error:  [106.86243725]
Prediction error %:  0.31723699506498926
mean error %:  0.33934226686556174
Prediction beats mean  0.5792682926829268 % of the time
median error:  111.27164557279681
Prediction error:  [106.86243725]
Prediction error %:  0.31723699506498926
median error %:  0.32876928961909524
Prediction beats median  0.5107770845150312 % of the time

---

## Misc. Findings

(this section is old and needs updated)

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
