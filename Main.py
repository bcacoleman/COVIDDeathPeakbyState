
import csv
import os
import os.path
import sys

import tkinter as tk
from tkinter import ttk as ttk
import tkinter.filedialog as filedialog

"""
input_path = tk.filedialog.askopenfilename(filetypes=[("CSV files", ".csv")],
                                             title='Select CSV containing COVID-19 Deaths data:')
"""
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import time


#input_path = 'DeathsByState.csv'
input_path = '/Users/bcoleman/PycharmProjects/covid-19-usa-by-state/COVID-19-Deaths-USA-By-State.csv'
deaths = pd.read_csv(input_path,index_col='State')
deathDF=deaths.transpose()
deathDF.head()
#deathDF = deathDF.rename(columns={'State':'Date'})

Cols=list(deathDF.columns)

KeepList=['State','Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
                    'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia',
                    'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky',
                    'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
                    'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
                    'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
                    'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
                    'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

DropList=np.setdiff1d(Cols,KeepList)
C19Deaths = deathDF.drop(DropList,axis=1)

States=list(C19Deaths.columns)

DailyDeaths = C19Deaths.diff()

ThreeDayAvg = pd.DataFrame()
SevenDayAvg = pd.DataFrame()
NineDayAvg = pd.DataFrame()

for col in States:
    ThreeDayAvg[col] = DailyDeaths.loc[:,col].rolling(window=3).mean()
    SevenDayAvg[col] = DailyDeaths.loc[:,col].rolling(window=7).mean()
    NineDayAvg[col] = DailyDeaths.loc[:,col].rolling(window=9).mean()

OneDayFrame = pd.DataFrame()
ThreeDayFrame = pd.DataFrame()
SevenDayFrame = pd.DataFrame()
NineDayFrame = pd.DataFrame()

for col in States:
    max1=DailyDeaths[col].max()
    indexMax1=DailyDeaths[col].idxmax()
    max3 = ThreeDayAvg[col].max()
    indexMax3 = ThreeDayAvg[col].idxmax()
    max7 = SevenDayAvg[col].max()
    indexMax7 = SevenDayAvg[col].idxmax()
    max9 = NineDayAvg[col].max()
    indexMax9 = NineDayAvg[col].idxmax()
    OneDayFrame[col]=[max1,indexMax1]
    ThreeDayFrame[col]=[max3,indexMax3]
    SevenDayFrame[col]=[max7,indexMax7]
    NineDayFrame[col]=[max9,indexMax9]

OneDayMaxFrame = pd.DataFrame()
OneDayMaxFrame = OneDayFrame.transpose()
OneDayMaxFrame = OneDayMaxFrame.reset_index()
OneDayMaxFrame = OneDayMaxFrame.rename(columns={'index':'State',0:'Peak1DayDeaths',1:'Peak1DayDate'})

ThreeDayAvgFrame = pd.DataFrame()
ThreeDayAvgFrame = ThreeDayFrame.transpose()
ThreeDayAvgFrame = ThreeDayAvgFrame.reset_index()
ThreeDayAvgFrame = ThreeDayAvgFrame.rename(columns={'index':'State',0:'Peak3DayAvgDeaths',1:'Peak3DayAvgDate'})

SevenDayAvgFrame = pd.DataFrame()
SevenDayAvgFrame = SevenDayFrame.transpose()
SevenDayAvgFrame = SevenDayAvgFrame.reset_index()
SevenDayAvgFrame = SevenDayAvgFrame.rename(columns={'index':'State',0:'Peak7DayAvgDeaths',1:'Peak7DayAvgDate'})

NineDayAvgFrame = pd.DataFrame()
NineDayAvgFrame = NineDayFrame.transpose()
NineDayAvgFrame = NineDayAvgFrame.reset_index()
NineDayAvgFrame = NineDayAvgFrame.rename(columns={'index':'State',0:'Peak9DayAvgDeaths',1:'Peak9DayAvgDate'})

TotalDF = pd.DataFrame()
TotalDF['State']=States
TotalDF['Peak1DayDeaths']=OneDayMaxFrame['Peak1DayDeaths']
TotalDF['Peak1DayDate']=OneDayMaxFrame['Peak1DayDate']
TotalDF['Peak3DayAvgDeaths']=ThreeDayAvgFrame['Peak3DayAvgDeaths']
TotalDF['Peak3DayAvgDate']=ThreeDayAvgFrame['Peak3DayAvgDate']
TotalDF['Peak7DayAvgDeaths']=SevenDayAvgFrame['Peak7DayAvgDeaths']
TotalDF['Peak7DayAvgDate']=SevenDayAvgFrame['Peak7DayAvgDate']
TotalDF['Peak9DayAvgDeaths']=NineDayAvgFrame['Peak9DayAvgDeaths']
TotalDF['Peak9DayAvgDate']=NineDayAvgFrame['Peak9DayAvgDate']


timestr = time.strftime("%Y%m%d")

TotalDF.to_csv('Output_%s.csv' % timestr)