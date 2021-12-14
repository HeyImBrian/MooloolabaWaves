from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split

from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import csv
from io import StringIO



# Load csv into different variables
dataFile = "WaveData.csv"

# Store the strings, floats, and attributes in separate variables.
waveAttributesStrings = ["Date/Time"]
waveRowsStrings = pd.read_csv(dataFile, skiprows=0, usecols=[0])

waveAttributesFloats = ["significant height","max height","zero upcrossing wave period","peak energy wave period","peak direction","temperature"]
waveRowsFloats = np.loadtxt(dataFile, delimiter=",", skiprows=1, usecols=(1, 2, 3, 4, 5, 6))

allAttributes = ["day", "significant height","max height","zero upcrossing wave period","peak energy wave period","peak direction","temperature"]


# Combining each set of times into single day elements.

def advanceDay(day):
    day += 1
    if day > 365:
        day = 1
    return day



daysList = []
currDay = 1
currDataIndex = 0
maxDataIndex = waveRowsStrings.size

while currDataIndex < maxDataIndex:
    for i in range(0, 46):
        if currDataIndex < maxDataIndex:
            daysList.append([currDay])
            currDataIndex += 1
        else:
            break

    currDay = advanceDay(currDay) # After looping through all the times in a day, go to next day.




# Need to remove rows with -99. Will round out the values by using surrounding ones because numpy cannot pop values
for index, row in enumerate(waveRowsFloats):
    for indexInRow, value in enumerate(row):
        if value == -99.9:

            currAddIndex = 0
            while waveRowsFloats[index][indexInRow] < 0:
                waveRowsFloats[index][indexInRow] = (((waveRowsFloats[index - currAddIndex][indexInRow]) + (waveRowsFloats[index + currAddIndex][indexInRow])) / 2)
                currAddIndex += 1





# Appending the days to the beginning of the waveRowsFloats.
# This effectively replaces the date/time in the original data.
dataTemp = np.append(daysList, waveRowsFloats, axis=1)
data = pd.DataFrame(dataTemp, columns=allAttributes)





plt.scatter(dataTemp[:, 0], dataTemp[:, 6])
plt.show()


# y is the temperature
train, test = train_test_split(data, random_state=42)
xTrain = train[train.columns[0:3]]
yTrain = train['temperature']
xTest = test[test.columns[0:3]]
yTest = test['temperature']


scaler = StandardScaler()
scaler.fit(xTrain)

xTrain = scaler.transform(xTrain)
xTest = scaler.transform(xTest)



neuralNetwork = MLPRegressor(hidden_layer_sizes=(10, 10, 10), max_iter=1000, activation='tanh')
neuralNetwork.fit(xTrain, yTrain)

testData = [[250,0.774,1.17]]

predictions = neuralNetwork.predict(testData)
print(predictions)

print("Accuracy Test: ", neuralNetwork.score(xTest, yTest))

