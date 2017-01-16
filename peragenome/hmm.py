"""
HMM (Hammertime Version 4)
Created By: Angus Hilts
Created: 2017-01-05

Module Summary:
    Identifies HMM files and FASTA files in the appropriate input destinations, then
    runs all HMMs in a pairwise fashion using hmmer. Resulting HMM files are created
    in a new directory.
Usage:
   peragenome hmm [-hr] [-t <x>] [-o output_directory] -f fasta_directory -m hmm_directory
Options:
   -h
"""

# Implementation Info:
#     - Add ability to specify new extensions with the -eE flags

import sys
import os
import getopt
import error
import lib

arg_string = "hrm:f::o:"
arg_list = ["help", "model-dir=", "fasta-dir=", "output=", "recursive"]

# hmm
# Summary:
#  Object for running HMM models against a fasta database
# Attributes:
#  fasta_dir      -  Directory for storing FASTA files
#  model_dir      -  Directory for storing HMM models
#  output_dir     -  Directory for sending the output to
#  recursive      -  True if recursive searches should be used, false otherwise
#  fasta_files    -  Dictionary with identified fasta files
#  model_files    -  Dictionary with identified model files
# Methods:
class hmm:
   # __init__(self, argv)
   # Parse arguments and set appropriate attribute values (defulat or user specified)
   def __init__(self, argv):
      self.argv = argv
      self.recursive = False
      self.threshold = 10.0
      self.fasta_ext = ".faa"
      self.model_ext = ".hmm"
      self.model_dir = ""
      self.fasta_dir = ""
      self.output_dir = os.getcwd() # default to the pwd
      self.fasta_files = {}
      self.model_files = {}

      if len(argv) <= 1:
         self.usage()
         raise error.usageException

      # Get arguments
      try:
         opts, args = getopt.getopt(argv[1:], arg_string, arg_list)
      except:
         self.usage()
         raise error.usageException

      # Parse the arguments
      for opt, arg in opts:
         if opt in ["-h", "--help"]:
            self.usage()
            sys.exit(0)
         
         # Sets the working directories
         elif opt in ["-m", "--model-dir"]:
            self.model_dir = os.path.abspath(arg)
            # Check that the directory exists
            if not os.path.isdir(self.model_dir):
               raise error.badArgument
         elif opt in ["-f", "--fasta-dir"]:
            self.fasta_dir = os.path.abspath(arg) 
            # Check that the directory exists
            if not os.path.isdir(self.fasta_dir):
               raise error.badArgument
         elif opt in ["-o", "--output"]:
            self.output_dir = arg
         
         # Other options
         elif opt in ["-r", "--recursive"]:
            self.recursive = True

      print(self.fasta_dir)
      print(self.model_dir)
      lib.continue_prompt()


   def usage(self):
      print("NAME")
      print("\tPeragenome: hmm -- search multiple fasta files with many HMMs")
      print()
      print("SYNOPSIS")
      print("\tperagenome hmm [-hr] [-t <x>] [-e <s>] [-o " + lib.colour.UNDERLINE 
         + "output_directory" + lib.colour.END + "] -f " + lib.colour.UNDERLINE 
         + "fasta_directory" + lib.colour.END + " -m " + lib.colour.UNDERLINE 
         + "hmm_directory" + lib.colour.END + "\n")
      print("DESCRIPTION")
      print("\tIdentifies HMM files and FASTA files in the appropriate input destinations, then")
      print("\truns all HMMs in a pairwise fashion using hmmer. Resulting HMM files are created")
      print("\tin a new directory.\n")
      print("\tThe following options are available:")
      print()
      print("\t-h\tPrints help info")

   # build_output_dir: ->
   # Summary:
   #  Creates output directories
   # Side Effects:
   #  New directores will be created in the pwd or specified output directory
   def build_output_dir(self):
      # Check if output dir was specified and set root
      root = self.output_dir
      # Create paths for new directories
      fasta_out_dir = os.path.abspath("%s/fasta_out" % root)
      seq_out_dir = os.path.abspath("%s/seq_out" % root)
      model_out_dir = os.path.abspath("%s/model_out" % root)

      # Create the directories if they do not already exist
      if not os.path.exists(fasta_out_dir):
         os.makedirs(fasta_out_dir)
      if not os.path.exists(seq_out_dir):
         os.makedirs(seq_out_dir)
      if not os.path.exists(model_out_dir):
         os.makedirs(model_out_dir)


   # TODO: Add a prompt for conflicts. It should be something like this:
   # File already exists. Overwrite?
   #  [Y]es - to overwrite
   #  [N]o  - to skip
   #  [A]ll - to supress this warning for future conflicts
   def model_search(self):

      # Iterate over the models
      for model_name, model in self.model_files.items():

         print(model_name)
         print(model)

         # Check for the model subdirectories
         model_out_dir = os.path.abspath("%s/model_out/%s" % (self.output_dir, model_name) )
         print(model_out_dir)
         # Check if the output directory exists. Create it if not
         if not os.path.exists(model_out_dir):
            os.makedirs(model_out_dir)
         for fasta_name, fasta in self.fasta_files.items():
            # run hmmsearch faa, hmm
            model_output = lib.shell_quotes( "%s/%s.out" % (model_out_dir, fasta_name) )
            fasta_input = lib.shell_quotes(fasta)
            model_input = lib.shell_quotes(model)
            
            cmd = "hmmsearch -E %s %s %s > %s" % (str(self.threshold), model_input, 
                                                  fasta_input, model_output)


            print("Executing: %s" % cmd)

            os.system(cmd)


   def get_seq_names(self, model_in, seq_out):
      for line in model_in:
         # Find lines starting with ">>" 
         if not line.isspace() and line.split()[0] == ">>":
            seq_out.write("%s\n" % line.split()[-1])


   def create_seq_files(self):
      for model_name, model in self.model_files.items():

         # Build the two paths
         model_out_dir = os.path.abspath( "%s/model_out/%s" % (self.output_dir, model_name) )
         seq_out_dir = os.path.abspath( "%s/seq_out/%s" % (self.output_dir, model_name) )

         # If the seq dir does not exist, create it
         if not os.path.exists(seq_out_dir):
            os.makedirs(seq_out_dir)

         for fasta_name, fasta in self.fasta_files.items():
            model_output = "%s/%s.out" % (model_out_dir, fasta_name)
            seq_output = "%s/%s.sqnm" % (seq_out_dir, fasta_name)

            with open(model_output, 'r') as m:
               with open(seq_output, 'w+') as s:
                  self.get_seq_names(m, s)


   def build_fasta_output(self):
      for model_name, model in self.model_files.items():
         # Build the two root paths again
         seq_out_dir = os.path.abspath( "%s/seq_out/%s" % (self.output_dir, model_name) )
         fasta_out_dir = os.path.abspath( "%s/fasta_out/%s" % (self.output_dir, model_name) )
         # Create output folder

         if not os.path.exists( fasta_out_dir ):
            os.makedirs( fasta_out_dir )

         for fasta_name, fasta in self.fasta_files.items():
            # Get file input and output paths and put them into a shell-friendly format
            seq_output = lib.shell_quotes( "%s/%s.sqnm" % (seq_out_dir, fasta_name) )
            fasta_output = lib.shell_quotes( "%s/%s.faa" % (fasta_out_dir, fasta_name) )
            fasta_input = lib.shell_quotes( fasta )

            # Create the command
            cmd = "pullseq -n %s -i %s > %s" % (seq_output, fasta_input, fasta_output)
            
            print("Executing: %s" % cmd)

            # And run it
            os.system(cmd)


   def main(self):
      # Find all the files
      # NOTE: I think model files should be non-recursive only maybe...
      self.model_files = lib.find_files(self.model_dir, self.model_ext, self.recursive)
      self.fasta_files = lib.find_files(self.fasta_dir, self.fasta_ext, self.recursive)
      self.build_output_dir()
      print(self.model_files)
      print(self.fasta_files)
      #self.model_search()
      #self.create_seq_files()
      #self.build_fasta_output()


