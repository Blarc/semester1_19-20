import csv
import datetime
import gzip
import platform
from typing import Dict

import numpy as np

from homework5_bus_prediction import lpputils


class Route:
    def __init__(self, routeNum: int):
        self.routeNum = routeNum

        # columns for train and test data
        self.columns = {}
        self.columnsCounter = 0

        # train data
        self.trainRowsCounter = 0
        self.trainX = None
        self.trainY = None
        self.trainDepartureTimes = []
        self.trainRowsIndex = 0

        # test data
        self.testRowsCounter = 0
        self.testX = None
        self.testY = None
        self.testDepartureTimes = []
        self.testRowsIndex = 0

        # add participation columns
        self.addColumn("rain")
        self.addColumn("snow")

        # add departure day of week columns
        for i in range(7):
            self.addColumn(str(i))

        # add departure time columns
        for i in range(0, 86400, TIME_INTERVAL):
            self.addColumn(i)

    def addColumn(self, col):
        self.columns[col] = self.columnsCounter
        self.columnsCounter += 1

    def addTrainDepartureTime(self, departureTime: datetime):
        self.trainDepartureTimes.append(departureTime)

    def addTestDepartureTime(self, departureTime: datetime):
        self.testDepartureTimes.append(departureTime)

    # initializes trainMatrix with zeros
    def initTrainMatrix(self):
        self.trainX = np.zeros(shape=(self.trainRowsCounter, self.columnsCounter))
        self.trainY = np.empty(self.trainRowsCounter)

    # initializes testMatrix with zeros
    def initTestMatrix(self):
        self.testX = np.zeros(shape=(self.testRowsCounter, self.columnsCounter))
        self.testY = np.empty(self.testRowsCounter)

    def fillTrainDay(self, departureTime: datetime):
        self.trainX[self.trainRowsIndex][self.columns[str(departureTime.day % 7)]] = 1

    def fillTestDay(self, departureTime: datetime):
        self.testX[self.testRowsIndex][self.columns[str(departureTime.day % 7)]] = 1

    def fillTrainTime(self, departureTime: datetime):
        time = departureTime.time()
        seconds = (time.hour * 60 + time.minute) * 60 + time.second
        approximation = seconds - (seconds % TIME_INTERVAL)
        self.trainX[self.trainRowsIndex][self.columns[approximation]] = 1

    def fillTestTime(self, departureTime: datetime):
        time = departureTime.time()
        seconds = (time.hour * 60 + time.minute) * 60 + time.second
        approximation = seconds - (seconds % TIME_INTERVAL)
        self.testX[self.testRowsIndex][self.columns[approximation]] = 1

    def fillTrainFirstStation(self, firstStation: str):
        self.trainX[self.trainRowsIndex][self.columns[firstStation]] = 1

    def fillTestFirstStation(self, firstStation: str):
        self.testX[self.testRowsIndex][self.columns[firstStation]] = 1

    def fillTrainLastStation(self, lastStation: str):
        self.trainX[self.trainRowsIndex][self.columns[lastStation]] = 1

    def fillTestLastStation(self, lastStation: str):
        self.testX[self.testRowsIndex][self.columns[lastStation]] = 1

    def fillTrainY(self, clazz: float):
        self.trainY[self.trainRowsIndex] = clazz


def createRoutes() -> (Dict[int, Route], int):
    f = gzip.open(TRAIN_PATH, "rt")
    reader = csv.reader(f, delimiter="\t")
    next(reader)

    routes: Dict[int, Route] = {}

    for line in reader:
        registration, driverId, routeNum, routeDir, routeDesc, firstStation, departureTime, lastStation, arrivalTime = line

        routeNum = int(routeNum)
        firstStation = firstStation.upper()
        lastStation = lastStation.upper()

        # add route to routes if it doesn't exist
        if routeNum not in routes:
            routes[routeNum] = Route(routeNum)

        route = routes[routeNum]
        route.trainRowsCounter += 1

        # add columns related to data
        if firstStation not in route.columns:
            route.addColumn(firstStation)

        if lastStation not in route.columns:
            route.addColumn(lastStation)

    return routes


def fillRoutes(path, precipitationData, train):
    f = gzip.open(path, "rt")
    reader = csv.reader(f, delimiter="\t")
    next(reader)

    for line in reader:
        registration, driverId, routeNum, routeDir, routeDisc, firstStation, departureTime, lastStation, arrivalTime = line

        routeNum = int(routeNum)
        firstStation = firstStation.upper()
        lastStation = lastStation.upper()
        parsedDepartureTime = lpputils.parsedate(departureTime)
        route = ROUTES[routeNum]

        if train:
            parsedArrivalTime = lpputils.parsedate(arrivalTime)
            route.addTrainDepartureTime(parsedDepartureTime)
            route.fillTrainDay(parsedDepartureTime)
            route.fillTrainTime(parsedDepartureTime)
            route.fillTrainFirstStation(firstStation)
            route.fillTrainLastStation(lastStation)
            route.fillTrainY((parsedArrivalTime - parsedDepartureTime).total_seconds())
            route.trainRowsIndex += 1
        else:
            route.addTestDepartureTime(parsedDepartureTime)
            route.fillTestDay(parsedDepartureTime)
            route.fillTestTime(parsedDepartureTime)
            route.fillTestFirstStation(firstStation)
            route.fillTestLastStation(lastStation)
            route.testRowsIndex += 1


# reads the test data and counts number of rows for each route
def getNumberOfTestRows():
    f = gzip.open(TEST_PATH, "rt")
    reader = csv.reader(f, delimiter="\t")
    next(reader)

    for line in reader:
        _, _, routeNum, _, _, _, _, _, _ = line

        routeNum = int(routeNum)
        ROUTES[routeNum].testRowsCounter += 1


if __name__ == "__main__":

    OUT = open("out.txt", "w")

    TRAIN_PATH = "D:\Jakob\\3letnik\semester1\git\\UOZP\homework5_bus_prediction\data\\train_pred.csv.gz"
    TEST_PATH = "D:\Jakob\\3letnik\semester1\git\\UOZP\homework5_bus_prediction\data\\test_pred.csv.gz"
    PRECIPITATION_PATH = "D:\Jakob\\3letnik\semester1\git\\UOZP\homework5_bus_prediction\data\\precipitation.csv"

    if platform.system() == "Linux":
        TRAIN_PATH = "/home/jakob/Documents/semester1_19-20/PI/homework5_bus_prediction/data/train.csv.gz"
        TEST_PATH = "/home/jakob/Documents/semester1_19-20/PI/homework5_bus_prediction/data/test.csv.gz"
        PRECIPITATION_PATH = "/home/jakob/Documents/semester1_19-20/PI/homework5_bus_prediction/data/precipitation.csv"

    # 225
    TIME_INTERVAL = 300

    ROUTES: Dict[int, Route] = createRoutes()

    getNumberOfTestRows()

    # initialize matrices for data (X, y)
    for r in ROUTES.values():
        r.initTrainMatrix()
        r.initTestMatrix()

    fillRoutes(TRAIN_PATH, None, True)
    fillRoutes(TEST_PATH, None, False)

    for t in ROUTES[14].trainDepartureTimes:
        print(t)

    print("done!")
