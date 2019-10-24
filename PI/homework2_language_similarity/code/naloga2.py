import math
import os
import platform
import random
import sys
from collections import defaultdict
from itertools import combinations

from unidecode import unidecode


def read_files(index_path, dir_path):
    index_dict = defaultdict(str)
    with open(index_path, encoding="utf8") as index:
        for line in index:
            split_line = line.split()
            index_dict[split_line[0]] = split_line[1]

    data_dict = defaultdict(lambda: defaultdict(int))

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
            data_dict[key][data[i:i + 3]] += 1

    return data_dict


class MedoidClustering:
    def __init__(self, data, k):
        self.k = k

        self.data = data

        self.point_distances = {frozenset((c1, c2)): self.point_distance(c1, c2) for c1, c2 in
                                combinations(self.data.keys(), 2)}
        self.clusters = [[r] for r in self.data.keys()]

    def point_distance(self, r1, r2):
        dict_r1 = self.data[r1]
        dict_r2 = self.data[r2]

        product_r1_r2 = 0
        for key in dict_r1:
            if key in dict_r2:
                product_r1_r2 += (dict_r1[key] * dict_r2[key])

        return 1 - (product_r1_r2 / (self.point_len(r1) * self.point_len(r2)))

    def point_len(self, r1):
        dict_r1 = self.data[r1]

        sum_r1 = 0
        for val in dict_r1.values():
            sum_r1 += (val * val)

        return math.sqrt(sum_r1)

    def get_random_leaders(self):
        leaders = defaultdict(list)
        keys_list = list(self.data.keys())
        while len(leaders) != self.k:
            leader = random.choice(keys_list)
            keys_list.remove(leader)
            leaders[leader] = [leader]

        return leaders

    def make_clusters(self, leaders):
        for c in self.data.keys():
            if c not in leaders:
                min_dist = sys.maxsize
                min_leader = None
                for leader in leaders:
                    dist = self.point_distances[frozenset((leader, c))]
                    if dist < min_dist:
                        min_dist = dist
                        min_leader = leader

                leaders[min_leader].append(c)

    def get_best_leader(self, cluster):
        _, leader = min([(self.sum_all_distances(a, cluster), a) for a in cluster])
        return leader

    def sum_all_distances(self, a, cluster):
        sum_a = 0
        for b in cluster:
            if a != b:
                sum_a += self.point_distances[frozenset((a, b))]
        return sum_a

    def run(self):
        leaders = self.get_random_leaders()

        run = True
        while run:
            run = False
            self.make_clusters(leaders)

            new_leaders = defaultdict(list)
            for leader, cluster in leaders.items():
                best_leader = self.get_best_leader(cluster)
                if best_leader != leader:
                    run = True
                new_leaders[best_leader] = [best_leader]

            leaders = {leader: [leader] for leader in new_leaders}
        self.make_clusters(leaders)

        return leaders


if __name__ == "__main__":
    DIR = "test"
    DIR_PATH = "D:\Jakob\\3letnik\semester1\git\PI\homework2_language_similarity\data\\" + DIR
    INDEX_PATH = "D:\Jakob\\3letnik\semester1\git\PI\homework2_language_similarity\data\INDEX.txt"
    if platform.system() == "Linux":
        DIR_PATH = "/home/jakob/Documents/semester1_19-20/PI/homework2_language_similarity/data/" + DIR
        INDEX_PATH = None
    readData = read_files(INDEX_PATH, DIR_PATH)
    mc = MedoidClustering(readData, 5)
    result = mc.run()
    print("done")
