import math
import platform
from collections import defaultdict
from itertools import combinations

import matplotlib.pyplot as plt
import numpy as np

NORM_FACTOR = 100


def read_file(file_name):
    """
    Read and process data to be used for clustering.
    :param file_name: name of the file containing the data
    :return: dictionary with element names as keys and feature vectors as values
    """
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


class Case:
    def __init__(self, name):
        self.name = name
        self.televoting = defaultdict(int)
        self.jury = defaultdict(int)
        self.total = defaultdict(int)

    def add_voting(self, type_of_voting, to_country, points):
        if self.name == to_country:
            return
        elif type_of_voting == "J":
            self.jury[to_country] += points
        else:
            self.televoting[to_country] += points
        self.total[to_country] += points

    def normalise(self):
        sum_televoting = sum(self.televoting.values()) / NORM_FACTOR
        self.televoting = {k: v / sum_televoting for k, v in self.televoting.items()}
        sum_jury = sum(self.jury.values()) / NORM_FACTOR
        self.jury = {k: v / sum_jury for k, v in self.jury.items()}
        sum_total = sum(self.total.values()) / NORM_FACTOR
        self.total = {k: v / sum_total for k, v in self.total.items()}

    def draw_country(self, color, type_of_voting="default"):
        if type_of_voting == "J":
            countries = self.jury.keys()
            points = self.jury.values()
        elif type_of_voting == "T":
            countries = self.televoting.keys()
            points = self.televoting.values()
        else:
            countries = self.total.keys()
            points = self.total.values()

        plt.scatter(countries, points, s=80, color=color, label=self.name)

    def draw_country_by_attribute(self, color, attribute):
        plt.scatter(self.name, self.total[attribute], s=80, color=color, label=self.name)
        plt.annotate(self.name, (self.name, self.total[attribute]))


class Cluster:
    def __init__(self, case):
        self.cases = [case]
        self.centeroid = case

    def add_cluster(self, cluster):
        self.cases.extend(cluster.cases)
        self.centeroid = [sum(x) / self.cases.__len__() for x in zip(*self.cases)]


class HierarchicalClustering:
    def __init__(self, data):
        self.dendrogram = {}
        self.data = data
        self.clusters = [[country] for country in self.data.keys()]

    @staticmethod
    def calc_row_distance(row1, row2):

        sum_of_attributes = 0
        attributes_counter = 0
        for i in range(0, len(row1)):
            val1 = row1[i]
            val2 = row2[i]
            if val1 is not None and val2 is not None:
                sum_of_attributes += pow(val1 - val2, 2)
                attributes_counter += 1

        # TODO normaliziraj
        if attributes_counter == 0:
            return 100
        return math.sqrt(sum_of_attributes / attributes_counter)

    def row_distance(self, r1, r2):
        """
        Distance between two rows.
        Implement either Euclidean or Manhattan distance.
        Example call: self.row_distance("Polona", "Rajko")
        """
        row1 = self.data[r1]
        row2 = self.data[r2]
        return self.calc_row_distance(row1, row2)

    def cluster_distance(self, c1, c2):
        """
        Compute distance between two clusters.
        Implement either single, complete, or average linkage.
        Example call: self.cluster_distance(
            [[["Albert"], ["Branka"]], ["Cene"]],
            [["Nika"], ["Polona"]])
        """

        c1 = flatten_list(c1)
        c2 = flatten_list(c2)

        sum_distances = 0
        for x in c1:
            for y in c2:
                sum_distances += self.row_distance(x, y)
        return sum_distances / (c1.__len__() * c2.__len__())

    def centroid_of(self, a):
        if type(a[0][0]) is not list and type(a[1][0]) is not list:
            return [sum(x) / 2 for x in zip(self.data[a[0][0]], self.data[a[1][0]])]
        if type(a[0][0]) is not list:
            return [sum(x) / 2 for x in zip(self.data[a[0][0]], self.centroid_of(a[1]))]
        return [sum(x) / 2 for x in zip(self.centroid_of(a[0]), self.centroid_of(a[1]))]

    def closest_clusters(self):
        """
        Find a pair of closest clusters and returns the pair of clusters and
        their distance.

        Example call: self.closest_clusters(self.clusters)
        """
        dis, pair = min((self.cluster_distance(c1, c2), (c1, c2))
                        for c1, c2 in combinations(self.clusters, 2))
        return dis, pair

    def run(self):
        """
        Given the data in self.data, performs hierarchical clustering.
        Can use a while loop, iteratively modify self.clusters and store
        information on which clusters were merged and what was the distance.
        Store this later information into a suitable structure to be used
        for plotting of the hierarchical clustering.
        """
        while self.clusters.__len__() > 2:
            dis, pair = self.closest_clusters()
            one, two = pair
            self.clusters.append([one, two])
            self.clusters.remove(one)
            self.clusters.remove(two)

        self.dendrogram = {x: 0 for x in flatten_list(self.clusters)}

    def plot_tree(self):
        """
        Use cluster information to plot an ASCII representation of the cluster
        tree.
        """
        self.plot_tree_rec(self.clusters)
        plt.bar(range(len(self.dendrogram)), list(self.dendrogram.values()), align="center")
        plt.xticks(range(len(self.dendrogram)), list(self.dendrogram.keys()))
        plt.xticks(rotation=90)
        plt.show()

    def draw_clusters(self, c1, c2):
        dist = self.cluster_distance(c1, c2)
        if len(c1) == 1:
            self.dendrogram[c1[0]] = dist
        if len(c2) == 1:
            self.dendrogram[c2[0]] = dist

    def plot_tree_rec(self, a):
        if type(a[0][0]) is not list and type(a[1][0]) is not list:
            self.draw_clusters(a[0], a[1])
        elif type(a[0][0]) is not list:
            self.draw_clusters(a[0], self.plot_tree_rec(a[1]))
        elif type(a[0][1]) is not list:
            self.draw_clusters(self.plot_tree_rec(a[0]), a[1])
        else:
            self.draw_clusters(self.plot_tree_rec(a[0]), self.plot_tree_rec(a[1]))
        return a


def flatten_list(a):
    if type(a) is list:
        return [x for i in a for x in flatten_list(i)]
    return [a]


def draw_data(data):
    plt.figure(figsize=(16, 12))

    colors = plt.cm.get_cmap("gist_rainbow")(np.linspace(0, 1, data.values().__len__()))

    attribute = "Germany"
    for color, country in zip(colors, data.values()):
        # country.draw_country(color)
        if country.name != attribute:
            country.draw_country_by_attribute(color, attribute)

    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
    plt.title(attribute)
    plt.ylabel("Points")
    plt.yticks(np.arange(0, 20, 0.5))
    plt.xlabel("Countries")
    plt.xticks(rotation=90)
    plt.show()


if __name__ == "__main__":
    DATA_FILE = "D:/Jakob/3letnik/semester1/PI/homework1_Eurovision/data/eurovision-finals-1975-2019.csv"
    if platform.system() == "Linux":
        DATA_FILE = "/home/jakob/Documents/semester1_19-20/PI/homework1_Eurovision/data/eurovision-finals-1975-2019.csv"
    normalised_data = read_file(DATA_FILE)
    hc = HierarchicalClustering(normalised_data)
    hc.run()
    hc.plot_tree()
    print(hc.clusters)
