import csv
import gzip
import platform

import numpy as np
import scipy.sparse

from homework5_bus_prediction import lpputils
from homework5_bus_prediction.linear import LinearLearner


def createColumns():
    f = gzip.open(TRAIN_PATH, "rt")
    reader = csv.reader(f, delimiter="\t")
    next(reader)

    cols = {}
    columnsCounter = 0
    rowsCounter = 0

    for _ in reader:
        # registration, driverId, route, routeDir, routeDisc, firstStation, departureTime, lastStation, arrivalTime = line
        # if registration not in cols:
        #     cols[registration] = columnsCounter
        #     columnsCounter += 1

        # if driverId not in cols:
        #     cols[driverId] = columnsCounter
        #     columnsCounter += 1

        rowsCounter += 1

    # add departure day of week columns
    for i in range(7):
        cols[f"{i}"] = columnsCounter
        columnsCounter += 1

    # add departure time columns
    for i in range(0, 86400, TIME_INTERVAL):
        cols[i] = columnsCounter
        columnsCounter += 1

    # add participation columns
    cols["rain"] = columnsCounter
    columnsCounter += 1
    cols["snow"] = columnsCounter
    columnsCounter += 1

    return cols, rowsCounter, columnsCounter


def createData(path, numOfRows, numOfColumns, precipitationData, train):
    f = gzip.open(path, "rt")
    reader = csv.reader(f, delimiter="\t")
    next(reader)
    departures = []
    X = np.zeros(shape=(numOfRows, numOfColumns))
    y = np.empty(numOfRows)
    for i, line in enumerate(reader):
        registration, driverId, route, routeDir, routeDisc, firstStation, departureTime, lastStation, arrivalTime = line

        parsedDepartureDateTime = lpputils.parsedate(departureTime)
        departures.append(parsedDepartureDateTime)
        X[i][columns[f"{parsedDepartureDateTime.weekday()}"]] = 1

        time = parsedDepartureDateTime.time()
        seconds = (time.hour * 60 + time.minute) * 60 + time.second
        approximation = seconds - (seconds % TIME_INTERVAL)
        X[i][columns[approximation]] = 1

        _, _, n = precipitationData[parsedDepartureDateTime.strftime("%Y-%m-%d")]

        if n == "3":
            X[i][columns["rain"]] = 1
            X[i][columns["snow"]] = 1
        elif n == "1":
            X[i][columns["rain"]] = 1
        elif n == "2":
            X[i][columns["snow"]] = 1

        if train:
            y[i] = lpputils.tsdiff(arrivalTime, departureTime)

    return X, y, departures


def createPrecipitation():
    # Date Rain(mm) Snow(cm) Precipitation
    with open(PRECIPITATION_PATH) as file:
        reader = csv.reader(file, delimiter=";")
        data = {d[0]: d[1:] for d in reader}

    return data


def getNumberOfRows(path):
    f = gzip.open(path, "rt")
    reader = csv.reader(f, delimiter="\t")
    next(reader)
    rowsCounter = 0
    for _ in reader:
        rowsCounter += 1

    return rowsCounter


def meanAbsoluteError(pred, true):
    absolutes = [abs(y - x) for x, y in zip(pred, true)]
    return sum(absolutes) / len(absolutes)


if __name__ == "__main__":

    OUT = open("out.txt", "w")

    TRAIN_PATH = "D:\Jakob\\3letnik\semester1\git\\UOZP\homework5_bus_prediction\data\\train_pred.csv.gz"
    TEST_PATH = "D:\Jakob\\3letnik\semester1\git\\UOZP\homework5_bus_prediction\data\\test_pred.csv.gz"
    PRECIPITATION_PATH = "D:\Jakob\\3letnik\semester1\git\\UOZP\homework5_bus_prediction\data\\precipitation.csv"

    if platform.system() == "Linux":
        TRAIN_PATH = "/home/jakob/Documents/semester1_19-20/PI/homework5_bus_prediction/data/train_pred.csv.gz"
        TEST_PATH = "/home/jakob/Documents/semester1_19-20/PI/homework5_bus_prediction/data/test_pred.csv.gz"
        PRECIPITATION_PATH = "/home/jakob/Documents/semester1_19-20/PI/homework5_bus_prediction/data/precipitation.csv"

    TIME_INTERVAL = 225

    # 225

    precipitation = createPrecipitation()

    columns, NUM_OF_ROWS, NUM_OF_COLUMNS = createColumns()

    trainX, trainY, trainDepartureTimes = createData(TRAIN_PATH, NUM_OF_ROWS, NUM_OF_COLUMNS, precipitation, train=True)
    testX, _, testDepartureTimes = createData(TEST_PATH, getNumberOfRows(TEST_PATH), NUM_OF_COLUMNS, precipitation,
                                              train=False)

    Xsp = scipy.sparse.csr_matrix(trainX)
    learner = LinearLearner(lambda_=0.001)
    model = learner(Xsp, trainY)

    predictions = [model(x) for x in trainX]
    print(meanAbsoluteError(predictions, trainY))

    # for index, x in enumerate(testX):
    #     arrivalTimePred = lpputils.tsadd(testDepartureTimes[index], model(x))
    #     print(arrivalTimePred)
    #     print(arrivalTimePred, file=OUT)

    print("done!")
