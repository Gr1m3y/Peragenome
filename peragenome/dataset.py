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

    def __init__( self, name = "", root="", csv="", n=0, modified="1969-12-31",
                  created="1969-12-31" ):
        self.root = root
        self.csv = csv_path
        self.num_files = n
        self.created = create_date
        self.modified = mod_date

    def save(self):
        # TODO: Add the stuff for saving all the data to the csv file
        return info()

    def load(self):
        with open(csv):


    def get_row():

    def add_row():

    # return dict of key, value pairs for each variable to be saved in the dat file
    def info():
        return {
                    "root":self.root,
                    "csv":self.csv,
                    "name":self.name,
                    "modified":self.modified,
                    "created":self.created
                }

    def display(self):
