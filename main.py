from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report, confusion_matrix

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import csv
import datetime
import pickle

from flask import Flask, render_template, url_for, request, redirect












scaler = MinMaxScaler()
neuralNetwork = 0

xTest = 0
yTest = 0



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
xTrainData = train[train.columns[0:5]]
yTrain = train['temperature']
xTestData = test[test.columns[0:5]]
yTest = test['temperature']


# Scale the data to work better with machine learning.
scaler = MinMaxScaler()
xTrain = scaler.fit_transform(xTrainData)
xTest = scaler.fit_transform(xTestData)

neuralNetwork = MLPRegressor(hidden_layer_sizes=(5, 5, 5), max_iter=1000, activation='logistic', solver='sgd', alpha=1)


def trainModel():
    neuralNetwork.fit(xTrain, yTrain)


#  "month", "day", "year", "hour", "min"


# This saves the model into a file.
def saveModel(model):
    filename = "saved_model.sav"
    pickle.dump(model, open(filename, 'wb'))


# This will load the model from the saved file
def retrieveModel():
    filename = "saved_model.sav"
    savedModel = pickle.load(open(filename, 'rb'))
    return savedModel


neuralNetwork = retrieveModel()


# # big test
# # prediction values are first ran through the scalar.transform feature.
# testList = []
# for index, i in enumerate(range(0, 12)):
#     tempTest = np.array([index+1, 1.0, 2025.0, 1.0, 0.0])
#     testList.append(tempTest)
#
# testList = scaler.fit_transform(testList)
# bruh = neuralNetwork.predict(testList)
#
# for i in range(len(testList)):
#     print(testList[i], bruh[i])
#
#
# print("Accuracy Test: ", neuralNetwork.score(xTest, yTest))


def predictTemperature(form):
    # Received datetime format: 2022-01-01 17:14
    # Year, Month, Day, Hour, Minute

    inputDate = request.form['date']
    inputTime = request.form['time']




    year = float(form[0:4])
    month = float(form[5:7])
    day = float(form[8:10])

    hour = float(form[11:13])
    minute = float(form[14:16])

    print(year)
    print(month)
    print(day)

    print(hour)
    print(minute)
    print()


    # Creating quick test data. This is needed for the scaler.fit_transform() function
    inputList = []
    userInput = np.array([month, day, year, hour, minute])
    inputList.append(userInput)
    for index, i in enumerate(range(0, 12)):
        tempInput = np.array([i, i*2, 2017+(i*0.2), i*2, i*5])
        inputList.append(tempInput)



    print("before transform: ", inputList[0])
    print()
    inputList = scaler.fit_transform(inputList)
    print("after transform: ", inputList[0])
    print()
    temp = neuralNetwork.predict(inputList)
    print("after predict: ", temp[0])
    print()


    # Temp[0] is the prediction of the user's input.
    result = temp[0]
    return result



# Setting up Flask.
# This will communicate with the webpage.
app = Flask(__name__)  # __name__ references this file



@app.route('/', methods=['GET', 'POST'])
def index():
    tempResult = False
    if request.method == 'POST':
        dateForm = request.form["date"]
        timeForm = request.form["time"]
        dateTimeForm = dateForm + " " + timeForm

        temperatureResult = predictTemperature(dateTimeForm)
        accuracyTest = neuralNetwork.score(xTest, yTest)

        return redirect(url_for("estimate", result=temperatureResult))
    return render_template('index.html')



@app.route("/", methods=['GET', 'POST'])
def estimate(dateTimeForm):
    return f"<h1>{dateTimeForm}</h1>"



if __name__ == "__main__":
    app.run(debug=True)
