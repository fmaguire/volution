#!/usr/bin/env python3

import sys
import os
import re
from tqdm import tqdm
from Bio import SeqIO

import argparse

def main(args):

    if len(args) is not 3:
        print("get_seqs.py SORTED_tmhmm_output_filepath SORTED_input_fasta_filepath")

    tmhmm_out_fh = open(args[1], 'rU')
    input_seq_fh = open(args[2], 'rU')
    output_file = open(args[3], 'rU')

    input_seqs = SeqIO.parse(input_seq_fh, "fasta")

    # get first record
    seq_record = input_seqs.__next__()

    for pred_line in tqdm(tmhmm_out_fh.readlines()):

        pred_line = pred_line.split()

        # skip sequences until they match the tmhmm accession
        # both files must be sorted
        # sort <tmhmm.out >tmhmm_sorted.out
        # paste - - <fasta | sort > sed 's/\t/\r/' >fasta_sorted
        skip_count = 0
        while not seq_record.description[:len(pred_line[0])] == pred_line[0]:
            seq_record = input_seqs.__next__()
            skip_count += 1
            if skip_count > 50:
                print("skipped more than 50 for ", pred_line[0])

        # example tmhmm output:
        #sp|Q6LZY8|RCE1_METMP	len=271	ExpAA=168.92	First60=43.93	PredHel=8	Topology=i11-33o38-60i80-102o122-144i157-179o192-214i219-241o245-261i


        if int(pred_line[4].split('=')[1]) > 0:

            # parse data fron topo info in tmhmm output
            topology = pred_line[-1].split('=')[-1]

            n = 0
            for indices in re.finditer("(?=(([i,o])(\d+)-(\d+)([i,o])))",
                                     topology):

                match = indices.groups()
                tm_orientation = match[1] + match[-1]
                tm_seq_indices = [int(match[2]) - 1 - 3,
                                  int(match[3]) - 1 + 3]


                if tm_seq_indices[0] < 0:
                    tm_seq_indices[0] = 0

                try:
                    tm_seq = str(seq_record.seq[tm_seq_indices[0]: tm_seq_indices[1]])
                except IndexError:
                    print(seq_record)
                    print("Too short")
                    tm_seq = str(seq_record.seq[tm_seq_indices[0]:])




                if len(seq_record.seq)==0:
                    print("No seq length")

                # reverse oi sequences to io to minimise topologies
                if tm_orientation == 'oi':
                    tm_seq = tm_seq[::-1]
                    tm_orientation = 'io'

                if tm_orientation == 'oo' or tm_orientation == 'ii':
                    print("Error weird orientation")
                    sys.exit(1)
                    #weird_output_file.write(">" + seq_record.description + '_' + str(n) + '\n')
                    #weird_output_file.write(tm_seq + '\n')
                    #next()



                output_file.write(">" + seq_record.description + '_' + str(n) + '\n')
                output_file.write(tm_seq + '\n')

                n+=1

    tmhmm_out_fh.close()
    input_seq_fh.close()

    output_file.close()

if __name__=='__main__':

    main(sys.argv)
