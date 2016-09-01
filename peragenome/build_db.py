"""
Peragenome - build_db.py
Created by: Angus Hilts
August 18, 2016

Summary:
    Functions for recursively finding .faa files and adding them to the database.
    This will save the relative file locations and create the db files, which will
    contain metadata used by Peragenome.
"""

import os
import sys
import glob
import time
import logging
import csv_handler as csv

###################
# Variables
###################
faa_files = {}      # Store faa filename and path

# find_files: string dict bool ->
# Description:
#   Searches for files with file_ext for the extension, then stores their path in storage
#   using the files name as the key, without its extension.
#   Recursive option will look through the tree recursively
#   NOTE: The extension should inlucde the '.' (I considered this more intuitive)
# Side effects:
#   storage will be modified
def find_files(file_ext, storage, recursive_opt, path):
    if recursive_opt:
        # Recursively walk the directory tree
        for root, dirnames, filenames in os.walk(root_dir):
            # Check for files with the '.faa' extension
            for f in fnmatch.filter(filenames, ("*%s"%file_ext)):
                pathname = os.path.join(root, f)
                print "Found %s" % pathname
                filename = get_filename(f)
                storage[filename] = pathname
    else:
        # Use a glob pattern to find files in the working directory
        # (i.e. current directory unless otherwise specified
        for f in glob.glob("%s/*%s" % ( path, file_ext)):
            print "Found %s" % f
            filename = get_filename(f)
            storage[filename] = f

# create_db: string string ->
# Description:
#   Creates files relevant to the database at the location specified by root_dir.
#   These files include .pfs.dat file which will hold info needed by the program, such as
#   paths to the other key db files, and a .csv file which will eventually hold the meta
#   data along with path info for each of the metagenomes in the database.
# Side effects:
#   Files will be made at the specified directory
def create_db(fs_root_dir, name):

    if not os.path.exists( os.path.abspath(fs_root_dir) ):
        print "The specified path for the FS was not found. Are you sure it was correctly specified?"
        return(1)

    # Generate name for the .pfs (pfs = Peragenome FileSystem)
    dat_filename = "%s.pfs.dat" % name
    dat_path = "%s/%s" % (fs_root_dir, dat_filename)
    dat_abs_path = os.path.abspath(dat_path)    # Converts the path to absolute path if it is not
                                                # one already

    # Do the same thing for the csv file
    csv_filename = "%s.pfs.csv" % name
    csv_path = "%s/%s" % (fs_root_dir, csv_filename)
    csv_abs_path = os.path.abspath(csv_path)


    with open(dat_abs_path, 'w+') as dat_file, open(csv_abs_path, 'w+') as csv_file:
        # Write the fs info to the dat file
        dat_file.write("name=\"%s\"\n" % name )
        dat_file.write("created=\"%s\"\n" % time.strftime("%Y-%m-%d") )
        dat_file.write("fs_root=\"%s\"\n" % os.path.abspath(fs_root_dir) )
        dat_file.write("fs_dat=\"%s\"\n" % dat_abs_path )
        dat_file.write("fs_csv=\"%s\"\n" % csv_abs_path )

    return "Done"

# populate_db: String ->
def populate_db(fs_dat_file):

    with open(fs_dat_file, 'r') as dat_file:
        csv_path = get_dat_field("fs_csv", dat_file)
        if csv_path == "Field not found":
            return csv_path

    with open(csv_path, 'w+') as csv_file:
        csv_file.write("test")

# get_dat_field: String -> String
# Summary:
#   Returns the value for field in dat_file. dat_file should be of the format
#   field_name=value. In this case, value is returned
def get_dat_field(field, dat_file):
    result = ""
    try:
        for line in dat_file:
            if line.split("=")[0] == field:
                result = line.split("=")[1]
                result = result.split("\n")[0]
                result = result.split("\"")[1]
                return result
        raise LookupError("field not found")
    except LookupError as err:
            err.args += (field, dat_file,)
            logging.warning( "get_dat_field: " + err[0] )
            logging.warning( "The value was not read from the file" )

