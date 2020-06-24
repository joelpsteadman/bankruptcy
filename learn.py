import numpy, pandas
import statistics, csv, os
from sklearn.metrics import r2_score
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from Utilities import Logger

# set up personal logger
logger = Logger()
current_path = os.getcwd()
logger.define_issue_log(os.path.join(current_path, 'files/issues.log'))

logger.log('(b = bankruptcy or bankruptcies)')

def partition(data_set, training_set_portion): 
    data_set.shuffle()
    size_of_training_set = round(len(data_set) / float(1 - training_set_portion))
    training_set = data_set[:size_of_training_set]
    test_set = data_set[size_of_training_set:]
    return {'train': training_set, 'test': test_set}

# def learn(training_inputs, training_outputs, test_inputs, test_outputs):
df = pandas.read_csv("./files/puma-output.csv")
all_X = df[['Divorce', 'Age', 'Education', 'Insurance', 'Black', 'Disabled', 'Veteran', 'Immigrant', 'Unemployed']]
all_y = df['Bankruptcy']

training_set, testing_set = train_test_split(df, test_size=0.2, shuffle=True)
training_X = training_set[['Divorce', 'Age', 'Education', 'Insurance', 'Black', 'Disabled', 'Veteran', 'Immigrant', 'Unemployed']]
training_y = training_set['Bankruptcy']
testing_X = testing_set[['Divorce', 'Age', 'Education', 'Insurance', 'Black', 'Disabled', 'Veteran', 'Immigrant', 'Unemployed']]
testing_y = testing_set['Bankruptcy']

logger.log("Total # of PUMA-year entries:\t\t\t\t", format(len(df), ',d'))
logger.log('# of entries in training set:\t\t\t\t', format(len(training_set), ',d'))
logger.log("# of entries in testing set\t\t\t\t", format(len(testing_set), ',d'))
# logger.log("Training inputs: ", train_inputs['train'], "Testing inputs ", test_inputs['test'])
regr = linear_model.LinearRegression()
regr.fit(training_X, training_y)

testing_X = testing_X.values.tolist()
predicted_bankruptcies = []
for puma in testing_X:
    predicted_bankruptcies.append(regr.predict([[puma[0], puma[1], puma[2], puma[3], puma[4], puma[5], puma[6], puma[7], puma[8]]]))

# logger.log(predicted_bankruptcies)

# x = numpy.random.normal(3, 1, 100)
# y = numpy.random.normal(150, 40, 100) / x

# train_x = x[:80]
# train_y = y[:80]

# test_x = x[80:]
# test_y = y[80:]

# mymodel = numpy.poly1d(numpy.polyfit(train_x, train_y, 2))

# r2 = r2_score(test_y, mymodel(test_x))
r2 = r2_score(testing_y, predicted_bankruptcies)

logger.log("R^2 of the model from the training set when applied to the testing set:", r2)

# logger.log(mymodel(5))

# r2_score(y_true, y_pred)

# measure accuracy in average # of standard deviations from the mean




# COMPARE TO MEAN ################################################################################

testing_y = testing_y.values.tolist()

# calculate how far (in stddev's) the mean is from the truth on average
stddev = statistics.stdev(testing_y)
mean = statistics.mean(training_y)
median = statistics.median(testing_y)
total_error = 0.0
for y in testing_y:
    error = abs(mean - y)
    total_error += error
average_mean_error = total_error * 100000/ len(testing_y)
logger.log('b in a PUMA per 100,000 people in the test set is', round(average_mean_error), 'from the average of the training set')

# calculate how far (in stddev's) the prediction is from the truth on average
total_error = 0.0
i = 0
for y in testing_y:
    error = abs(predicted_bankruptcies[i] - y)
    total_error += error
    i += 1
average_mean_error = total_error * 100000 / len(testing_y)
logger.log('b in a PUMA per 100,000 people in the test set is', round(average_mean_error[0]), 'from the prediction based on the training model')

columns = ['Prediction', 'Actual', 'Mean']
# name of output file  
filename = "./files/learn-output.csv"
# writing to csv file  
with open(filename, 'w') as csvfile:  
    # creating a csv writer object  
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(columns)
    i = 0
    for y in testing_y:
        row = [predicted_bankruptcies[i][0] * 100000, testing_y[i] * 100000, mean * 100000]
        csvwriter.writerow(row)
        i += 1

# what % off am I on average?
total_error = 0.0
i = 0
for y in testing_y:
    prediction = predicted_bankruptcies[i][0]
    if prediction < y:
        if not y: # y is 0.0
            error = 1 - (prediction / 0.0001)
        else:
            error = 1 - (prediction / y)
        total_error += error
    else:
        error = 1 - (y / prediction)
        total_error += error
    i += 1
average_mean_error = total_error / len(testing_y)
logger.log('Predicted bankruptcy rate based on the training set is', round(average_mean_error*100), '% off, on average, from the real value for each PUMA in the test set')

total_error = 0.0
i = 0
for y in testing_y:
    if mean < y:
        if not y: # y is 0.0
            error = 1 - (mean / 0.0001)
        else:
            error = 1 - (mean / y)
        total_error += error
    else:
        error = 1 - (y / mean)
        total_error += error
    i += 1
average_mean_error = total_error / len(testing_y)
logger.log('Average bankruptcy rate of the training set is', round(average_mean_error*100), '% off, on average, when used to predict that of each PUMA in the test set')

# guesses more accurately than the mean x % of the time
total_wins = 0
i = 0
for y in testing_y:
    mean_error = abs(mean - y)
    pred_error = abs(predicted_bankruptcies[i][0] - y)
    if pred_error < mean_error:
        total_wins += 1
    i += 1
percent_wins = float(total_wins) / len(testing_y)
logger.log('Prediction beats mean', round(percent_wins, 1) * 100, '% of the time in this test set')

# test how accurately it predicts the remaining data as a whole
real_total = 0
median_total = 0
mean_total = 0
predicted_total = 0
i = 0
for y in testing_y:
    real_total += y
    median_total += median
    mean_total += mean
    predicted_total += predicted_bankruptcies[i][0]
    mean_error = abs(mean - y)
    pred_error = abs(predicted_bankruptcies[i][0] - y)
    i += 1
# percent_wins = float(total_wins) / len(testing_y)
logger.log('Real test set b-rate:\t\t\t\t\t', round((real_total/i)*100, 3), '%')
logger.log('Median test set b-rate:\t\t\t\t\t', round((median_total/i)*100, 3), '%')
logger.log('Mean test set b-rate:\t\t\t\t\t', round((mean_total/i)*100, 3), '%')
logger.log('Predicted test set b-rate:\t\t\t\t\t', round((predicted_total/i)*100, 3), '%')
number_of_people_off = (real_total - predicted_total) * 100000
logger.log('Real # of b in this test set:\t\t\t\t', format(int(round(real_total * 100000)), ',d'))
logger.log('Real b - predicted b in this test set:\t\t\t', format(int(round(number_of_people_off)), ',d'))

# COMPARE TO MEDIAN ################################################################################

median = statistics.median(testing_y)

# calculate how far (in stddev's) the median is from the truth on average
stddev = statistics.stdev(testing_y)
median = statistics.median(testing_y)
total_error = 0.0
for y in testing_y:
    error = abs(median - y)
    total_error += error
average_median_error = total_error * 100000/ len(testing_y)
logger.log('b in a PUMA per 100,000 people in the test set is', round(average_median_error), 'from the average of the training set on average')

# # calculate how far (in stddev's) the prediction is from the truth on average
# total_error = 0.0
# i = 0
# for y in testing_y:
#     error = abs(predicted_bankruptcies[i] - y)
#     total_error += error
#     i += 1
# average_median_error = total_error * 100000 / len(testing_y)
# logger.log('Prediction error:', average_median_error[0])

columns = ['Prediction', 'Actual', 'median']
# name of output file  
filename = "./files/learn-output.csv"
# writing to csv file  
with open(filename, 'w') as csvfile:  
    # creating a csv writer object  
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(columns)
    i = 0
    for y in testing_y:
        row = [predicted_bankruptcies[i][0] * 100000, testing_y[i] * 100000, median * 100000]
        csvwriter.writerow(row)
        i += 1

# # what % off am I on average?
# total_error = 0.0
# i = 0
# for y in testing_y:
#     prediction = predicted_bankruptcies[i][0]
#     if prediction < y:
#         if not y: # y is 0.0
#             error = 1 - (prediction / 0.0001)
#         else:
#             error = 1 - (prediction / y)
#         total_error += error
#     else:
#         error = 1 - (y / prediction)
#         total_error += error
#     i += 1
# average_median_error = total_error / len(testing_y)
# logger.log('Prediction error %:', average_median_error)

total_error = 0.0
i = 0
for y in testing_y:
    if median < y:
        if not y: # y is 0.0
            error = 1 - (median / 0.0001)
        else:
            error = 1 - (median / y)
        total_error += error
    else:
        error = 1 - (y / median)
        total_error += error
    i += 1
average_median_error = total_error / len(testing_y)
logger.log('Median b-rate of the training set is', round(average_median_error*100), '% off, on average, when used to predict that of each PUMA in the test set')

# guesses more accurately than the median x % of the time
total_wins = 0
i = 0
for y in testing_y:
    median_error = abs(median - y)
    pred_error = abs(predicted_bankruptcies[i][0] - y)
    if pred_error <= median_error:
        total_wins += 1
    i += 1
percent_wins = float(total_wins) / len(testing_y)
logger.log('Prediction beats median', round(percent_wins*100, 1), '% of the time in this test set')


# COMPARE TO ALL ################################################################################

all_y = all_y.values.tolist()

# calculate how far (in stddev's) the median is from the truth on average
stddev = statistics.stdev(all_y)
all_median = statistics.median(all_y)
total_error = 0.0
for y in all_y:
    error = abs(all_median - y)
    total_error += error
average_median_error = total_error * 100000/ len(all_y)
logger.log('b in a PUMA per 100,000 people for all entries is', round(average_median_error), 'from the average of the training set on average')
regr = linear_model.LinearRegression()
regr.fit(all_X, all_y)

all_X = all_X.values.tolist()
# for entry in all_X:
#     entry[3] = 1
predicted_bankruptcies = []
for puma in all_X:
    predicted_bankruptcies.append(regr.predict([[puma[0], puma[1], puma[2], puma[3], puma[4], puma[5], puma[6], puma[7], puma[8]]]))

r2 = r2_score(all_y, predicted_bankruptcies)

logger.log("R^2 for the entire dataset:\t\t\t\t", r2)

# calculate how far (in stddev's) the prediction is from the truth on average
total_error = 0.0
i = 0
for y in all_y:
    error = abs(predicted_bankruptcies[i] - y)
    total_error += error
    i += 1
average_median_error = total_error * 100000 / len(all_y)
logger.log('b in a PUMA per 100,000 people in the test set is',  round(average_median_error[0]), 'from the prediction when trained on the entire dataset on average')

columns = ['Prediction', 'Actual']
# name of output file  
filename = "./files/learn-output.csv"
# writing to csv file  
with open(filename, 'w') as csvfile:  
    # creating a csv writer object  
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(columns)
    i = 0
    for y in all_y:
        row = [predicted_bankruptcies[i][0] * 100000, all_y[i] * 100000]
        csvwriter.writerow(row)
        i += 1

# what % off am I on average?
total_error = 0.0
i = 0
for y in all_y:
    prediction = predicted_bankruptcies[i][0]
    if prediction < y:
        if not y: # y is 0.0
            error = 1 - (prediction / 0.0001)
        else:
            error = 1 - (prediction / y)
        total_error += error
    else:
        error = 1 - (y / prediction)
        total_error += error
    i += 1
average_median_error = total_error / len(all_y)
logger.log('Predicted b-rate based on the entire data set is', round(average_median_error*100), '% off, on average, from the real value for each PUMA')

total_error = 0.0
i = 0
for y in all_y:
    if all_median < y:
        if not y: # y is 0.0
            error = 1 - (all_median / 0.0001)
        else:
            error = 1 - (all_median / y)
        total_error += error
    else:
        error = 1 - (y / all_median)
        total_error += error
    i += 1
average_median_error = total_error / len(all_y)
logger.log('Median b-rate of the entire dataset is', round(average_median_error*100), '% off, on average, when used to predict that of each PUMA')

# guesses more accurately than the median x % of the time
total_wins = 0
median_wins = 0
i = 0
for y in all_y:
    median_error = abs(all_median - y)
    pred_error = abs(predicted_bankruptcies[i][0] - y)
    if pred_error <= median_error:
        total_wins += 1
    if median_error <= stddev:
        median_wins += 1
    i += 1
percent_wins = float(total_wins) / len(all_y)
percent_med_wins = float(median_wins) / len(all_y)
logger.log('Prediction beats median', round(percent_wins*100, 1), '% of the time when trained and tested on the entire dataset')
logger.log('Median is within 1 standard deviation', round(percent_med_wins*100, 1), '% of the time in the entire dataset')

# guesses within 1 stddev % of the time
total_wins = 0
i = 0
for y in all_y:
    # median_error = abs(all_median - y)
    pred_error = abs(predicted_bankruptcies[i][0] - y)
    if pred_error <= stddev:
        total_wins += 1
    i += 1
percent_wins = float(total_wins) / len(all_y)
logger.log('Prediction is within 1 standard deviation', round(percent_wins*100, 1), '% of the time when trained and tested on the entire dataset ')

# test how accurately it predicts the data as a whole
real_total = 0
median_total = 0
mean_total = 0
predicted_total = 0
i = 0
for y in all_y:
    real_total += y
    median_total += median
    mean_total += mean
    predicted_total += predicted_bankruptcies[i][0]
    mean_error = abs(mean - y)
    pred_error = abs(predicted_bankruptcies[i][0] - y)
    i += 1
# percent_wins = float(total_wins) / len(testing_y)
logger.log('Real b-rate:\t\t\t\t\t\t', round((real_total/i)*100, 3), '%')
logger.log('Median b-rate:\t\t\t\t\t\t', round((median_total/i)*100, 3), '%')
logger.log('Mean b-rate:\t\t\t\t\t\t', round((mean_total/i)*100, 3), '%')
logger.log('Predicted b-rate:\t\t\t\t\t\t', round((predicted_total/i)*100, 3), '%')
US_POPULATION = 310000000
number_of_people_off = ((real_total - predicted_total)/i) * US_POPULATION
logger.log('Real # of b per year in entire dataset per year:\t\t', format(int(round((real_total/i) * US_POPULATION)), ',d'))
logger.log('Real b - predicted b per year in the entire dataset:\t', format(int(round(number_of_people_off)), ',d'))

# WHAT IF EVERYONE WAS INSURED?

for entry in all_X:
    entry[3] = 1
predicted_bankruptcies = []
for puma in all_X:
    predicted_bankruptcies.append(regr.predict([[puma[0], puma[1], puma[2], puma[3], puma[4], puma[5], puma[6], puma[7], puma[8]]]))
predicted_total = 0
i = 0
for y in all_y:
    predicted_total += predicted_bankruptcies[i][0]
    i += 1
number_of_people_off = ((real_total - predicted_total)/i) * US_POPULATION
logger.log('Predicted b-rate if all Americans had health insurance:\t', round((predicted_total/i)*100, 3), '%')
logger.log('Predicted b per year if all Americans had health insurance:', format(int(round((predicted_total/i) * US_POPULATION)), ',d'), '(', format(int(round(number_of_people_off)), ',d'), 'less )')
