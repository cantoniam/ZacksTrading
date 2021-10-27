#####################################################################
#
# FileName : ZacksList
#
# Usage : Functions that grab the Zacks List ranking, company report
#         or other available stock information from Zacks.com
#
#####################################################################

import os
import pandas as pd
import urllib.request
import socket

# return zacks info for the given symbol
def Zacks_Info(symbol):
    data_str = ""
    url = 'https://quote-feed.zacks.com/index?t='+symbol
    try:
        downloaded_data  = urllib.request.urlopen(url, timeout=2)
        data = downloaded_data.read()
        data_str = data.decode()
    except urllib.error.HTTPError as err:
        if isinstance(err.reason, socket.timeout):
            print("HTTPError socket time out for: " + url)
        else:
            print(err.code + ": " + err.reason + " for" + url)
    except urllib.error.URLError as err:
        if isinstance(err.reason, socket.timeout):
            print("URLError socket time out for: " + url)
        else:
            print("URLError for" + url)
    except socket.timeout as err:
        print("socket timed out - URL:" + url)
    return data_str
    
# return the company report, has more information, but takes longer to retrieve
def Zacks_CompanyReport(symbol):
    data_str = ""
    my_url = "https://www.zacks.com/stock/research/"+symbol+"/company-reports"
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=my_url, headers=headers)
    try:
        downloaded_data  = urllib.request.urlopen(req, timeout=2)
        data = downloaded_data.read()
        data_str = data.decode()
    except urllib.error.HTTPError as err:
        if isinstance(e.reason, socket.timeout):
            print("HTTPError socket time out for: " + my_url)
        else:
            print(err.code + ": " + err.reason + " for" + my_url)
    except urllib.error.URLError as err:
        if isinstance(err.reason, socket.timeout):
            print("URLError socket time out for: " + my_url)
        else:
            print(err.reason + " for" + my_url)
    except socket.timeout as err:
        print("socket timed out - URL:" + my_url)
    return data_str

# Get a specific property from a zacks info string
def Zacks_GetProperty(symbol, zacks_property, zacks_info):
    zacks_property_ret_str = ""
    pos = zacks_info.find("\""+zacks_property+"\":\"")
    if(pos != -1):
        first_pos = pos + len(zacks_property) + 4
        end_pos = zacks_info.find("\",", first_pos, -1)
        zacks_property_ret_str = zacks_info[first_pos:end_pos]
        zacks_property_ret_str = zacks_property_ret_str.replace(",","")
    return zacks_property_ret_str

# Get a data item from the company report for a symbol
def Zacks_GetData(symbol, data_item, company_report):
    zacks_data_item_ret_str = ""
    pos = company_report.find(data_item)
    if(pos != -1):
        search_pos = pos + len(data_item)
        first_pos = company_report.find("<td>", search_pos, -1)
        first_pos += 4
        end_pos = company_report.find("</td>", first_pos, -1)
        zacks_data_item_ret_str = company_report[first_pos:end_pos]
        zacks_data_item_ret_str = zacks_data_item_ret_str.replace(",","")
    return zacks_data_item_ret_str
    
# Get a ribbon data item from the company report.
def Zacks_GetRibbonData(symbol, ribbon_property, company_report):
    ribbon_property_ret_str = ""
    pos = company_report.find(ribbon_property)
    if(pos != -1):
        search_pos = pos
        first_pos = company_report.find(">", search_pos, -1)
        first_pos += 1
        end_pos = company_report.find("<", first_pos, -1)
        ribbon_property_ret_str = company_report[first_pos:end_pos]
        ribbon_property_ret_str = ribbon_property_ret_str.replace(",","")
    return ribbon_property_ret_str

# Get the map of the Zack's info map for each of the given symbols.
def GetZacksInfoMap(symbols):
    zacks_info_map = {}
    for symbol in symbols:
        zacks_info_map[symbol] = Zacks_Info(symbol)
    return zacks_info_map

# Get the map of the symbols to their company report.
def GetZacksCompanyReportMap(symbols):
    zacks_report_map = {}
    for symbol in symbols:
        zacks_report_map[symbol] = Zacks_CompanyReport(symbol)
    return zacks_report_map

# Get the map of symbols to their Zacks specified property.
def GetZacksPropertyMap(symbols, property_name):
    zacks_prop_map = {}
    for symbol in symbols:
        zacks_info = Zacks_Info(symbol)
        property_str = Zacks_GetProperty(symbol, property_name, zacks_info)
        zacks_prop_map[symbol] = property_str
    return zacks_prop_map

# get the map of symbols to their data item
def GetZacksDataMap(symbols, data_item):
    zacks_data_map = {}
    for symbol in symbols:
        company_report = Zacks_CompanyReport(symbol)
        data_item_str = Zacks_GetData(symbol, data_item, company_report)
        zacks_data_map[symbol] = data_item_str
    return zacks_data_map
    
# Get the map of symbos to their ribbon_item
def GetZacksDataRibbonMap(symbols, ribbon_item):
    zacks_data_ribbon_map = {}
    for symbol in symbols:
        company_report = Zacks_CompanyReport(symbol)
        data_item_str = Zacks_GetRibbonData(symbol, ribbon_item, company_report)
        zacks_data_ribbon_map[symbol] = data_item_str
    return zacks_data_ribbon_map