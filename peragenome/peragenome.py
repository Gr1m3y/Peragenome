#!/usr/bin/env python3

"""
Peragenome
Created By: Angus Hilts
Created: 2017-01-05

A tool for running hmms against many fasta files as well as mapping names to the resulting
files.

Module Summary:
    Interface module for handling input and piping any parameters to the correct program.
Programs:
    hmm         -   Run multiple HMMs against multiple FASTA files
    map_seqnm   -   Generate seq names by mapping the file name using a mapping file
    map_fnm     -   Map fasta file names using a mapping file
    map_seqlst  -   Map sequence names using mapping file
NOTE: See individual files for more detailed information
"""

import getopt
import sys
import hmm
import error
import lib
import map_seqnm
import usage

# Dictionaries to store individual program constructors and their main running program.
prog_ctor = {"hmm":hmm.hmm, "map_seqnm":map_seqnm.map_seqnm}
prog_main = {"hmm":hmm.hmm.main, "map_seqnm":map_seqnm.map_seqnm.main}

###################
# MAIN
###################

def main(argv):
   arg_string = "h"
   arg_list = ["help"]

   # Make sure a command was supplied
   if len(argv) <= 1:
      usage.peragenome()
      sys.exit(2)

   # Get the name of the program for use
   prog_name = sys.argv[1]

   if (prog_name not in prog_ctor) or (prog_name not in prog_main):
      # Pogram is not found in the dictionaries, so cannot be run
      usage()
   else:
      # Create the application object then run its main method
      try:
         prog_inst = prog_ctor[prog_name](argv)
         prog_main[prog_name](prog_inst)
      except(error.usageException):
         sys.exit(2)
      except(KeyboardInterrupt):
         print()
      except(error.badArgument):
         print("Incorrect arg")


if __name__ == "__main__":
   main(sys.argv[1:])
