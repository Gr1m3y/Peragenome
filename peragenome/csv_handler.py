"""
Peragenome - csv_handler.py
Created by: Angus Hilts
August 29, 2016

Summary:
    A handler for dealing with and manipulating the csv files. Display,
    insert, delete, etc. should all be included in this module.

Interface Description:
    get_nth_field: int string -> int
    get_nth_row: int file -> string
    find_row: string file [int] -> string
    get_nth_col: int file -> listOfString
    get_col_name: int file -> string
    get_col_num: string string -> int
    edit_field_by_posn: int int string file ->
    has_null_field: string -> int
    get_row_by_key: string, string file -> string
"""
# TODO List
# - Add proper delete functions

import logging
import sys

# get_nth_field: int string -> string
# Summary:
#   Finds the nth field in a one line string where fields are comma 
#   delimited
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

# get_row_by_key: string, string file -> string
# Summary:
#   Finds the row with the given key_value specifed, under the
#   primary_name heading
def get_row_by_key(primary_name, key_value, csv_file):
    try:
        csv_file.seek(0)    # Reset the cursor
        title_string = csv_file.getline().split("\n")[0]
        title_row = title_string.split(",") # split row into list

        # Find the correct column to use as the primary key
        for i, title in enumerate(title_row):
            if title == primary_name:
                col_index = i

        return find_row(key_value, csv_file, i) # TODO: fix error stuff here by updating find_row

# find_row: string file [int] -> string
# Summary:
#   Finds a row in a .csv file based on the identifier given. By
#   default, the first column is searched through for the identifier. 
#   The entire row is returned as a string
def find_row(identifier, csv_file, column=0):
    try:
        csv_file.seek(0)
        for i, line in enumerate(csv_file):
            if identifier == get_nth_field(column, line):
                return line
        return "Row not found" # TODO: This should probably raise an exception
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
        csv_file.seek(0)    # reset the read cursor to prevent errors 
                            # in subesequent functions
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

        # Fetch the title line into a list
        title_fields = file_lines[0].rstrip().split(",")
        # Insert title into the title row
        title_fields[-1] = title

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

        # Get the column numbers for the passed in titles
        col1 = get_col_num(title1, title_row)
        col2 = get_col_num(title2, title_row)
        # Call swap_by_num
        swap_columns_by_num(col1, col2, csv_file)

    except:
        logging.error("swap_columns_by_title: Unknown error")
        logging.error( sys.exc_info()[0] )

# create_new_table: string int listOfString -> 
# Summary:
#   Creates a new csv file called filename.csv with ncol number of 
#   columns. If specified, titles will be inserted for the first row.
# Constraints:
#   - ncol >= len(titles)
#   - ncol >= 0
# Side Effects:
#   New file created in the present working director (at runtime)
# NOTE: If the number of titles does not match ncol, then any remaining 
#   columns will be left blank
def create_new_table( filename, ncol, titles=[] ):
    filename_ext = filename + ".csv"

    try:
        # Check that the arguments are following constraints
        if ncol < 0:
            raise ValueError("ncol was negative")
        elif len(titles) > ncol:
            raise ValueError("len(titles) was greater than ncol")

        # Open and create the file
        with open(filename_ext, 'w+') as new_csv:
            header = "," * (ncol-1)
            # Check if the input contained defined titles
            if titles != []:
                fields = header.split(",")

                # Iterate over titles passed as arguments and set the 
                # correct fields
                for i, name in enumerate(titles):
                    fields[i] = name
                header = ",".join(fields)   # join the titles as a 
                                            # single string

            new_csv.seek(0) # set the cursor just in case
            new_csv.write(header)

    except ValueError as err:
        # log details for a bad call to the function
        err.args += (filename, ncol, titles,)
        logging.warning("create_new_table: " + err[0] )
        logging.warning("File not created")
        logging.warning(err[1:])
    except:
        logging.error("create_new_table: Unknown error")
        logging.error( sys.exc_info()[:2] )

# get_table_dimensions: file -> (int, int)
# Summary:
#   Returns a tuple containing the dimensions of the table stored in csv_file
# NOTE: The number of columns returned will always be at least 1 since an empty file
#   is equivalent to a single column table with 0 rows.
def get_table_dimensions(csv_file):
    try:
        csv_file.seek(0)        # reset the cursor

        # get the number of columns
        line = csv_file.readline()
        cols = len( line.split(",") )   # split first line into columns and count them

        csv_file.seek(0)        # reset the cursor
        i = -1                  # initialize i to account for the possibility that the file is empty
        # iterate over the file to count the lines to get number of rows
        for i, line in enumerate(csv_file):
                pass
        rows = i+1

        return rows, cols

    except:
        logging.error("get_table_dimensions: Unknown error")
        logging.error( sys.exc_info()[:2] )

# find_next_null: int int file -> (int, int)
# Summary:
#   Searches the CSV file from the position specified by row, col (inclusive)
#   until an empty value is found.
# Constraints:
#   - row > 0
#   - col > 0
#   - row < get_table_dimensions(csv_file)[0]
#   - col < get_table_dimensions(csv_file)[1]
# NOTE: Returns the tuple (-1,-1) if no NULLS are found
def find_next_null(row, col, csv_file):
    try:
        # Get the dimensions of the table
        row_dim, col_dim = get_table_dimensions(csv_file)

        # Check the constraints
        if row >= row_dim or col >= col_dim:
            raise ValueError("dimensions out of bounds")


        csv_file.seek(0)
        csv_rows = csv_file.readlines()

        # iterate over lines starting from the row specified
        for line in csv_rows[row:]:
            fields = line.rstrip().split(",")

            # iterate over the fields for the current row
            for field in fields[col:]:
                if field == '':
                    return row, col
                col += 1   # increment the col

            row += 1   # increment the row
            col = 0 # reset the col number
        return (-1,-1)

    # TODO: Should this really be an exception? Or should this just count as
    # "no next null found"?
    except ValueError as err:
        err.args += (row, col, csv_file,)
        logging.warning("find_next_null: " + err[0])
        logging.warning("Could not search outside table")
    except:
        logging.error("find_next_null: Unknown error")
        logging.error( sys.exc_info()[:2] )

#TODO: Make this function
def get_row_list():
    return 0

# TODO: Make this function (returns 2d array of all fields)
def get_table():
    return 0
