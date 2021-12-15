from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report, confusion_matrix

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import csv
from io import StringIO
import datetime



# Load csv into different variables
dataFile = "WaveData.csv"

# Store the strings, floats, and attributes in separate variables.
waveAttributesStrings = ["Date/Time"]
waveRowsStrings = pd.read_csv(dataFile, skiprows=0, usecols=[0])

waveAttributesFloats = ["significant height","max height","zero upcrossing wave period","peak energy wave period","peak direction","temperature"]
waveRowsFloats = np.loadtxt(dataFile, delimiter=",", skiprows=1, usecols=(1, 2, 3, 4, 5, 6))

allAttributes = ["month", "day", "year", "hour", "min", "significant height","max height","zero upcrossing wave period","peak energy wave period","peak direction","temperature"]






# Setting up the time columns

currDateTime = datetime.datetime(month=1, day=1, year=2017, hour=1, minute=0)
daysList = []
monthList = []
yearList = []
hourList = []
minList = []

currDataIndex = 0
maxDataIndex = waveRowsStrings.size

while currDataIndex < maxDataIndex:

    for i in range(0, 46):
        if currDataIndex < maxDataIndex:
            daysList.append([currDateTime.day])
            monthList.append([currDateTime.month])
            yearList.append([currDateTime.year])
            hourList.append([currDateTime.hour])
            minList.append([currDateTime.minute])

            currDateTime += datetime.timedelta(minutes=30)
            currDataIndex += 1
        else:
            break







# Need to remove rows with -99.
for index, row in enumerate(waveRowsFloats):
    for indexInRow, value in enumerate(row):
        if value == -99.9:

            currAddIndex = 0
            while waveRowsFloats[index][indexInRow] < 0:
                waveRowsFloats[index][indexInRow] = (((waveRowsFloats[index - currAddIndex][indexInRow]) + (waveRowsFloats[index + currAddIndex][indexInRow])) / 2)
                currAddIndex += 1




# Appending the all attributes to the beginning of the waveRowsFloats.
# This effectively replaces the date/time in the original data.
dataTemp = np.append(minList, waveRowsFloats, axis=1)
dataTemp = np.append(hourList, dataTemp, axis=1)
dataTemp = np.append(yearList, dataTemp, axis=1)
dataTemp = np.append(daysList, dataTemp, axis=1)
dataTemp = np.append(monthList, dataTemp, axis=1)


data = pd.DataFrame(dataTemp, columns=allAttributes)


# plt.scatter(dataTemp[:, 0], dataTemp[:, 6])
# plt.show()


# y is the temperature
train, test = train_test_split(data, random_state=42)
xTrain = train[train.columns[0:5]]
yTrain = train['temperature']
xTest = test[test.columns[0:5]]
yTest = test['temperature']


# Scale the data to work better with machine learning.
# scaler = StandardScaler()
# scaler.fit(xTrain)
#
# xTrain = scaler.transform(xTrain)
# xTest = scaler.transform(xTest)
scaler = MinMaxScaler()
xTrain = scaler.fit_transform(xTrain)
xTest = scaler.fit_transform(xTest)


print(xTrain)

print("Loading")

neuralNetwork = MLPRegressor(hidden_layer_sizes=[10], max_iter=1000, activation='logistic', solver='sgd', alpha=1)
neuralNetwork.fit(xTrain, yTrain)

#  "month", "day", "year", "hour", "min",
# testData = [[8, 4, 2018, 1, 0]]
# predictions = neuralNetwork.predict(testData)
# print(predictions)




# big test
# prediction values are first ran through the scalar.transform feature.
testList = []
for index, i in enumerate(range(0, 12)):
    tempTest = np.array([index+1, 1.0, 2017.0, 1.0, 0.0])
    testList.append(tempTest)

testList = scaler.fit_transform(testList)
bruh = neuralNetwork.predict(testList)

for i in range(len(testList)):
    print(testList[i], bruh[i])


print("Accuracy Test: ", neuralNetwork.score(xTest, yTest))

