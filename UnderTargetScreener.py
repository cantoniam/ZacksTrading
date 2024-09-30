#####################################################################
#
# FileName : UnderTargetScreener
#
# Usage : This python script takes one parameter - the csv file
#         containing one symbol per line, of all the Stock Symbols
#         you wish to check against the screener. Defaults to use the
#         SP500ListAll.csv included in the input directory.
#
#####################################################################

# import required libraries and modules
import os
import pandas as pd
import sys
import datetime as dt
from CommonUtilities import CommonUtilities as util
from ZacksUtilities import ZacksList as zlist
from ZacksUtilities import ZacksCalculations as zcalc

print("Begin Screener.py")

# cd to the current directory
workingdirectory = os.getcwd()
os.chdir(workingdirectory)

print(workingdirectory)

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
print("Screener: using " + import_csv_filename + " for symbols")
symbols = []
if(util.PathExists(import_csv_filename)):
    symbols_csv = pd.read_csv(import_csv_filename)
    try:
        symbols = symbols_csv['Stocks'] # grab the stocks column, this is the only one and will convert this to a list
    except Exception as e:
        print("Input file requires a column header of \"Stocks\"" + e)

print("Get Zacks Info Map for symbols")
info_map, info_failures = zlist.GetZacksInfoMap(symbols)
print("Get Zacks Company Report for symbols")
successful_info_symbols = [symbol for symbol in symbols if symbol not in info_failures]
report_map, report_failures = zlist.GetZacksCompanyReportMap(successful_info_symbols)
successful_symbols = [symbol for symbol in successful_info_symbols if symbol not in report_failures]
failures = info_failures
failures.extend(report_failures)
if len(failures) > 0:
    print('Failed to retrieve valid data for: ')
    print(failures)

valid_ranks =["Strong Buy","Buy", "Hold"]

validated_list = zcalc.GetUndervaluedByRank(successful_symbols, report_map, info_map, True, valid_ranks)

print('\nResults:')
if("Strong Buy" in valid_ranks):
    print('Strong Buys are:\n')
    print(validated_list['Strong_Buy'])
    print('===================================')
if("Buy" in valid_ranks):
    print('Buys are:\n')
    print(validated_list['Buy'])
    print('===================================')
if("Hold" in valid_ranks):
    print('Holds are:\n')
    print(validated_list['Hold'])
    print('===================================')
if("Sell" in valid_ranks):
    print('Sells are:\n')
    print(validated_list['Sell'])
    print('===================================')
if("Strong Sell" in valid_ranks):
    print('Strong Sells are:\n')
    print(validated_list['Strong_Sell'])
    
buys_str = ",".join(validated_list['Strong_Buy']) 
if(buys_str):
    buys_str += ","
buys_str += ",".join(validated_list['Buy'])

today = dt.datetime.today().strftime('%Y-%m-%d')
new_file = path_or_buf=workingdirectory + '/output/UnderTargetScreenerResults'+today+'.txt'
with open(new_file, "w") as text_file:
    text_file.write(buys_str)