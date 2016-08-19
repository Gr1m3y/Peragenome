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

###################
# Variables
###################
faa_files = {}      # Store faa filename and path

# find_files: string dict bool ->
# Description:
#   Searches for files with file_ext for the extension, then stores their path in storage
#   using the files name as the key, without its extension.
#   Recursive option will look through the tree recursively
#   NOTE: The extension should inlucde the '.'
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

# create_db string string -> 
# Description:
#   Creates files relevant to the database at the location specified by root_dir.
#   These files include .pfs.dat file which will hold info needed by the program, such as
#   paths to the other key db files, and a .csv file which will eventually hold the meta
#   data along with path info for each of the metagenomes in the database.
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

    dat_file = open(dat_abs_path, 'w+')
    csv_file = open(csv_abs_path,  'w+')


    # Write the fs info to the dat file
    dat_file.write("fs_root=\"%s\"\n" % os.path.abspath(fs_root_dir) )
    dat_file.write("fs_dat=\"%s\"\n" % dat_abs_path )
    dat_file.write("fs_csv=\"%s\"\n" % csv_abs_path )


    dat_file.close()
    csv_file.close()


    return "Done"
