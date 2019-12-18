import csv
import datetime
import gzip
import platform
from typing import Dict

import numpy as np
import scipy.sparse

from homework5_bus_prediction import lpputils
from homework5_bus_prediction.linear import LinearLearner


def meanAbsoluteError(pred, true):
    absolutes = [abs(y - x) for x, y in zip(pred, true)]
    return sum(absolutes) / len(absolutes)


class Route:

    def __init__(self, routeNum: int):
        self.routeNum = routeNum
        self.model = None
        self.start = ""
        self.end = ""
        self.dir = ""

        # columns for train and test data
        self.columns = {}
        self.columnsCounter = 0

        # train data
        self.trainRowsCounter = 0
        self.trainX = None
        self.trainY = None
        self.trainDepartureTimes = []
        self.trainRowsIndex = 0

        # add participation columns
        # self.addColumn("rain")
        # self.addColumn("snow")

        # add departure day of week columns
        for i in range(7):
            self.addColumn(str(i))

        # add departure month
        # for i in range(1, 13):
        #     self.addColumn(str(i) + "month")

        # add departure time columns
        for i in range(0, 86400, TIME_INTERVAL):
            self.addColumn(i)

    def addColumn(self, col):
        self.columns[col] = self.columnsCounter
        self.columnsCounter += 1

    def addTrainDepartureTime(self, departureTime: datetime):
        self.trainDepartureTimes.append(departureTime)

    # initializes trainMatrix with zeros

    def initTrainMatrix(self):
        self.trainX = np.zeros(shape=(self.trainRowsCounter, self.columnsCounter))
        self.trainY = np.empty(self.trainRowsCounter)

    # initializes testMatrix with zeros

    # def fillTrainMonth(self, departureTime: datetime):
    #     self.trainX[self.trainRowsIndex][self.columns[str(departureTime.month) + "month"]] = 1

    def fillTrainDay(self, departureTime: datetime):
        self.trainX[self.trainRowsIndex][self.columns[str(departureTime.weekday())]] = 1

    def fillTrainTime(self, departureTime: datetime):
        time = departureTime.time()
        seconds = (time.hour * 60 + time.minute) * 60 + time.second
        approximation = seconds - (seconds % TIME_INTERVAL)
        self.trainX[self.trainRowsIndex][self.columns[approximation]] = 1

    def fillTrainFirstStation(self, firstStation: str):
        self.trainX[self.trainRowsIndex][self.columns[firstStation]] = 1

    def fillTrainLastStation(self, lastStation: str):
        self.trainX[self.trainRowsIndex][self.columns[lastStation]] = 1

    def fillTrainY(self, clazz: float):
        self.trainY[self.trainRowsIndex] = clazz

    def setModel(self):
        sparseX = scipy.sparse.csr_matrix(self.trainX)
        learner = LinearLearner(lambda_=0.1)
        self.model = learner(sparseX, self.trainY)

    def getPredictionsTrain(self):
        return [self.model(x) for x in self.trainX]

    def predict(self, x):
        return self.model(x)

    def getMAETrain(self) -> float:
        return meanAbsoluteError(self.getPredictionsTrain(), self.trainY)

    # def getPredictionsTest(self):
    #     sparseX = scipy.sparse.csr_matrix(self.trainX)
    #     learner = LinearLearner(lambda_=0.1)
    #     model = learner(sparseX, self.trainY)
    #
    #     return [model(x) for x in self.testX]

    # def toOutput(self):
    #     for departureTime, prediction in zip(self.testDepartureTimes, self.getPredictionsTest()):
    #         print(departureTime + datetime.timedelta(seconds=prediction), file=OUT)


def createRoutes() -> (Dict[int, Route], int):
    f = gzip.open(TRAIN_PATH, "rt")
    reader = csv.reader(f, delimiter="\t")
    next(reader)

    routes: Dict[int, Route] = {}

    for line in reader:
        registration, driverId, routeNum, routeDir, routeDesc, firstStation, departureTime, lastStation, arrivalTime = line

        routeDir = routeDir.upper()
        firstStation = firstStation.upper()

        # add route to routes if it doesn't exist
        if routeDir not in routes:
            routes[routeDir] = Route(int(routeNum))
            routes[routeDir].start = firstStation
            routes[routeDir].end = lastStation.upper()
            routes[routeDir].dir = routeDir

        route = routes[routeDir]
        route.trainRowsCounter += 1

    return routes


def fillRoutes(path):
    f = gzip.open(path, "rt")
    reader = csv.reader(f, delimiter="\t")
    next(reader)

    for line in reader:
        registration, driverId, routeNum, routeDir, routeDisc, firstStation, departureTime, lastStation, arrivalTime = line

        routeDir = routeDir.upper()
        parsedDepartureTime = lpputils.parsedate(departureTime)
        parsedArrivalTime = lpputils.parsedate(arrivalTime)

        route = ROUTES[routeDir]
        if route.trainX is None:
            route.initTrainMatrix()

        route.addTrainDepartureTime(parsedDepartureTime)
        route.fillTrainDay(parsedDepartureTime)
        # route.fillTrainMonth(parsedDepartureTime)
        route.fillTrainTime(parsedDepartureTime)
        route.fillTrainY((parsedArrivalTime - parsedDepartureTime).total_seconds())
        route.trainRowsIndex += 1


# reads the test data and counts number of rows for each route
# def getNumberOfTestRows():
#     f = gzip.open(TEST_PATH, "rt")
#     reader = csv.reader(f, delimiter="\t")
#     next(reader)
#
#     for line in reader:
#         _, _, routeNum, _, _, _, _, _, _ = line
#
#         routeNum = int(routeNum)
#         ROUTES[routeNum].testRowsCounter += 1


if __name__ == "__main__":

    OUT = open("tekmovanjeOut.txt", "w")

    TRAIN_PATH = "D:\Jakob\\3letnik\semester1\git\\UOZP\homework5_bus_prediction\data\\train.csv.gz"
    TEST_PATH = "D:\Jakob\\3letnik\semester1\git\\UOZP\homework5_bus_prediction\data\\test.csv.gz"
    PRECIPITATION_PATH = "D:\Jakob\\3letnik\semester1\git\\UOZP\homework5_bus_prediction\data\\precipitation.csv"

    if platform.system() == "Linux":
        TRAIN_PATH = "/home/jakob/Documents/semester1_19-20/PI/homework5_bus_prediction/data/train.csv.gz"
        TEST_PATH = "/home/jakob/Documents/semester1_19-20/PI/homework5_bus_prediction/data/test.csv.gz"
        PRECIPITATION_PATH = "/home/jakob/Documents/semester1_19-20/PI/homework5_bus_prediction/data/precipitation.csv"

    # HOLIDAYS_DAYS = [
    #     datetime.datetime(2012, 1, 1),
    #     datetime.datetime(2012, 1, 2),
    #     datetime.datetime(2012, 2, 8),
    #     datetime.datetime(2012, 4, 8),
    #     datetime.datetime(2012, 4, 9),
    #     datetime.datetime(2012, 4, 27),
    #     datetime.datetime(2012, 5, 1),
    #     datetime.datetime(2012, 5, 2),
    #     datetime.datetime(2012, 6, 25),
    #     datetime.datetime(2012, 8, 15),
    #     datetime.datetime(2012, 9, 31),
    #     datetime.datetime(2012, 10, 1),
    #     datetime.datetime(2012, 12, 25),
    #     datetime.datetime(2012, 12, 26),
    # ]

    # 225
    TIME_INTERVAL = 150

    ROUTES: Dict[int, Route] = createRoutes()

    fillRoutes(TRAIN_PATH)

    for r in ROUTES.values():
        r.setModel()
        # print(
        #     f"Route: {r.routeNum}, Dir:{r.dir}, Start:{r.start}, End:{r.end} RowsCounter: {r.trainRowsCounter}, MAE: {r.getMAETrain()}")

    f = gzip.open(TEST_PATH, "rt")
    fileReader = csv.reader(f, delimiter="\t")
    next(fileReader)

    predictionsTest = []
    realTest = []

    for l in fileReader:
        _, _, routeNumber, routeDir, _, _, departureTime, lastStation, arrivalTime = l

        routeDir = routeDir.upper()

        # if routeDir in ROUTES:
        r = ROUTES[routeDir]

        x = np.zeros(r.columnsCounter)

        parsedDepartureTime = lpputils.parsedate(departureTime)
        # month = str(parsedDepartureTime.month) + "month"
        time = parsedDepartureTime.time()
        seconds = (time.hour * 60 + time.minute) * 60 + time.second
        approx = seconds - (seconds % TIME_INTERVAL)

        day = str(parsedDepartureTime.weekday())

        x[r.columns[approx]] = 1
        x[r.columns[day]] = 1

        # predTime = r.model(x)
        # predictionsTest.append(predTime)
        #
        # realTime = (lpputils.parsedate(arrivalTime) - parsedDepartureTime).total_seconds()
        # realTest.append(realTime)

        print(parsedDepartureTime + datetime.timedelta(seconds=r.model(x)), file=OUT)

# print(meanAbsoluteError(predictionsTest, realTest))

print("done!")
