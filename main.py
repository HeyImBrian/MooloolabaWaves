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




# # Algorithm
# linReg = linear_model.LinearRegression()
#
#
# plt.scatter()