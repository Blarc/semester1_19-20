import os
from collections import defaultdict

import numpy as np
from unidecode import unidecode


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


def prepare_data_matrix():
    """
    Return data in a matrix (2D numpy array), where each row contains triplets
    for a language. Columns should be the 100 most common triplets
    according to the idf measure.
    """
    # create matrix X and list of languages
    # ...
    return X, languages


def power_iteration(X):
    """
    Compute the eigenvector with the greatest eigenvalue
    of the covariance matrix of X (a numpy array).

    Return two values:
    - the eigenvector (1D numpy array) and
    - the corresponding eigenvalue (a float)
    """
    pass


def power_iteration_two_components(X):
    """
    Compute first two eigenvectors and eigenvalues with the power iteration method.
    This function should use the power_iteration function internally.

    Return two values:
    - the two eigenvectors (2D numpy array, each eigenvector in a row) and
    - the corresponding eigenvalues (a 1D numpy array)
    """
    pass


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
    X, languages = prepare_data_matrix()

    # PCA
    # ...

    # plotting
    # ...
