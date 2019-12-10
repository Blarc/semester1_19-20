import csv
import gzip
import platform

import numpy as np

from homework5_bus_prediction import lpputils


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
    X = np.zeros(shape=(numOfRows, numOfColumns))
    y = np.empty(shape=(numOfRows, 1))
    for i, line in enumerate(reader):
        registration, driverId, route, routeDir, routeDisc, firstStation, departureTime, lastStation, arrivalTime = line

        parsedDepartureDateTime = lpputils.parsedate(departureTime)
        X[i][columns[f"{parsedDepartureDateTime.day % 7}"]] = 1

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

    return X, y


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


if __name__ == "__main__":

    TRAIN_PATH = "D:\Jakob\\3letnik\semester1\git\\UOZP\homework5_bus_prediction\data\\train_pred.csv.gz"
    TEST_PATH = "D:\Jakob\\3letnik\semester1\git\\UOZP\homework5_bus_prediction\data\\test_pred.csv.gz"
    PRECIPITATION_PATH = "D:\Jakob\\3letnik\semester1\git\\UOZP\homework5_bus_prediction\data\\precipitation.csv"

    if platform.system() == "Linux":
        TRAIN_PATH = "/home/jakob/Documents/semester1_19-20/PI/homework5_bus_prediction/data/train_pred.csv.gz"
        TEST_PATH = "/home/jakob/Documents/semester1_19-20/PI/homework5_bus_prediction/data/test_pred.csv.gz"
        PRECIPITATION_PATH = "/home/jakob/Documents/semester1_19-20/PI/homework5_bus_prediction/data/precipitation.csv"

    TIME_INTERVAL = 1800

    precipitation = createPrecipitation()

    columns, NUM_OF_ROWS, NUM_OF_COLUMNS = createColumns()

    trainX, trainY = createData(TRAIN_PATH, NUM_OF_ROWS, NUM_OF_COLUMNS, precipitation, train=True)
    testX, _ = createData(TEST_PATH, getNumberOfRows(TEST_PATH), NUM_OF_COLUMNS, precipitation, train=False)
    
    print("HELLO")
