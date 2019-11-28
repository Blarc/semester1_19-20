import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit, KFold

from sklearn.linear_model import *
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score


X0 = "X0"
X9 = "X9"
Y = "Y"

NALOGA_1 = "reg/167.csv"
NALOGA_2 = "reg/8.csv"
NALOGA_3 = "reg/26.csv"
NALOGA_4 = "reg/41.csv"
NALOGA_5 = "reg/154.csv"
NALOGA_6 = "reg/166.csv"


DATA = pd.read_csv("./data/" + NALOGA_6)
DATA.info()

NUMBER_OF_ATTRIBUTES = len(DATA.columns) - 1

# naloga 1
# C = DATA.corr()
# print(C[Y].sort_values(ascending=False))

# naloga 2 / naloga 4
# # Split to learning and test set
# L, T = train_test_split(DATA, test_size=0.2)
#
# # naloga 5
# # Split to learning and test set
# # SIZE_LEARN = 37
# # L = DATA[:SIZE_LEARN]
# # T = DATA[SIZE_LEARN:]
# #
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
# # Train the model using training sets
# regr.fit(learning_x, learning_y)
#
# # Make predictions for testing set
# testing_pred = regr.predict(testing_x)
#
# # The coefficients
# print('Coefficients: \n', regr.coef_)
# # The mean squared error
# print("Mean squared error: %.6f" % mean_squared_error(testing_y, testing_pred))
# # Explained variance score: 1 is perfect prediction
# print('Variance score: %.6f' % r2_score(testing_y, testing_pred))

# naloga 6
# # Split to learning and test set
# K = 10
# SIZE_LEARN = 23
# # L = DATA[:SIZE_LEARN]
# # T = DATA[SIZE_LEARN:]
#
# # learning_x = L.iloc[:, 0:NUMBER_OF_ATTRIBUTES]
# # learning_y = L.iloc[:, NUMBER_OF_ATTRIBUTES:]
#
# model = KNeighborsRegressor(n_neighbors=3)
# scores = []
#
# DATA.sample(frac=1)
# L = DATA[:SIZE_LEARN]
# T = DATA[SIZE_LEARN:]
#
# # Split learning set to attributes and classes
# learning_x = L.iloc[:, 0:NUMBER_OF_ATTRIBUTES]
# learning_y = L.iloc[:, NUMBER_OF_ATTRIBUTES:]
#
#
#
# for test_set in T:
#     # Split testing set to attributes and classes
#     testing_x = test_set.iloc[:, 0:NUMBER_OF_ATTRIBUTES]
#     testing_y = test_set.iloc[:, NUMBER_OF_ATTRIBUTES:]
#
#
#
# # model.fit(learning_x, learning_y)
# # score = model.score(testing_x, testing_y)

# naloga 8




print("End of program")