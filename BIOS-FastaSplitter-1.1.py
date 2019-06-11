#!/usr/bin/env python

# BIOS Fasta Splitter Script
# Developped by Leonardo Camargo Forero, M.Sc
# 2013
import os, sys

def splitFasta (seqFile, numSeq):

        current_file_index = 0
        count_seq = 0
        numSeq = int(numSeq)
        numSeq += 1

        ### Open First File #############################

        file_name = seqFile+".%d" % current_file_index
        file_path = os.path.join(temp_directory, file_name)
        current_file = open(file_path, "w")

        #################################################

        for line in open(seqFile):
                if line[0] == '>' :
                        count_seq += 1
                if count_seq == numSeq :
                        current_file_index += 1
                        file_name = seqFile+".%d" % current_file_index
                        file_path = os.path.join(temp_directory, file_name)
                        current_file = open(file_path, "w")
                        count_seq=0
                current_file.write(line)

if __name__ == "__main__":
        
	temp_directory =os.getcwd()
        input_file = sys.argv[1]
        seq_number = sys.argv[2]
        print("Starting Fasta File Splitting .... ")
	print("by Number of sequences "+seq_number)
	splitFasta(input_file,seq_number)
        print "Done :D"


