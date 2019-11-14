import operator
import os
import platform
from collections import defaultdict

import numpy as np
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

        data = open_file(file_path)

        file_name = file_name.replace(".txt", "")
        for i in range(0, len(data) - 2):
            key = index_dict[file_name]
            data_dict[key][data[i:i + 3]] += 1

    col_dict = defaultdict(float)
    for lang in data_dict:
        for triplet in data_dict[lang]:
            col_dict[triplet] += 1

    num_of_langs = len(data_dict)
    for triplet in col_dict:
        col_dict[triplet] = np.math.log(num_of_langs / col_dict[triplet], 10)

    col_sorted = sorted(list(col_dict.items()), key=operator.itemgetter(1))
    col_enumerated = enumerate(col_sorted[0:100])
    col_dict = {x[1][0]: x[0] for x in col_enumerated}
    return data_dict, col_dict


def prepare_data_matrix(data, columns):
    """
    Return data in a matrix (2D numpy array), where each row contains triplets
    for a language. Columns should be the 100 most common triplets
    according to the idf measure.
    """
    # create matrix X and list of languages
    # ...

    h = len(data)
    matrix = np.zeros(shape=(h, 100))
    languages = []
    index = 0
    for lang in data:
        # matrix[index] = np.array([data[lang][triplet] for triplet in columns])
        for triplet in columns:
            if triplet in data[lang]:
                matrix[index][columns[triplet]] = data[lang][triplet]
        languages.append(lang)
        index += 1

    return matrix, languages


def power_iteration(X):
    """
    Compute the eigenvector with the greatest eigenvalue
    of the covariance matrix of X (a numpy array).

    Return two values:
    - the eigenvector (1D numpy array) and
    - the corresponding eigenvalue (a float)
    """

    X = X.transpose()

    cov = np.cov(X)

    vector = np.random.rand(X.shape[0])
    while True:
        old_vector = vector
        vector = np.dot(cov, vector)
        vector = vector_norm(vector)

        if np.isclose(old_vector, vector).all():
            break

    return vector, cov.dot(vector.transpose()).dot(vector)


def vector_norm(vector):
    return vector / np.sqrt(np.sum(vector ** 2))


def power_iteration_two_components(X):
    """
    Compute first two eigenvectors and eigenvalues with the power iteration method.
    This function should use the power_iteration function internally.

    Return two values:
    - the two eigenvectors (2D numpy array, each eigenvector in a row) and
    - the corresponding eigenvalues (a 1D numpy array)
    """

    first_vector, first_value = power_iteration(X)

    X = X.transpose()

    second_vector, second_value = first_vector * np.math.cos(90), 0

    return np.array([first_vector, second_vector]), np.array([first_value, second_value])


def project_to_eigenvectors(X, vecs):
    """
    Project matrix X onto the space defined by eigenvectors.
    The output array should have as many rows as X and as many columns as there
    are vectors.
    """
    pass


def total_variance(X):
    """
    Total variance of the data matrix X. You will need to use for
    to compute the explained variance ratio.
    """
    return np.var(X, axis=0, ddof=1).sum()


def explained_variance_ratio(X, eigenvectors, eigenvalues):
    """
    Compute explained variance ratio.
    """
    pass


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


if __name__ == "__main__":
    # prepare the data matrix
    # X, languages = prepare_data_matrix()
    INDEX_PATH = "D:\Jakob\\3letnik\semester1\git\PI\homework3_PCA\data\INDEX.txt"
    DATA_PATH = "D:\Jakob\\3letnik\semester1\git\PI\homework3_PCA\data\\test"

    if platform.system() == "Linux":
        INDEX_PATH = "/home/jakob/Documents/semester1_19-20/PI/homework3_PCA/data/INDEX.txt"
        DATA_PATH = "/home/jakob/Documents/semester1_19-20/PI/homework3_PCA/data/test"

    data, cols = read_files(INDEX_PATH, DATA_PATH)

    matrix, languages = prepare_data_matrix(data, cols)

    vec, val = power_iteration(matrix)

    print("Hello World!");

    # PCA
    # ...

    # plotting
    # ...
