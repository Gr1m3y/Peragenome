"""
Peragenome
Created By: Angus Hilts
Created: 2017-01-05

Module containing usage functions for peragenome programs.
"""

import lib

def peragenome():
   print("NAME")
   print("\tPeragenome -- Suite of tools for working with multiple HMMs and sequence files")
   print("\nSYNOPSIS")
   print("\tperag [-h] ["  + lib.colour.UNDERLINE + "program_name" + lib.colour.END + "] [" + lib.colour.UNDERLINE + "program_options"
      + lib.colour.END + "]")
   print("\nDESCRIPTION")
   print("\tPeragenome is a suite...")
   print("\nThe following options are available:")
   print("\n\t-h\tPrints the manual pages")
   print("\nEXAMPLES")
   print("\tperag hmm -m model_directory -f fasta_directory -o output_directory")
   print("")

def hmm():
   print("NAME")
   print("\tPeragenome: hmm -- pairwise searching of HMMs against FASTA files")
   print()
   print("SYNOPSIS")
   print("\tperag hmm [-hr] [-e <x>] [-o " + lib.colour.UNDERLINE 
      + "output_directory" + lib.colour.END + "] -f " + lib.colour.UNDERLINE 
      + "fasta_directory" + lib.colour.END + " -m " + lib.colour.UNDERLINE 
      + "hmm_directory" + lib.colour.END + "\n")
   print("DESCRIPTION")
   print("\tIdentifies HMM files and FASTA files in the appropriate input directories, then runs all HMMs in ")
   print("\ta pairwise fashion using hmmer. Resulting hmmer output, seqnm, and fasta files are created in new ")
   print("\tdirectories.\n")
   print("\tThe following options are available:")
   print()
   print("\t-h\tPrints help info\n")
   print("\t-r\tSearch the FASTA input directory recursively\n")
   print("\t-o\tOptional output directory, default is the present working directory (see pwd(1))\n")
   print("\t-f\tSpecifies the directory to be searched for FASTA files, default uses .faa extension\n")
   print("\t-m\tSpecifies the directory to be searched for HMM model files, default uses .hmm extension\n")
   print("\t-e <x>\tSpecifies the e-value cutoff to be used by hmmer. x can be specifed as an integer, decimal")
   print("\t\tor using scientifig notation (e.g. 1.2, 3e-10, etc.)\n")
   print("EXAMPLES")
   print("\tperag hmm -e 2e-25 -o output_directory -f fasta_directory -m model_directory\n")

def map_seqnm():
   print("NAME")
   print("\tPeragenome: map_seqnm -- sequence renaming based on file name and mapping file\n")
   print("SYNOPSIS")
   print("\tperag map_seqnm [-h] [-m] [-d] [-r] -i " + lib.colour.UNDERLINE + "input_directory" + lib.colour.END)
   print("DESCRIPTION")

   print("\tTakes a folder containing FASTA files and a mapping file which contains the following entries: ")
   print("\t\tfilename1 -> filename2")
   print("\tSequence names contained in the file filename1 are replaced with filename2|n where n is an ")
   print("\tindex.")
    
   print("\n\tExample:")
   print("\tIn id_000123.faa:")
   print("\t\t>seq_1")
   print("\t\tATTCTCGTGCATGCATGCTACGTACGCGGCAAATATCTCATCA")
   print("\t\t>seq_46")
   print("\t\tATCTGCTACTGCTGCATGCTATTTACTCGCGACTCTACGACTG")
   print("\tIn map_file.csv:")
   print("\t\tname1,name2")
   print("\t\tid_000123.faa,soil_sample")
    
   print("\n\tThe above input results in the following output:")
   print("\tIn id_000123_new.faa:")
   print("\t\t>soil_sample|1")
   print("\t\tATTCTCGTGCATGCATGCTACGTACGCGGCAAATATCTCATCA")
   print("\t\t>soil_sample|2")
   print("\t\tATCTGCTACTGCTGCATGCTATTTACTCGCGACTCTACGACTG")

   print("\nThe following options are available:")
   print()
   print("\t-h\tPrints help info\n")
   print("\t-m\tSpecify a mapping file other than the default\n")
   print("\t-d\tSpecify the domain column for mapping function\n")
   print("\t-r\tSpecify the range column for mapping function\n")
   print("\t-i\tSpecify the input directory, containing the FASTA files\n")
   print("EXAMPLES")
   print("\tperag map_seqnm -i fasta_directory\n")






