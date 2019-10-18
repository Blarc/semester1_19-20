import math
import platform
from itertools import combinations

NORM_FACTOR = 100
OUT = open("out.txt", "w")

def read_file(file_name):

    data = {}
    columns = {}
    columns_counter = 0

    with open(file_name) as f:
        header = f.readline()

        for line in f:
            row = line.strip().split(",")
            year, type_of_voting, country, to_country, points = int(row[0]), row[1], row[2], row[3], int(row[4])
            col = (to_country, year)
            if col not in columns:
                columns[col] = columns_counter
                columns_counter += 1

    with open(file_name) as f:
        header = f.readline()

        for line in f:
            row = line.strip().split(",")
            year, type_of_voting, country, to_country, points = int(row[0]), row[1], row[2], row[3], int(row[4])
            col = (to_country, year)
            if country not in data:
                data[country] = [None] * columns_counter
            index = columns[col]
            if data[country][index] is None:
                data[country][index] = 0
            data[country][index] += points

    return data


def flatten_list(a):
    if type(a) is list:
        return [x for i in a for x in flatten_list(i)]
    return [a]
class HierarchicalClustering:

    def __init__(self, data):
        self.data = data
        self.clusters = [[country] for country in self.data.keys()]
        self.row_distances = {frozenset((c1, c2)): self.row_distance(c1, c2) for c1, c2 in
                              combinations(self.data.keys(), 2)}

    def row_distance(self, r1, r2):

        row1 = self.data[r1]
        row2 = self.data[r2]

        sum_of_attributes = 0
        attributes_counter = 0
        for i in range(0, len(row1)):
            val1 = row1[i]
            val2 = row2[i]
            if val1 is not None and val2 is not None:
                sum_of_attributes += pow(val1 - val2, 2)
                attributes_counter += 1

        if attributes_counter == 0:
            return -1
        return math.sqrt((sum_of_attributes / attributes_counter) * len(row1))

    def cluster_distance(self, c1, c2):

        c1 = flatten_list(c1)
        c2 = flatten_list(c2)

        sum_distances = 0
        counter = 0
        for x in c1:
            for y in c2:
                dist = self.row_distances[frozenset((x, y))]
                if dist != -1:
                    sum_distances += dist
                    counter += 1

        if counter == 0:
            return -1
        return sum_distances / counter

    def closest_clusters(self):

        min_dist = 999
        min_pair = (-1, -1)
        for c1, c2 in combinations(self.clusters, 2):
            dis, pair = self.cluster_distance(c1, c2), (c1, c2)
            if -1 < dis < min_dist:
                min_dist = dis
                min_pair = pair

        return min_dist, min_pair

    def run(self):

        while len(self.clusters) > 2:
            dis, pair = self.closest_clusters()
            one, two = pair
            self.clusters.append([one, two])
            self.clusters.remove(one)
            self.clusters.remove(two)

        # self.dendrogram = {x: 0 for x in flatten_list(self.clusters)}

    def plot_tree_rec(self, c, depth):
        if len(c) == 1:
            for i in range(0, depth):
                print("    ", end="", file=OUT)
            print("----" + c[0], file=OUT)
        else:
            self.plot_tree_rec(c[0], depth + 1)
            for i in range(0, depth):
                print("    ", end="", file=OUT)
            print("----|", file=OUT)
            self.plot_tree_rec(c[1], depth + 1)

    def plot_tree(self):
        # self.clusters = [self.clusters[1], self.clusters[0]]
        self.plot_tree_rec(self.clusters, 0)



if __name__ == "__main__":
    DATA_FILE = "D:\Jakob\\3letnik\semester1\git\PI\homework1_Eurovision\data\eurovision-finals-1975-2019.csv"
    if platform.system() == "Linux":
        DATA_FILE = "/home/jakob/Documents/semester1_19-20/PI/homework1_Eurovision/data/eurovision-finals-1975-2019.csv"
    normalised_data = read_file(DATA_FILE)
    hc = HierarchicalClustering(normalised_data)
    hc.run()
    hc.plot_tree()
    print(hc.clusters)
    OUT.close()
