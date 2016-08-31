"""
Peragenome - csv_handler.py
Created by: Angus Hilts
August 29, 2016

Summary:
    A handler for dealing with and manipulating the csv files. Display, insert, delete, etc. should all be
    included in this module.
"""

import logging
import sys

# get_nth_field: int string -> string
# Summary:
#   Finds the nth field in a one line string where fields are comma delimited
def get_nth_field(n, row):
    try:
        return row.split(",")[n]
    except IndexError as err:
        err.args += (n, row,)
        logging.error('get_nth_field: Index out of bounds')
        logging.error(err)
# get_nth_row: int file -> string
# Summary:
#   Finds the nth row in a .csv file and returns it as a string
def get_nth_row(n, csv_file):
    try:
        for i, line in enumerate(csv_file):
            if i == n:
                return line
    except IndexError as err:
        err.args += (n,csv_file,)
        logging.error('get_nth_row: Line out of bounds')
        logging.error(err)
    except:
        logging.error('get_nth_row: Unknown error')
        logging.error( sys.exc_info()[0])

# find_row: string file [int] -> string
# Summary:
#   Finds a row in a .csv file based on the identifier given. By default,
#   the first column is searched through for the identifier. The entire
#   row is returned as a string
def find_row(identifier, csv_file, column=0):
    try:
        for i, line in enumerate(csv_file):
            if identifier == get_nth_field(column, line):
                return line
        return "Row not found"
    except:
        logging.error('find_row: Unknown error')
        logging.error( sys.exc_info()[0] )

# get_nth_col: int file -> listOfString
# Summary:
#   Returns the nth field of all rows from a .csv file (i.e. the entire
#   column)
def get_nth_col(n, csv_file):
    result = []
    try:
        for i, line in enumerate(csv_file):
            result.append( get_nth_field(n, line) )
        return result
    except:
        logging.error('get_nth_col: Unknown error')
        logging.error( sys.exc_info()[0] )

# get_col_name: int file -> string
# Summary:
#   Gets the name of the nth column in the .csv file. The first row is
#   assumed to be the titles row.
def get_col_name(n, csv_file):
    try:
        return get_nth_field( n, csv_file.readline() )
    except:
        logging.error( 'get_col_name: Unknown error' )
        logging.error( sys.exc_info()[0] )

def edit_field_by_posn( row, col, value, csv_file ):
    try:
        # read the files lines into a variable
        file_lines = csv_file.readlines()
        csv_file.seek(0)    # reset the read cursor to prevent errors in subesequent
                            # functions
        # read the old row into a list
        new_row = get_nth_row( row, csv_file ).rstrip().split(",")
        # update the row
        print new_row
        new_row[col] = value
        print new_row
        # update the file lines with the new row
        # Note: new_row is a list, needs to be joined with commas
        file_lines[row] = ','.join(new_row).append("\n")
        print file_lines[row]

        csv_file.seek(0)
        csv_file.write( file_lines )
    except:
        logging.error( 'edit_field_by_posn: Unknown error' )
        logging.error( sys.exc_info()[0] )
