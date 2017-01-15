"""
lib.py
Created By: Angus Hilts
Created: 2017-01-11

Module Summary:
   Some library functions for use throughout the program.
"""

import os
import glob
import fnmatch

# shell_quote: string -> string
# Description:
#   Returns the strin in a "shell-ready" format to prevent things like whitespace from
#   interfering with commands
# NOTE: This is really good to use before making bash calls
def shell_quotes(s):
    return "'" + s.replace("'", "'\\'") + "'"

# get_filename: string -> string
# Description
#   Returns the filename of f with all extensions removed (makes code a little more
#   readable in my humble opinion)
def get_filename(f):
    # Get rid of the path leading to the file
    fname = f.split("/")[-1]
    # Get rid of the extension and return
    return fname.split(".")[0]

# find_files: string string string -> dict
# Description:
#     Finds files with the fiven extension (. must be included) then returns a dictionary
#     with the filenames and their absolute paths
def find_files(dir, ext, recursive):
   print("Searching " + dir)
   files = {}
   # If recursive option is specified, walk the directory tree and look for the FASTA files
   if recursive:
      for root, dirnames, filenames in os.walk(dir):
         #Filter the files for the correct extension
         for f in fnmatch.filter(filenames, ("*%s" % ext)):
            # Get the path for the file
            pathname = os.path.join(root, f)
            print("Found %s" % pathname)
            # Strip the path down to only the files's name
            filename = get_filename(f)
            # Finally, throw it into a dictionary
            files[filename] = os.path.abspath(f)
   else:
      # Use glob pattern to find files in the working directory
      # (i.e. current directory, unless otherwise specified)
      print(glob.glob("%s/*%s" % (dir, ext)))
      for f in glob.glob("%s/*%s" % (dir, ext) ):
         print("Found %s" % f)
         filename = get_filename(f)
         files[filename] = f

   return files

# For string formatting
# Example:
#  print(colour.BOLD + "Hello, world!" + colour.END)
class colour:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'\


