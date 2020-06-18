# Bankruptcy Analysis at the Community Level

*Analysis written in Python 3, R used for visualization*

## Results

Taking into account (in order of predictive power) race(1), divorce(2), age(3), immigrant status(4), health insurance(5), education(6), disability status(7), employment status(8), and veteran status(9) with 2013 - 2018 census, ACS, and bankruptcy data, my model is **able to predict bankrupcty rate of a PUMA to within one standard deviation 79% of the time.** This is true when trained and tested on the entire 6 years of data and when the model is trained on an arbitrary 80% of the data and tested on the remaining 20%.

1) Percent of a PUMA's population that were black
2) Percent of a PUMA'S population that were divorced at the time (rather than single, widowed, etc)
3) Percent of a PUMA's population that were between the ages of 35 and 54
4) Percent of a PUMA's population that were not born in the US
5) Percent of a PUMA's population that had health insurance
6) Percent of a PUMA's population that had just a high school degree of some college
7) Percent of a PUMA's population that were disabled
8) Percent of a PUMA's population that were unemployed
9) Percent of a PUMA's population that were veterans

### Results Output:
Size of data set: 14,103; Size of training data set: 11,282; Testing data set: 2,821

R^2: 0.13744617491860567

Model predicts better than the mean 58% of the time

Model predicts better than the median 51% of the time

Model predicts within 1 standard deviation 79% of the time

### Data Table

|             | Black | Divorce | Age  | Immigrant | Insurance | Education | Disabled | Unemployed | Veteran | Bankruptcy  / 100,000 |
|-------------|-------|---------|------|-----------|-----------|-----------|----------|------------|---------|-----------------------|
| Min         | 0%    | 3%      | 5%   | 0%        | 45%       | 12%       | 5%       | 37%        | 0%      | 0                     |
| Median      | 7%    | 12%     | 16%  | 7%        | 92%       | 43%       | 19%      | 65%        | 7%      | 223                   |
| Average     | 13%   | 12%     | 17%  | 11%       | 90%       | 42%       | 19%      | 65%        | 7%      | 260                   |
| Max         | 97%   | 23%     | 34%  | 76%       | 100%      | 64%       | 43%      | 86%        | 50%     |                 1,425 |
| R2          | 0.10  | 0.03    | 0.02 | 0.02      | 0.01      | 0.01      | 0.01     | 0.00       | 0.00    |                       |
| Correlation | 0.31  | 0.17    | 0.15 | -0.13     | -0.12     | 0.10      | 0.09     | -0.05      | 0.04    |                       |

---

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