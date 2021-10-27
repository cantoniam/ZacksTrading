#####################################################################
#
# FileName : ZacksCalculations
#
# Usage : Functions that calculate something relating to the Zack's
#         list ranked stocks.
#
#####################################################################

from . import ZacksList as zlist

# returns the zacks rank for the given stock symbol
def Zacks_Ranking(symbol, zacks_info):
    zacks_rank = zlist.Zacks_GetProperty(symbol, "zacks_rank_text", zacks_info)
    return zacks_rank

# returns the earnings growth for the given stock symbol
def Zacks_EarningsGrowth(symbol, zacks_info):
    earnings_growth_str = zlist.Zacks_GetProperty(symbol, "PEG Ratio", zacks_info)
    earnings_growth = 0.0
    if(len(earnings_growth_str) > 0):
        earnings_growth = float(earnings_growth_str)
    return earnings_growth
    
# returns the last price for the given stock symbol
def Zacks_LastPrice(symbol, company_report):
    last_price_str = zlist.Zacks_GetRibbonData(symbol, "get_last_price", company_report)
    last_price = 0.0
    if(len(last_price_str) > 0):
        last_price = float(last_price_str)
    return last_price
    
# returns the average target price for the given stock symbol
def Zacks_AvgTargetPrice(symbol, company_report):
    target_price_str = zlist.Zacks_GetData(symbol, "Target Price Consensus", company_report)
    target_price = 0.0
    if(len(target_price_str) > 0):
        target_price = float(target_price_str)
    return target_price
    
# returns the percent the last price is under average target price for the given stock symbol
def Calculate_LastPricePercentOfTarget(symbol, company_report):
    last_price = Zacks_LastPrice(symbol, company_report)
    target_price = Zacks_AvgTargetPrice(symbol, company_report)
    percent = 0.0
    if not target_price == 0.0: # don't divide by zero please
        percent = (1.0 - (last_price / target_price)) * 100.0     
    return percent
    
# returns the long term growth rate for the given stock symbol, not this is not available for many stocks
def Zacks_LTGrowthRate(symbol, company_report):
    print(company_report)
    growth_rate = zlist.Zacks_GetData(symbol, "Estimated Long-Term EPS Growth Rate", company_report)
    return growth_rate
    
# returns the list of stocks by rank that are under their average target price for the given stock symbols.
# We are calling these "undervalued", although this is not the traditional definition.
def GetUndervaluedByRank(symbols, zacks_company_reports_map, zacks_info_map={}, check_rank=False, valid_ranks=[]):
    checked_list = []
    Strong_Buy=[]
    Buy=[]
    Hold=[]
    Sell=[]
    Strong_Sell=[]
    for symbol in symbols:
        passed_checks = True
        zacks_rank = ""
        if(check_rank):
            zacks_info = zacks_info_map[symbol]
            zacks_rank = zlist.Zacks_GetProperty(symbol, "zacks_rank_text", zacks_info)
            if(not(zacks_rank in valid_ranks)):
                passed_checks = False

        if(passed_checks):
            company_report = zacks_company_reports_map[symbol]
            percentGrowthLeft = Calculate_LastPricePercentOfTarget(symbol, company_report)
            if(not(percentGrowthLeft >= 15.0)):
                passed_checks = False
        if(passed_checks):
            if(zacks_rank == 'Strong Buy'):
                Strong_Buy.append(symbol)
            elif(zacks_rank == 'Buy'):
                Buy.append(symbol)
            elif(zacks_rank == 'Hold'):
                Hold.append(symbol)
            elif(zacks_rank == 'Sell'):
                Sell.append(symbol)
            elif(zacks_rank == 'Strong Sell'):
                Strong_Sell.append(symbol)
    results = {'Strong_Buy':Strong_Buy,'Buy':Buy,'Hold':Hold,'Sell':Sell,'Strong_Sell':Strong_Sell}
    
    return results

# returns the list of stocks that have a long term growth rate by rank for the given stock symbols.
def GetLTGrowthByRank(symbols, zacks_company_reports_map, zacks_info_map={}, check_rank=False, valid_ranks=[]):
    checked_list = []
    Strong_Buy=[]
    Buy=[]
    Hold=[]
    Sell=[]
    Strong_Sell=[]
    for symbol in symbols:
        print("Perform Checks on " + symbol)
        passed_checks = True
        zacks_rank = ""
        if(check_rank):
            zacks_info = zacks_info_map[symbol]
            zacks_rank = zlist.Zacks_GetProperty(symbol, "zacks_rank_text", zacks_info)
            if(not(zacks_rank in valid_ranks)):
                passed_checks = False

        if(passed_checks):
            company_report = zacks_company_reports_map[symbol]
            growth_rate_str = Zacks_LTGrowthRate(symbol, company_report)
            growth_rate = 0.0
            if(growth_rate_str == "NA"):
                growth_rate = float(growth_rate_str)
            if(not(percentGrowthLeft >= 20.0)):
                passed_checks = False
        if(passed_checks):
            if(zacks_rank == 'Strong Buy'):
                Strong_Buy.append(symbol)
            elif(zacks_rank == 'Buy'):
                Buy.append(symbol)
            elif(zacks_rank == 'Hold'):
                Hold.append(symbol)
            elif(zacks_rank == 'Sell'):
                Sell.append(symbol)
            elif(zacks_rank == 'Strong Sell'):
                Strong_Sell.append(symbol)
    results = {'Strong_Buy':Strong_Buy,'Buy':Buy,'Hold':Hold,'Sell':Sell,'Strong_Sell':Strong_Sell}
    
    return results

# Return the list of stock symbols that pass a basic screener for under target price and one of the given ranks.
def StockScreener(symbols, zacks_company_reports_map, zacks_info_map, valid_ranks = ["Hold", "Buy", "Strong Buy"]):
    symbol_results = []
    for symbol in symbols:
        company_report = zacks_company_reports_map[symbol]
        percentGrowthLeft = Calculate_LastPricePercentOfTarget(symbol, company_report)
        
        passed_screener = True
        # undervalued per projected analyst targets
        if(not(percentGrowthLeft >= 10.0)):
            passed_screener = False
        zacks_info = zacks_info_map[symbol]
        # valid rank per given ranks list
        if(not(Zacks_GetProperty(symbol, "zacks_rank_text", zacks_info) in valid_ranks)):
            passed_screener = False
            
        if(passed_screener):
            symbol_results.append(symbol)
     
    return symbol_results
    
# Returns the list of stocks for the given stock symbols by rank.
def GetAllZacksRank(symbols, zacks_info_map, ranking):
    symbols_with_rank = []
    for symbol in symbols:
        zacks_info = zacks_info_map[symbol]
        Rank = Zacks_Ranking(symbol, zacks_info)
        if(Rank == ranking):
            symbols_with_rank.append(symbol)
    return symbols_with_rank
    
# this function put each ticker in its rank list and return the result
def Market_Rank(symbols):
    Strong_Buy=[]
    Buy=[]
    Hold=[]
    Sell=[]
    Strong_Sell=[]
    for symbol in symbols:
        zacks_info = zlist.Zacks_Info(symbol)
        Rank = Zacks_Ranking(symbol, zacks_info)
        if(Rank == 'Strong Buy'):
            Strong_Buy.append(symbol)
        elif(Rank == 'Buy'):
            Buy.append(symbol)
        elif(Rank == 'Hold'):
            Hold.append(symbol)
        elif(Rank == 'Sell'):
            Sell.append(symbol)
        elif(Rank == 'Strong Sell'):
            Strong_Sell.append(symbol)
   
    Result = {'Strong_Buy':Strong_Buy,'Buy':Buy,'Hold':Hold,'Sell':Sell,'Strong_Sell':Strong_Sell}
    return Result
    
# Returns the market rank info for the given symbols
def Market_Rank_Info(symbols, info_map):
    Strong_Buy=[]
    Buy=[]
    Hold=[]
    Sell=[]
    Strong_Sell=[]
    for symbol in symbols:
        zacks_info = info_map[symbol]
        Rank = Zacks_Ranking(symbol, zacks_info)
        if(Rank == 'Strong Buy'):
            Strong_Buy.append(symbol)
        elif(Rank == 'Buy'):
            Buy.append(symbol)
        elif(Rank == 'Hold'):
            Hold.append(symbol)
        elif(Rank == 'Sell'):
            Sell.append(symbol)
        elif(Rank == 'Strong Sell'):
            Strong_Sell.append(symbol)
   
    Result = {'Strong_Buy':Strong_Buy,'Buy':Buy,'Hold':Hold,'Sell':Sell,'Strong_Sell':Strong_Sell}
    return Result
