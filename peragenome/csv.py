"""
Peragenome - csv.py
Created by: Angus Hilts
August 29, 2016

Summary:
    A handler for dealing with and manipulating the csv files. Display, insert, delete, etc. should all be
    included in this module.
"""

def get_nth_field(n, row):
    try:
        return row.split(",")[n]
    except IndexError:
        logging.error('get_nth_field: Index out of bounds')
