import os
import platform
from collections import defaultdict


def read_files(dir_path):
    data = defaultdict(lambda: defaultdict(int))

    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        with open(file_path) as f:
            while True:
                c = f.read(3)
                if not c:
                    break
                print(c)


class MedoidClustering:
    def __init__(self, data):
        self.data = data
        self.clusters = None

    def row_distance(self, r1, r2):
        pass

    def cluster_distance(self, c1, c2):
        pass

    def closest_clusters(self):
        pass

    def run(self):
        pass


if __name__ == "__main__":
    DIR = "one"
    DIR_PATH = None
    if platform.system() == "Linux":
        DIR_PATH = "/home/jakob/Documents/semester1_19-20/PI/homework2_language_similarity/data/" + DIR
    readData = read_files(DIR_PATH)
