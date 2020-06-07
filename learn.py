import numpy
import pandas
from sklearn.metrics import r2_score
from sklearn import linear_model

# def learn(training_inputs, training_outputs, test_inputs, test_outputs):
df = pandas.read_csv("./files/puma-output.csv")

X = df[['Divorce', 'Age', 'Education', 'Insurance']]
y = df['Bankruptcy']

regr = linear_model.LinearRegression()
regr.fit(X, y)

predicted_bankruptcy = regr.predict([[0.23, 0.3, 0.62, 0.47]])

print(predicted_bankruptcy)

# x = numpy.random.normal(3, 1, 100)
# y = numpy.random.normal(150, 40, 100) / x

# train_x = x[:80]
# train_y = y[:80]

# test_x = x[80:]
# test_y = y[80:]

# mymodel = numpy.poly1d(numpy.polyfit(train_x, train_y, 2))

# r2 = r2_score(test_y, mymodel(test_x))

# print(r2)

# print(mymodel(5))
