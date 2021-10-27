# ZacksStrongBuy
# Requirements: Written using python 3.9, requires the pandas library
# script takes one optional parameter to specify the input stock list CSV file
# if this parameter is not found, it will look for a file called SP500ListAll.csv
# NOTE: Import file name must end with ".csv"
# the first line must be Stocks
# Every Stock must be on its own line

# import required libraries and modules
import os
import pandas as pd
import sys
import datetime as dt
from CommonUtilities import CommonUtilities as util
from ZacksUtilities import ZacksList as zlist
from ZacksUtilities import ZacksCalculations as zcalc

# cd to the current directory
workingdirectory = os.getcwd()
os.chdir(workingdirectory)

# declare the input paramater csv file name
import_file_name = ''

# it considers no parameters as 1 parameter, the first paramater being the script name. This will be the 0 index aka sys.argv[0].
if(len(sys.argv) > 1):
    import_file_name = sys.argv[1]

# if the parameter is not supplied, default to all S&P500 stocks
if(len(import_file_name) == 0):
    import_file_name = 'SP500ListAll.csv'

# import the csv stock list
import_csv_filename = path_or_buf=workingdirectory +'/input/'+ import_file_name
favorites = []
if(util.PathExists(import_csv_filename)):
    favorites_csv = pd.read_csv(import_csv_filename)
    favorites = favorites_csv['Stocks'] # grab the stocks column, this is the only one and will convert this to a list

results = []
# print the results for the given stocks
zacks_info_map = zlist.GetZacksInfoMap(favorites)
strong_buys_list = zcalc.GetAllZacksRank(favorites, zacks_info_map, 'Strong Buy')
print('Strong Buys are:\n')
print(strong_buys_list)
strong_buys_str = ",".join(strong_buys_list)

today = dt.datetime.today().strftime('%Y-%m-%d')
# save the file into the working directory
file_name = path_or_buf=workingdirectory +'/output/favoritesStrongBuys'+today+'.txt'
with open(file_name, "w") as text_file:
    text_file.write(strong_buys_str)