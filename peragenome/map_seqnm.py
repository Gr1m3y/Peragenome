"""
map_seqnm
Created by: Angus Hilts
Created: 2017-01-05

Module Summar:
    Takes a folder containing FASTA files and a mapping file which contains the following
    entries:
        filename1 -> filename2
    Sequence names contained in the file filename1 are replaced with filename2_n where n is
    an index.
    
    Example:
    In id_000123.faa:
        >seq_1
        ATTCTCGTGCATGCATGCTACGTACGCGGCAAATATCTCATCA
        >seq_46
        ATCTGCTACTGCTGCATGCTATTTACTCGCGACTCTACGACTG
    In map_file.csv:
        name1,name2
        id_000123.faa,soil_sample
    
    The above input results in the following output:
    In id_000123.faa:
        >soil_sample|1
        ATTCTCGTGCATGCATGCTACGTACGCGGCAAATATCTCATCA
        >soil_sample|2
        ATCTGCTACTGCTGCATGCTATTTACTCGCGACTCTACGACTG
"""

import csv
import sys
import os
import lib
import error
import getopt
import usage

arg_string = "hd:r:m:i:"
arg_list = ["help", "mapping-file=", "input=", "domain=", "range="]

# TODO: Put some of these values into a file for saving which can be set
class map_seqnm:
    def __init__(self, argv):
        self.mapping_file = "settings/img_taxonmap.csv"
        self.fasta_dir = ""
        self.domain = "taxon_oid"
        self.range = "taxon_name"
        self.fasta_ext = ".faa"
        self.recursive = True
        self.fasta_files = {}
        self.mapping = {}

        # Set the default mapping file to be the one in the install directory
        default_map = os.path.dirname(os.path.realpath(__file__))
        default_map = os.path.abspath(default_map)
        self.mapping_file = default_map + "/" + self.mapping_file

        # Parse arguments
        try:
            opts, args = getopt.getopt(argv[1:], arg_string, arg_list)
        except:
            usage.map_seqnm()
            raise error.usageException

        for opt, arg in opts:
            if opt in ["-h", "--help"]:
                usage.map_seqnm()
                sys.exit(0)
            elif opt in ["-m", "--mapping-file"]:
                self.mapping_file = arg
                print(self.mapping_file)
            elif opt in ["-i", "--input"]:
                self.fasta_dir = arg
            elif opt in ["-d", "--domain"]:
                self.domain = arg
            elif opt in ["-r", "--range"]:
                self.range = arg

    def create_mapping(self):
        # Open the mapping file and find the correct columns
        with open(self.mapping_file, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)

            domain_col = header.index(self.domain)
            range_col = header.index(self.range)

            for line in reader:
                domain_val = line[domain_col]
                range_val = line[range_col]
                self.mapping[domain_val] = range_val
            
    def rename_seqs(self):
        for fasta_name, fasta in self.fasta_files.items():

            new_file = fasta.split(".")[0]
            new_file = "%s_new%s" % (new_file, self.fasta_ext)

            if fasta_name in self.mapping:
                cmd = "awk '/^>/{print \">%s|\" ++i; next}{print}' < %s > %s" % (self.mapping[fasta_name],
                                                                       lib.shell_quotes(fasta), 
                                                                       lib.shell_quotes(new_file))
                print("Executing: %s" % cmd)
                os.system(cmd)
            else:
                print("No mapping with that name")


    def main(self):
        # Find the fasta files of interest
        self.fasta_files = lib.find_files(self.fasta_dir, self.fasta_ext, self.recursive)
        print(self.fasta_files)
        # Create a dictionary for faster mapping later on
        self.create_mapping()
        self.rename_seqs()

