#####################################################################
#
# FileName : CommonUtilities
#
# Usage : Basic utility functions for use by any module.
#
#####################################################################

import os
import smtplib

# Check that a file path exists
def PathExists(path):
    result = os.path.exists(path)
    if not result:
        print('Could not find path:'+ path)
    return result
    
# Compare two lists, return any new symbols that are in curr that were not in prev.
def CompareLists(prev, curr):
    new_symbols = []
    for symbol_curr in curr:
        if not symbol_curr in prev:
            new_symbols.append(symbol_curr)
    return new_symbols
