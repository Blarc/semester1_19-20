import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit, KFold, cross_val_score

from sklearn.linear_model import *
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score


X0 = "X0"
X9 = "X9"
Y = "Y"

NALOGA_1 = "reg/167.csv"
NALOGA_2 = "reg/8.csv"
NALOGA_3 = "reg/25.csv"
NALOGA_4 = "reg/41.csv"
NALOGA_5 = "reg/154.csv"
NALOGA_6 = "reg/166.csv"
NALOGA_7 = "reg/116.csv"

naloga = NALOGA_7


DATA = pd.read_csv("./data/" + naloga)
DATA.info()

NUMBER_OF_ATTRIBUTES = len(DATA.columns) - 1

# naloga 1
# C = DATA.corr()
# print(C[Y].sort_values(ascending=False))

# naloga 2 / naloga 3
# # Split to learning and test set
# # L, T = train_test_split(DATA, test_size=0.2)
# #
# # print("Learning set size: {:d}\nTest set size: {:d}\n".format(len(L), len(T)))
#
# # Split learning set to attributes and classes
# # learning_x = L.iloc[:, 0:NUMBER_OF_ATTRIBUTES]
# # learning_y = L.iloc[:, NUMBER_OF_ATTRIBUTES:]
#
# # Split testing set to attributes and classes
# # testing_x = T.iloc[:, 0:NUMBER_OF_ATTRIBUTES]
# # testing_y = T.iloc[:, NUMBER_OF_ATTRIBUTES:]
#
# # Split testing set to attributes and classes
# data_x = DATA.iloc[:, 0:NUMBER_OF_ATTRIBUTES]
# data_y = DATA.iloc[:, NUMBER_OF_ATTRIBUTES:]
#
# regr = LinearRegression()
# # Train the model using training sets
# regr.fit(data_x, data_y)
#
# # Make predictions for testing set
# # testing_pred = regr.predict(data_x)
#
# # The coefficients
# print('Coefficients: \n', regr.coef_)
# # The mean squared error
# # print("Mean squared error: %.6f" % mean_squared_error(testing_y, testing_pred))
# # # Explained variance score: 1 is perfect prediction
# # print('Variance score: %.6f' % r2_score(testing_y, testing_pred))

# naloga 4 / naloga 5
# Split to learning and test set
# SIZE_LEARN = 37
# if naloga == NALOGA_4:
#     SIZE_LEARN = 32
#
# L = DATA[:SIZE_LEARN]
# T = DATA[SIZE_LEARN:]
#
# print("Learning set size: {:d}\nTest set size: {:d}\n".format(len(L), len(T)))
#
# # Split learning set to attributes and classes
# learning_x = L.iloc[:, 0:NUMBER_OF_ATTRIBUTES]
# learning_y = L.iloc[:, NUMBER_OF_ATTRIBUTES:]
#
# # Split testing set to attributes and classes
# testing_x = T.iloc[:, 0:NUMBER_OF_ATTRIBUTES]
# testing_y = T.iloc[:, NUMBER_OF_ATTRIBUTES:]
#
# regr = LinearRegression()
# # Train the model using learning sets
# regr.fit(learning_x, learning_y)
#
# # Make predictions for learning set
# learning_pred = regr.predict(learning_x)
#
# # Make predictions for testing set
# testing_pred = regr.predict(testing_x)
#
# # The coefficients
# print('Coefficients: \n', regr.coef_)
# # The mean squared error on learning
# print("Mean squared error (learn): %.6f" % mean_squared_error(learning_y, learning_pred))
# # The mean squared error on testing
# print("Mean squared error (test): %.6f" % mean_squared_error(testing_y, testing_pred))


# naloga 6
# Split to learning and test set
K = 10
SIZE_LEARN = 52
L = DATA[:SIZE_LEARN]
T = DATA[SIZE_LEARN:]

learning_x = L.iloc[:, 0:NUMBER_OF_ATTRIBUTES]
learning_y = L.iloc[:, NUMBER_OF_ATTRIBUTES:]

test_x = T.iloc[:, 0:NUMBER_OF_ATTRIBUTES]
test_y = T.iloc[:, NUMBER_OF_ATTRIBUTES:]

res = []
for i in range(1, 20):
    knn = KNeighborsRegressor(n_neighbors=i)
    knn = knn.fit(learning_x, learning_y)
    scores = cross_val_score(knn, test_x, test_y, scoring="neg_mean_squared_error", cv=K)
    # rmse_scores = np.sqrt(-scores)
    print(i)
    scores = [abs(x) for x in scores]
    print(np.mean(scores))
    res.append((np.mean(scores), i))


print(min(res))


print("End of program")