import numpy as np
import pandas as pd
import scipy.cluster.hierarchy as sch
from matplotlib import pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans

NALOGA_8 = "clu/12.csv"
NALOGA_9 = "clu/169.csv"
NALOGA_10 = "clu/150.csv"

naloga = NALOGA_10

DATA = pd.read_csv("./data/" + naloga)
DATA.info()

NUMBER_OF_ATTRIBUTES = len(DATA.columns)

# naloga 8

# cluster = AgglomerativeClustering(n_clusters=2, affinity='manhattan', linkage='single')
# cluster.fit_predict(DATA)
# print(cluster.labels_)
#
# ones = np.count_nonzero(cluster.labels_)
# zeros = len(cluster.labels_) - ones
#
# print("ones:  %d" % ones)
# print("zeros: %d" % zeros)

# naloga 9

# C1 = [4, 57]
# C2 = [59, 79]

# C1 = [3, 69]
# C2 = [50, 23]
#
# K = 100
#
# kmeans = KMeans(n_clusters=2, random_state=0, max_iter=K, init=np.array([C1, C2]), n_init=1)
# kmeans.fit(DATA)
#
# print(kmeans.labels_)
# print(kmeans.cluster_centers_)
#
# ones = np.count_nonzero(kmeans.labels_)
# zeros = len(kmeans.labels_) - ones
# #
# print("ones:  %d" % ones)
# print("zeros: %d" % zeros)

# naloga 10

C1 = [87, -16]
C2 = [-48, -80]

K = 100

kmeans = KMeans(n_clusters=2, random_state=0, max_iter=K, init=np.array([C1, C2]), n_init=1)
kmeans.fit(DATA)

print(kmeans.cluster_centers_)




print("End of program")