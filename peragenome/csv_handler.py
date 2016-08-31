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
        csv_file.seek(0)
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
        csv_file.seek(0)
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
        csv_file.seek(0)
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
        csv_file.seek(0)
        return get_nth_field( n, csv_file.readline() )
    except:
        logging.error( 'get_col_name: Unknown error' )
        logging.error( sys.exc_info()[0] )

# get_col_num: string string -> int
# Summary:
#   Returns the number of the field corresponding to title
#   If title is not found, returns -1
def get_col_num(title, row):
    try:
        fields = row.rstrip().split(",")
        # iterate through the fields
        for i, f in enumerate(fields):
            if f == title:
                return i
        return -1
    except:
        logging.error("get_col_num: Unknown error")
        logging.error( sys.exc_info()[0] )

# edit_field_by_posn: int int string file ->
# Summary:
#   Edits the field corresponding to row,col in the csv file.
# Side Effects:
#   .csv file will be modified permanently
def edit_field_by_posn( row, col, value, csv_file ):
    try:
        csv_file.seek(0)
        # read the files lines into a variable
        file_lines = csv_file.readlines()
        csv_file.seek(0)    # reset the read cursor to prevent errors in subesequent
                            # functions
        # read the old row into a list
        new_row = get_nth_row( row, csv_file ).rstrip().split(",")
        # update the row

        new_row[col] = value

        new_row = ','.join(new_row) + '\n'

        # update the file lines with the new row
        # Note: new_row is a list, needs to be joined with commas
        file_lines[row] = new_row

        # reset the cursor
        csv_file.seek(0)
        # write the new data to the file
        csv_file.writelines( file_lines )
        # remove any trailing unexpected data
        csv_file.truncate()

    except:
        logging.error( 'edit_field_by_posn: Unknown error' )
        logging.error( sys.exc_info()[0] )

# has_null_field: string -> int
# Summary:
#   Returns an int indicating which field is null if one is found,
#   otherwise returns -1
def has_null_field(row):
    try:
        fields = row.split(",")
        for i, f in enumerate(fields):
            if f == '':
                return i
        return -1
    except:
        logging.error( 'has_null_field: Unknown error' )
        logging.error( sys.exc_info()[0] )

def add_column(title, csv_file):
    try:
        csv_file.seek(0)
        # Read the files lines into memory
        file_lines = csv_file.readlines()
        csv_file.seek(0)        # reset the cursor

        # Add cell for the new field to each row
        for i, line in enumerate(file_lines):
            print "old line is: " + line
            file_lines[i] = line.rstrip() + ",\n"
            print "new line is: " + line

        print file_lines[0]

        title_fields = file_lines[0].rstrip().split(",")    # Fetch the title line into a list
        title_fields[-1] = title                            # Insert title into the title row

        print title_fields

        # Update the title row in memory
        title_row = ','.join(title_fields) + '\n'
        file_lines[0] = title_row

        csv_file.seek(0)    # reset the cursor

        csv_file.writelines( file_lines )
        csv_file.truncate() # truncate the girl and wipe away the debt.

    except IndexError as in_err:
        in_err.args += (title, csv_file)
        logging.error("add_column: Indexing error occurred")
        logging.error(in_err)
    except:
        logging.error("add_column: Unknown error")
        logging.error( sys.exc_info()[0] )

# title_exists: string string -> bool
# Summary:
#   Returns true if the string title is found in a field in row
def title_exists(title, row):
    try:
        fields = row.split()
        for f in fields:
            if f == title:
                return True
        return False
    except:
        logging.error("title_exists: Unknown error")
        logging.error( sys.exc_info()[0] )

# swap_columns_by_num: int int file -> 
# Summary:
#   Swaps all values in the columns corresponding to col1 and col2
# Side effects:
#   csv_file is permanently modified
def swap_columns_by_num(col1, col2, csv_file):
    try:
        # Reset the cursor, just in case ;)
        csv_file.seek(0)

        file_lines = csv_file.readlines()

        # iterate over all lines in the file
        for i, line in enumerate(file_lines):
            fields = line.rstrip().split(",")
            # swap the values for the corresponding fields
            fields[col1], fields[col2] = fields[col2], fields[col1]
            new_line = ",".join(fields) + '\n'
            file_lines[i] = new_line    # update the line in the file

        csv_file.seek(0)
        csv_file.writelines( file_lines )
        csv_file.truncate()

    except:
        logging.error("swap_columns_by_num: Unknown error")
        logging.error( sys.exc_info()[0] )

# swap_columns_by_title: string string file ->
# Summary:
#   Finds the correct columns for title1 and title2 then swaps all
#   values
# Side effects:
#   csv_file is permanently modified
def swap_columns_by_title(title1, title2, csv_file):
    try:
        csv_file.seek(0)    # Reset cursor just in case

        title_row = csv_file.readline()

        print title_row

        col1 = get_col_num(title1, title_row)
        print col1
        col2 = get_col_num(title2, title_row)
        print col2
        swap_columns_by_num(col1, col2, csv_file)

    except:
        logging.error("swap_columns_by_title: Unknown error")
        logging.error( sys.exc_info()[0] )
