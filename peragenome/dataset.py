# dataset.py
# Class for storing and updating information for a dataset

# Operations:
#   insert()    -   insert a new row
#   delete()    -   delete a row
#   get_row()   -   return a row
#   delete_df() -   delete the dataframe (DANGEROUS)

import pandas
import logging
import os
import flib

# Constants
FILE_PATH_HEADER = "file_path"  # Default header for filepaths

class Dataset:
    ####################
    # Class Functions  #
    ####################

    def __init__(self, name, csv, modified="1969-12-31", titles=[]):
        # Initialize dataframe to None
        self.data_frame = None
        # Set the variables
        self.name = name
        self.csv = csv
        self.modified = modified
        # Add file_path to the titles for the tables
        self.titles = titles
        self.titles.insert(0, FILE_PATH_HEADER) # Push the column for file
                                                # paths on. We don't trust the
                                                # user to do this...


    def create_dataframe(self, file_ext, root_path=".", recursive=False):
        if self.df:
            logging.warning("Dataset.create_dataframe: Dataframe already exists")
            return
            # TODO user proper exception above
        else:
            # Find all of the correct files
            file_paths = find_files(file_ext, root_path, recursive)
            self.data_frame = pandas.DataFrame( {FILE_PATH_HEADER:file_paths}
                                                columns=self.titles)

    def save_dataframe(self):
        self.data_frame.to_csv(path_or_buf=self.csv)

    def load_dataframe(self):
        try:
            if not self.data_frame:
                self.data_frame = pandas.read_csv(self.csv, index_col=0)
            else:
                # TODO Use better exception here
                logging.error( "Dataset.data_frame: Dataframe is already loaded" )

    ####################
    # Operations       #
    ####################

