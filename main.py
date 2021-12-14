from sklearn.neural_network import MLPClassifier
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

waveAttributesFloats = ["significant height","max height","zero upcrossing wave period","peak energy wave period","Peak Direction","sea surface temperature"]
waveRowsFloats = np.loadtxt(dataFile, delimiter=",", skiprows=1, usecols=(1, 2, 3, 4, 5, 6))




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



data = np.append(daysList, waveRowsFloats, axis=1)

print(data)



#plt.scatter(daysList, waveRowsFloats[:, 5])
#plt.show()





# # Algorithm
# logisticReg = linear_model.LogisticRegression()



# Training
# x = np.array(daysList).reshape(-1, 1)
# y = waveRowsFloats[:, 5]
x = waveRowsFloats
y = waveRowsStrings







# xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.01, random_state=4)
# neuralNetwork = MLPClassifier(activation='logistic', solver='sgd', hidden_layer_sizes=(1, 2), random_state=1)
# neuralNetwork.fit(xTrain, yTrain.values.ravel())
# prediction = neuralNetwork.predict(xTest)
# testValues = yTest.values
# correctCount = 0
# for i in range(len(prediction)):
#     if prediction[i] == testValues[i]:
#         correctCount += 1
#
# print("This is the accuracy: ", correctCount/len(prediction))

