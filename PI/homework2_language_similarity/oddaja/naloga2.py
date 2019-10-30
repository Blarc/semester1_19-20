import copy
import math
import os
import platform
import random
from collections import defaultdict
from itertools import combinations

import numpy as np
from matplotlib import pyplot as plt
from unidecode import unidecode


class Point:
    def __init__(self, lang: str):
        self.lang = lang
        self.freqs = defaultdict(int)
        self.cluster = None
        self.silhouette_val = 0
        self.silhouette_val_sum = 0

    def add_string(self, string: str):
        self.freqs[string] += 1

    def __repr__(self):
        return self.lang

    def point_length(self) -> float:
        return math.sqrt(sum([freq * freq for freq in self.freqs.values()]))

    def similarity_with_point(self, point) -> float:
        scalar_product = 0
        for string in self.freqs:
            if string in point.freqs:
                scalar_product += (self.freqs[string] * point.freqs[string])

        return scalar_product / (self.point_length() * point.point_length())

    def get_leader(self) -> str:
        return self.cluster.leader

    def is_leader(self) -> bool:
        return self.cluster is not None and self.get_leader() == self

    def reset(self):
        self.cluster = None
        self.silhouette_val = 0


class Cluster:
    def __init__(self, leader: Point):
        self.leader = leader
        self.points = [leader]
        leader.cluster = self

    def add_point(self, point: Point):
        point.cluster = self
        self.points.append(point)

    def size(self) -> int:
        return len(self.points)

    def reset(self, new_leader: Point):
        self.leader = new_leader
        self.points = [new_leader]
        new_leader.cluster = self

    def __repr__(self):
        return self.leader.__str__()


class MedoidClustering:
    def __init__(self, data: dict, k):
        self.k = k
        self.points = list(data.values())
        self.points_similarity = {frozenset((p1, p2)): p1.similarity_with_point(p2)
                                  for p1, p2 in combinations(self.points, 2)}
        self.clusters = None
        self.best_silhouette_sum = -100
        self.best_silhouette_clusters = None
        self.worst_silhouette_sum = 100
        self.worst_silhouette_clusters = None

    def expand_clusters(self):
        for point in self.points:
            if not point.is_leader():
                best_similarity = -9999
                best_cluster = None
                for cluster in self.clusters:
                    similarity = self.points_similarity[frozenset((point, cluster.leader))]
                    if similarity > best_similarity:
                        best_similarity = similarity
                        best_cluster = cluster

                best_cluster.add_point(point)

    def similarity_with_best_neighbour(self, a: Point) -> float:
        best_similarity = -9999
        for cluster in self.clusters:
            if cluster.leader != a.get_leader():
                similarity = self.similarity_with_cluster(a, cluster, False)
                if similarity > best_similarity:
                    best_similarity = similarity

        return best_similarity

    def similarity_with_cluster(self, a: Point, cluster: Cluster, correction: bool) -> float:
        similarity = 0
        for point in cluster.points:
            if point is not a:
                similarity += self.points_similarity[frozenset((a, point))]
        if similarity == 0:
            return 0
        if correction:
            return similarity / (cluster.size() - 1)
        return similarity / cluster.size()

    def find_best_leader(self, cluster: Cluster) -> Point:
        best_similarity = -9999
        best_point = None
        for point in cluster.points:
            similarity = self.similarity_with_cluster(point, cluster, True)
            if similarity > best_similarity:
                best_similarity = similarity
                best_point = point

        return best_point

    def reset_points(self):
        for point in self.points:
            point.reset()

    def run(self):
        self.reset_points()
        self.clusters = [Cluster(x) for x in random.sample(self.points, self.k)]
        run = True
        while run:
            run = False
            self.expand_clusters()

            for cluster in self.clusters:
                best_leader = self.find_best_leader(cluster)
                if best_leader != cluster.leader:
                    run = True
                cluster.reset(best_leader)

        self.expand_clusters()
        self.silhouette()

    def calc_silhouette(self, a: Point):
        if a.cluster.size() > 1:
            similarity_cluster = self.similarity_with_cluster(a, a.cluster, True)
            similarity_all = self.similarity_with_best_neighbour(a)

            silhouette_val = (similarity_cluster - similarity_all) / max(similarity_all, similarity_cluster)
            a.silhouette_val = silhouette_val
            a.silhouette_val_sum += silhouette_val

    def silhouette(self):
        suma = 0
        for point in self.points:
            self.calc_silhouette(point)
            suma += point.silhouette_val

        if suma > self.best_silhouette_sum:
            self.best_silhouette_sum = suma
            self.best_silhouette_clusters = copy.deepcopy(self.clusters)

        elif suma < self.worst_silhouette_sum:
            self.worst_silhouette_sum = suma
            self.worst_silhouette_clusters = copy.deepcopy(self.clusters)

    def draw_histogram(self):

        sorted_points = sorted(self.points, key=lambda x: x.silhouette_val_sum)
        num_of_points = len(sorted_points)

        cmap = plt.get_cmap(name="rainbow", lut=num_of_points)
        colors = [cmap(x) for x in range(0, num_of_points)]

        values = [x.silhouette_val_sum for x in sorted_points]
        languages = [x.lang for x in sorted_points]

        plt.barh(languages, values, color=colors)

    @staticmethod
    def draw_silhouette(silhouette: list):
        for cluster in silhouette:
            cluster.points.sort(key=lambda x: x.silhouette_val)

        silhouette.sort(key=lambda x: x.points[-1].silhouette_val)
        num_of_points = len(silhouette)

        cmap = plt.get_cmap(name="rainbow", lut=num_of_points)

        values = []
        languages = []
        colors = []

        index = 0
        for cluster in silhouette:
            for point in cluster.points:
                values.append(point.silhouette_val)
                languages.append(point.lang)
                colors.append(cmap(index))

            index += 1

        plt.xticks(np.arange(min(values) - 0.2, max(values) + 0.2, 0.1), rotation="vertical")
        plt.barh(languages, values, color=colors)

    def draw_worst_silhouette(self):
        self.draw_silhouette(self.worst_silhouette_clusters)

    def draw_best_silhouette(self):
        self.draw_silhouette(self.best_silhouette_clusters)

    def draw(self):
        plt.figure()
        self.draw_best_silhouette()
        plt.show()
        plt.figure()
        self.draw_worst_silhouette()
        plt.show()
        plt.figure()
        self.draw_histogram()
        plt.show()

    def compare_file(self, file_path: str, name="unknown") -> None:
        point = read_file(file_path, name)
        comparisons = sorted([(point.similarity_with_point(p), p.lang) for p in self.points], reverse=True)
        print(name)
        for comparison in comparisons[0:3]:
            print(comparison[1], comparison[0] / sum(x for x, _ in comparisons) * 100)
        print()

    def compare_files(self, dir_path):
        for file_name in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file_name)
            self.compare_file(file_path, file_name)


def read_files(index_path, dir_path) -> dict:
    index_dict = defaultdict(str)
    with open(index_path, encoding="utf8") as index:
        for line in index:
            split_line = line.split()
            index_dict[split_line[0]] = split_line[1]

    data_dict = defaultdict(Point)

    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)

        data = open_file(file_path)

        file_name = file_name.replace(".txt", "")
        for i in range(0, len(data) - 2):
            key = index_dict[file_name]
            if key not in data_dict:
                data_dict[key] = Point(key)
            data_dict[key].add_string(data[i:i + 3])

    return data_dict


def open_file(file_path):
    data = open(file_path, "rt", encoding="utf8").read()
    data = unidecode(data)
    data = data.replace(".", " ")
    data = data.replace(",", " ")
    data = data.replace("!", " ")
    data = data.replace("?", " ")
    data = data.replace(";", " ")
    data = data.replace("'", " ")
    data = data.replace("\"", " ")
    data = data.replace("\n", " ")
    data = data.replace("  ", " ")
    data = data.lower()

    return data


def read_file(file_path, name="Name not specified") -> Point:
    data = open_file(file_path)
    point = Point(name)
    for i in range(0, len(data) - 2):
        point.add_string(data[i:i + 3])

    return point


if __name__ == "__main__":
    K = 5
    REPETITIONS = 100
    DIR = "test"
    DIR_PATH = "D:\Jakob\\3letnik\semester1\git\PI\homework2_language_similarity\data\\" + DIR
    INDEX_PATH = "D:\Jakob\\3letnik\semester1\git\PI\homework2_language_similarity\data\INDEX.txt"
    COMPARE_PATH = "D:\Jakob\\3letnik\semester1\git\PI\homework2_language_similarity\data\compare\slo1"
    if platform.system() == "Linux":
        DIR_PATH = "/home/jakob/Documents/semester1_19-20/PI/homework2_language_similarity/data/" + DIR
        INDEX_PATH = "/home/jakob/Documents/semester1_19-20/PI/homework2_language_similarity/data/INDEX.txt"
        COMPARE_PATH = "/home/jakob/Documents/semester1_19-20/PI/homework2_language_similarity/data/compare/"

    read_data = read_files(INDEX_PATH, DIR_PATH)
    mc = MedoidClustering(read_data, K)

    for j in range(0, REPETITIONS):
        mc.run()
    mc.draw()
    mc.compare_files(COMPARE_PATH)
