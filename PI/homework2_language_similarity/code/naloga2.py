import math
import os
import platform
import random
from collections import defaultdict
from itertools import combinations

from unidecode import unidecode


def read_files(dir_path):
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
            data_dict[file_name][data[i:i + 3]] += 1

    return data_dict


class MedoidClustering:
    def __init__(self, data):
        self.data = data

        self.point_distances = {frozenset((c1, c2)): self.point_distance(c1, c2) for c1, c2 in
                                combinations(self.data.keys(), 2)}
        self.clusters = None

    def point_distance(self, r1, r2):
        dict_r1 = self.data[r1]
        dict_r2 = self.data[r2]

        product_r1_r2 = 0
        for key in dict_r1:
            if key in dict_r2:
                product_r1_r2 += (dict_r1[key] * dict_r2[key])

        return product_r1_r2 / (self.point_len(r1) * self.point_len(r2))

    def point_len(self, r1):
        dict_r1 = self.data[r1]

        sum_r1 = 0
        for val in dict_r1.values():
            sum_r1 += (val * val)

        return math.sqrt(sum_r1)

    def cluster_distance(self, c1, c2):
        pass

    def closest_clusters(self):
        pass

    def get_random_leaders(self, k):
        leaders = []
        keys_list = list(self.data.keys())
        while len(leaders) != k:
            leader = random.choice(keys_list)
            keys_list.remove(leader)
            leaders.append(leader)

        return leaders

    def run(self, k):
        pass

if __name__ == "__main__":
    DIR = "test"
    DIR_PATH = "D:\Jakob\\3letnik\semester1\git\PI\homework2_language_similarity\data\\test"
    if platform.system() == "Linux":
        DIR_PATH = "/home/jakob/Documents/semester1_19-20/PI/homework2_language_similarity/data/" + DIR
    readData = read_files(DIR_PATH)
    mc = MedoidClustering(readData)
    mc.run(5)
    print("done")
