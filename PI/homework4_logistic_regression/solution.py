import platform

import numpy as np
from scipy.optimize import fmin_l_bfgs_b


def load(name):
    """
    Odpri datoteko. Vrni matriko primerov (stolpci so znacilke)
    in vektor razredov.
    """
    data = np.loadtxt(name)
    X, y = data[:, :-1], data[:, -1].astype(np.int)
    return X, y


def h(x, theta):
    """
    Napovej verjetnost za razred 1 glede na podan primer (vektor vrednosti
    znacilk) in vektor napovednih koeficientov theta.
    """
    # ... dopolnite (naloga 1)

    power = x.dot(-theta.T)

    return 1 / (1 + np.exp(power))


def sixEight(x, theta, yi):
    # return yi * np.log(max(h(x, theta), 0.1 ** 15)) + (1 - yi) * np.log(max((1 - h(x, theta)), 0.1 ** 15))
    return yi * np.log(h(x, theta)) + (1 - yi) * np.log((1 - h(x, theta)))


def cost(theta, X, y, lambda_):
    """
    Vrednost cenilne funkcije.
    """
    # ... dopolnite (naloga 1, naloga 2)
    reg = lambda_ * sum([e ** 2 for e in theta])

    # return -1 / len(y) * sum([sixEight(x, theta, yi) for x, yi in zip(X, y)]) + reg
    return -1 / len(y) * sum([sixEight(x, theta, yi) for x, yi in zip(X, y)]) + reg


def grad(theta, X, y, lambda_):
    """
    Odvod cenilne funkcije. Vrne 1D numpy array v velikosti vektorja theta.
    """
    # ... dopolnite (naloga 1, naloga 2)

    l = []
    for i, e in enumerate(theta):
        l.append(1 / len(y) * sum([(h(x, theta) - yi) * x[i] for x, yi in zip(X, y)]) + 2 * lambda_ * e)

    return np.array(l)


def num_grad(theta, X, y, lambda_, e=1e-3):
    """
    Odvod cenilne funkcije izracunan numericno.
    Vrne numpyev vektor v velikosti vektorja theta.
    Za racunanje gradienta numericno uporabite funkcijo cost.
    """
    # ... dopolnite (naloga 1, naloga 2)
    return np.array([(cost(theta + eps, X, y, lambda_) - cost(theta - eps, X, y, lambda_)) / (2 * e)
                     for eps in np.identity(len(theta)) * e])


class LogRegClassifier(object):

    def __init__(self, th):
        self.th = th

    def __call__(self, x):
        """
        Napovej razred za vektor vrednosti znacilk. Vrni
        seznam [ verjetnost_razreda_0, verjetnost_razreda_1 ].
        """
        x = np.hstack(([1.], x))
        p1 = h(x, self.th)  # verjetno razreda 1
        return [1-p1, p1]


class LogRegLearner(object):

    def __init__(self, lambda_=0.0):
        self.lambda_ = lambda_

    def __call__(self, X, y):
        """
        Zgradi napovedni model za ucne podatke X z razredi y.
        """
        X = np.hstack((np.ones((len(X),1)), X))

        # optimizacija
        theta = fmin_l_bfgs_b(
            cost,
            x0=np.zeros(X.shape[1]),
            args=(X, y, self.lambda_),
            fprime=grad)[0]

        return LogRegClassifier(theta)


def test_learning(learner, X, y):
    """ vrne napovedi za iste primere, kot so bili uporabljeni pri učenju.
    To je napačen način ocenjevanja uspešnosti!

    Primer klica:
        res = test_learning(LogRegLearner(lambda_=0.0), X, y)
    """
    c = learner(X,y)
    results = [c(x) for x in X]
    return results


def test_cv(learner, X, y, k=5):
    """
    Primer klica:
        res = test_cv(LogRegLearner(lambda_=0.0), X, y)
    ... dopolnite (naloga 3)
    """

    groups = [[]] * k

    for i, x in enumerate(X):
        groups[i % k].append(x)

    c = learner(X, y)
    results = [c(x) for x in X]
    return results


def CA(real, predictions):
    solution = [0 if x > y else 1 for x, y in predictions]
    correct = np.count_nonzero(np.equal(solution, real))

    return correct / len(real)

def AUC(real, predictions):
    # ... dopolnite (dodatna naloga)
    pass


if __name__ == "__main__":
    # Primer uporabe

    DATA_PATH = "D:\Jakob\\3letnik\semester1\git\PI\homework4_logistic_regression\data\\reg.data"

    if platform.system() == "Linux":
        DATA_PATH = "/home/jakob/Documents/semester1_19-20/PI/homework4_logistic_regression/data/reg.data"
    X, y = load(DATA_PATH)

    learner = LogRegLearner(lambda_=0.0)
    classifier = learner(X, y)  # dobimo model

    napoved = classifier(X[0])  # napoved za prvi primer
    print(napoved)
