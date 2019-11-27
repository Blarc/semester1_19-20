import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

data = pd.read_csv("./data/reg/167.csv")

data.head()

X9 = "X9"
Y = "Y"

# bins = np.linspace(0, max(data[X9]), 50)
#
# mhv = np.digitize(data[X9], bins)
#
# L, T = train_test_split(data, test_size=0.2, random_state=42, stratify=mhv)

C = data.corr()
print(C[Y].sort_values(ascending=False))

print("Hello World!")