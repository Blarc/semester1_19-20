from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np

NORM_FACTOR = 100


def read_file(file_name):
    """
    Read and process data to be used for clustering.
    :param file_name: name of the file containing the data
    :return: dictionary with element names as keys and feature vectors as values
    """
    with open(file_name) as f:
        header = f.readline().strip().split("\t")[1:]
        data = {}
        for line in f:
            row = line.strip().split(",")
            type_of_voting, country, to_country, points = row[1], row[2], row[3], int(row[4])
            if country not in data:
                data[country] = Country(country)
            data[country].add_voting(type_of_voting, to_country, points)

    for country in data.values():
        country.normalise()

    return data


class Country:
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

    def add_cluster(self, cluster):
        self.cases.extend(cluster.cases)

    def centeroid_by_attribute(self, attribute):
        result = 0
        for case in self.cases:
            result += case.total[attribute]

        return result / self.cases.__len__()


class HierarchicalClustering:
    def __init__(self, data):
        self.data = data
        self.clusters = [Cluster(country) for country in self.data.values()]

    def merge_clusters(self, c1, c2):
        c1.add_cluster(c2)
        self.clusters.remove(c2)

    def row_distance(self, r1, r2):
        """
        Distance between two rows.
        Implement either Euclidean or Manhattan distance.
        Example call: self.row_distance("Polona", "Rajko")
        """
        pass

    @staticmethod
    def cluster_distance_by_attribute(c1, c2, attribute):
        c1_points = c1.centroid_by_attribute(attribute)
        c2_points = c2.centroid_by_attribute(attribute)
        return abs(c1_points - c2_points)

    def cluster_distance(self, c1, c2):
        """
        Compute distance between two clusters.
        Implement either single, complete, or average linkage.
        Example call: self.cluster_distance(
            [[["Albert"], ["Branka"]], ["Cene"]],
            [["Nika"], ["Polona"]])
        """
        pass

    def closest_clusters_by_attribute(self, attribute):
        min_dist = float("inf")
        min_cluster_1, min_cluster_2 = None, None
        for cluster_1 in self.clusters:
            if cluster_2 != attribute:
                for country2 in self.data[country1].total:
                    if country2 != attribute:
                        dist = self.row_distance_by_attribute(country1, country2, attribute)
                        if dist < min_dist:
                            min_dist = dist
                            min_country1, min_country2 = country1, country2

        return min_country1, min_country2

    def run(self):
        """
        Given the data in self.data, performs hierarchical clustering.
        Can use a while loop, iteratively modify self.clusters and store
        information on which clusters were merged and what was the distance.
        Store this later information into a suitable structure to be used
        for plotting of the hierarchical clustering.
        """
        pass

    def plot_tree(self):
        """
        Use cluster information to plot an ASCII representation of the cluster
        tree.
        """
        pass


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
    normalised_data = read_file(DATA_FILE)
    hc = HierarchicalClustering(normalised_data)
    # hc.merge_clusters(hc.clusters[0], hc.clusters[1])
    print(hc.closest_clusters_by_attribute("Germany"))
    draw_data(normalised_data)
