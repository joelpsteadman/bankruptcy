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

logger.log("len(df) ", len(df), "; len(training_set): ", len(training_set), "; len(testing_set):", len(testing_set))
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

logger.log("R^2: ", r2)

# logger.log(mymodel(5))

# r2_score(y_true, y_pred)

# measure accuracy in average # of standard deviations from the mean




# COMPARE TO MEAN ################################################################################

testing_y = testing_y.values.tolist()

# calculate how far (in stddev's) the mean is from the truth on average
stddev = statistics.stdev(testing_y)
mean = statistics.mean(training_y)
total_error = 0.0
for y in testing_y:
    error = abs(mean - y)
    total_error += error
average_mean_error = total_error * 100000/ len(testing_y)
logger.log('Mean error:', average_mean_error)

# calculate how far (in stddev's) the prediction is from the truth on average
total_error = 0.0
i = 0
for y in testing_y:
    error = abs(predicted_bankruptcies[i] - y)
    total_error += error
    i += 1
average_mean_error = total_error * 100000 / len(testing_y)
logger.log('Prediction error:', average_mean_error)

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
logger.log('Prediction error %:', average_mean_error)

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
logger.log('mean error %:', average_mean_error)

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
logger.log('Prediction beats mean', percent_wins, '% of the time')

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
logger.log('median error:', average_median_error)

# calculate how far (in stddev's) the prediction is from the truth on average
total_error = 0.0
i = 0
for y in testing_y:
    error = abs(predicted_bankruptcies[i] - y)
    total_error += error
    i += 1
average_median_error = total_error * 100000 / len(testing_y)
logger.log('Prediction error:', average_median_error)

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
average_median_error = total_error / len(testing_y)
logger.log('Prediction error %:', average_median_error)

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
logger.log('median error %:', average_median_error)

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
logger.log('Prediction beats median', percent_wins, '% of the time')


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
logger.log('median error:', average_median_error)
regr = linear_model.LinearRegression()
regr.fit(all_X, all_y)

all_X = all_X.values.tolist()
predicted_bankruptcies = []
for puma in all_X:
    predicted_bankruptcies.append(regr.predict([[puma[0], puma[1], puma[2], puma[3], puma[4], puma[5], puma[6], puma[7], puma[8]]]))

r2 = r2_score(all_y, predicted_bankruptcies)

logger.log("R^2: ", r2)

# calculate how far (in stddev's) the prediction is from the truth on average
total_error = 0.0
i = 0
for y in all_y:
    error = abs(predicted_bankruptcies[i] - y)
    total_error += error
    i += 1
average_median_error = total_error * 100000 / len(all_y)
logger.log('Prediction error:', average_median_error)

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
logger.log('Prediction error %:', average_median_error)

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
logger.log('median error %:', average_median_error)

# guesses more accurately than the median x % of the time
total_wins = 0
i = 0
for y in all_y:
    median_error = abs(all_median - y)
    pred_error = abs(predicted_bankruptcies[i][0] - y)
    if pred_error <= median_error:
        total_wins += 1
    i += 1
percent_wins = float(total_wins) / len(all_y)
logger.log('Prediction beats median', percent_wins, '% of the time')

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
logger.log('Prediction is within 1 standard deviation', percent_wins, '% of the time')