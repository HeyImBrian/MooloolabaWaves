from sklearn import datasets
from sklearn import linear_model
from sklearn.model_selection import train_test_split

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import csv
from io import StringIO



# Load csv into different variables
dataFile = "WaveData.csv"

# Store the strings, floats, and attributes in separate variables.
waveAttributesStrings = ["Date/Time"]
waveRowsStrings =pd.read_csv(dataFile, skiprows=0, usecols=[0])

waveAttributesFloats = ["significant height","max height","zero upcrossing wave period","peak energy wave period","Peak Direction","sea surface temperature"]
waveRowsFloats = np.loadtxt(dataFile, delimiter=",", skiprows=1, usecols=(1, 2, 3, 4, 5, 6))




# Algorithm
linReg = linear_model.LinearRegression()

# Combining each set of times into single day elements.
daysList = []
currDay = 0
currDataIndex = 0
maxDataIndex = waveRowsStrings.size

while currDataIndex < maxDataIndex:
    for i in range(0, 46):
        if currDataIndex < maxDataIndex:
            daysList.append(currDay)
            currDataIndex += 1
        else:
            break
    currDay += 1



# Need to remove rows with -99. Will round out the values by using surrounding ones because numpy cannot pop values
for index, row in enumerate(waveRowsFloats):
    for indexInRow, value in enumerate(row):
        if value == -99.9:

            currAddIndex = 0
            while waveRowsFloats[index][indexInRow] < 0:
                waveRowsFloats[index][indexInRow] = (((waveRowsFloats[index - currAddIndex][indexInRow]) + (waveRowsFloats[index + currAddIndex][indexInRow])) / 2)
                currAddIndex += 1



plt.scatter(daysList, waveRowsFloats[:, 5])
plt.show()






# Training
X = np.array(daysList).reshape(-1, 1)
y = waveRowsFloats[:, 5]

XTrain, XTest, yTrain, yTest = train_test_split(X, y, test_size=0.2)



model = linReg.fit(XTrain, yTrain)
predictions = model.predict(XTest)

print("Predictions: ", predictions)
print("R^2 value: ", linReg.score(X, y))
print("coedd: ", linReg.coef_)