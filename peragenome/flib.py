# flib
# Library of useful functions for dealing with the directory and files

import logging
import sys
import os

# find_files: String String Bool -> List(String)
# Summary:
#   Find all files at path ending with file_ext. If recursive is true, then
#   recursively searches in any directories found
# NOTE: Paths to files returned are specified as relative from the calling
#   location
def find_files(file_ext, root=".", recursive=False):
    found_files = []    # list of files found
    # Iterate through the directory starting at root
    for path, dirs, files in os.walk(root):
        # Check recursive option
        if not recursive:
            # Remove dirs from search space
            while len(dirs) > 0:
                dirs.pop()
        # Iterate over found files
        for f in files:
            if f.endswith(file_ext):
                found_files.append( os.path.join(path, f) )

    return found_files
