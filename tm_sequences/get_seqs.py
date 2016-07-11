#!/usr/bin/env python3

import sys
import os
from Bio import SeqIO


if __name__=='__main__':

    if len(sys.argv) is not 3:
        print("get_seqs.py tmhmm_output_filepath input_fasta_filepath")

    tmhmm_out_fh = open(sys.argv[1], 'rU')
    input_seq_fh = open(sys.argv[2], 'rU')

    output_name = os.basename(sys.argv[2])

    output_files = {'ii': open(output_name + 'ii_tm_seqs.fasta', 'w'),
                    'oo': open(output_name + 'oo_tm_seqs.fasta', 'w'),
                    'io': open(output_name + 'io_tm_seqs.fasta', 'w'),
                    'oi': open(output_name + 'oi_tm_seqs.fasta', 'w')}

    input_seqs = SeqIO.parse(input_seq_fh, "fasta")


    for pred_line in tmhmm_out_fh.readlines():
        seq_record = input_seqs.next()
        pred_line = line.split()

        # example tmhmm output:
        #sp|Q6LZY8|RCE1_METMP	len=271	ExpAA=168.92	First60=43.93	PredHel=8	Topology=i11-33o38-60i80-102o122-144i157-179o192-214i219-241o245-261i


        if int(pred_line[4].split('=')[1]) > 0:

            # parse data fron topo info in tmhmm output
            topology = pred_line[-1]

            tm_orientation = topology[0] + topology[-1]

            topology = topology.split('-')

            # start and end of predicted helices
            tm_seq_indices = (int(topology[0][1:]) - 1,
                              int(topology[-1][:-1]) - 1)

            tm_seq = seq_record.seq[tm_seq_indices[0]: tm_seq_indices[1]]

            # sanity check that ID makes sense
            if seq_record.id[:len(pred_line[0])] is not pred_line[0]:
                print("Error id do not match")
                print(seq_record.id)
                print(pred_line)

            output_files[tm_orientation].write(seq_record.id)
            output_files[tm_orientation].write(tm_seq)

    tmhmm_out_fh.close()
    input_seq_fh.close()

    for fh in output_files.values():
        fh.close()

