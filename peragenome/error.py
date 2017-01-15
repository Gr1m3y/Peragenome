"""
HMM (Hammertime Version 4)
Created By: Angus Hilts
Created: 2017-01-05

Module Summary:
    Includes a few custom exceptions, that's all.
"""

class usageException(Exception):
   """Raise if usage function is called"""

class badArgument(Exception):
   """Raise if an argument is passed"""