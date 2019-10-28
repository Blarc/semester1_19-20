import math
import os
import platform
import random
from collections import defaultdict
from itertools import combinations

from unidecode import unidecode


class Point:
    def __init__(self, lang: str):
        self.lang = lang
        self.freqs = defaultdict(int)
        self.cluster = None

    def add_string(self, string: str):
        self.freqs[string] += 1

    def __repr__(self):
        return self.lang

    def point_length(self):
        return math.sqrt(sum([freq * freq for freq in self.freqs.values()]))

    def similarity_with_point(self, point):
        scalar_product = 0
        for string in self.freqs:
            if string in point.freqs:
                scalar_product += (self.freqs[string] * point.freqs[string])

        return scalar_product / (self.point_length() * point.point_length())

    def get_leader(self):
        return self.cluster.leader

    def is_leader(self):
        return self.cluster != None and self.get_leader() == self


class Cluster:
    def __init__(self, leader: Point):
        self.leader = leader
        self.points = [leader]
        leader.cluster = self

    def add_point(self, point: Point):
        self.points.append(point)

    def size(self):
        return len(self.points)

    def reset(self, new_leader: Point):
        self.leader = new_leader
        self.points = [new_leader]
        new_leader.cluster = self

    def __repr__(self):
        return self.leader.__str__()


class MedoidClustering:
    def __init__(self, read_data: dict, k):
        self.k = k
        self.points = list(read_data.values())
        self.points_similarity = {frozenset((p1, p2)): p1.similarity_with_point(p2)
                                  for p1, p2 in combinations(self.points, 2)}
        self.clusters = [Cluster(x) for x in random.sample(self.points, k)]

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

    def similarity_with_cluster(self, a: Point, cluster: Cluster, correction: bool):
        similarity = 0
        for point in cluster.points:
            if point is not a:
                similarity += self.points_similarity[frozenset((a, point))]
        if similarity == 0:
            return 0
        if correction:
            return similarity / (cluster.size() - 1)
        return similarity / cluster.size()

    def similarity_with_best_neighbour(self, a: Point):
        best_similarity = -9999
        for cluster in self.clusters:
            if cluster.leader != a.get_leader():
                similarity = self.similarity_with_cluster(a, cluster, False)
                if similarity > best_similarity:
                    best_similarity = similarity

        return best_similarity

    def find_best_leader(self, cluster: Cluster):
        best_similarity = -9999
        best_point = None
        for point in cluster.points:
            similarity = self.similarity_with_cluster(point, cluster, True)
            if similarity > best_similarity:
                best_similarity = similarity
                best_point = point

        return best_point

    def run(self):
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

    def silhouette(self, a: Point, cluster: Cluster):
        if cluster.size() > 1:
            similarity_cluster = self.similarity_with_cluster(a, cluster, True)
            similarity_all = self.similarity_with_best_neighbour(a)


def read_files(index_path, dir_path):
    index_dict = defaultdict(str)
    with open(index_path, encoding="utf8") as index:
        for line in index:
            split_line = line.split()
            index_dict[split_line[0]] = split_line[1]

    data_dict = defaultdict(Point)

    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)

        data = open(file_path, "rt", encoding="utf8").read()
        data = unidecode(data)
        data = data.replace(".", " ")
        data = data.replace(",", " ")
        data = data.replace("!", " ")
        data = data.replace("?", " ")
        data = data.replace(";", " ")
        data = data.replace("'", " ")
        data = data.replace("\n", " ")
        data = data.replace("  ", " ")
        data = data.lower()

        file_name = file_name.replace(".txt", "")
        for i in range(0, len(data) - 2):
            key = index_dict[file_name]
            if key not in data_dict:
                data_dict[key] = Point(key)
            data_dict[key].add_string(data[i:i + 3])

    return data_dict


if __name__ == "__main__":
    DIR = "test"
    DIR_PATH = "D:\Jakob\\3letnik\semester1\git\PI\homework2_language_similarity\data\\" + DIR
    INDEX_PATH = "D:\Jakob\\3letnik\semester1\git\PI\homework2_language_similarity\data\INDEX.txt"
    if platform.system() == "Linux":
        DIR_PATH = "/home/jakob/Documents/semester1_19-20/PI/homework2_language_similarity/data/" + DIR
        INDEX_PATH = "/home/jakob/Documents/semester1_19-20/PI/homework2_language_similarity/data/INDEX.txt"
    readData = read_files(INDEX_PATH, DIR_PATH)
    mc = MedoidClustering(readData, 5)
    mc.run()
    print("done")
