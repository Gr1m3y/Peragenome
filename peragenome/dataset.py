"""
Peragenome - dataset.py
Created by: Angus Hilts
September 7, 2016

Summary:
    Class for loading and handling. This allows the information to be 
    loaded once, then quickly accessed later. It also makes editing and 
    individual. 
"""

import csv
import logging
import sys

class Dataset:
    files = {}      # Key is the primary key when built from the CSV,
                    # value is a list containing the fields from the csv
                    # for that row

    # TODO: I think that enumerating the fields may be most useful for accessing them...

    def __init__( self, name="", root="", csv="", n=0, modified="1969-12-31",
                  created="1969-12-31", primary="" ):
        self.root = root
        self.csv = csv_path
        self.num_files = n
        self.created = create_date
        self.modified = mod_date
        self.primary = primary
        self.titles = []
        # Return the assigned values as a dictionary
        return self.info()

    def save(self):
        # TODO: Add the stuff for saving all the data to the csv file
        return info()

    def load(self):
        with open(csv) as csv_file:
            title_line = csv_file.getline() # Load first line of csv
                                            # for getting titles



    # for now this will use the primary key, I will eventually add filters to sort by attributes
    def get_row(self, key):
        # I do not think I should raise any errors here, let the KeyError be passed up to later
        # handling
        return files[key]

    def add_row():



    # return dict of key, value pairs for each variable to be saved in the dat file
    def info():
        return {
                    "root":self.root,
                    "csv":self.csv,
                    "name":self.name,
                    "modified":self.modified,
                    "created":self.created,
                    "primary":self.primary
                }

    def display(self):
