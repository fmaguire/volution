#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
Script to process tmhmm in parallel
"""

from Bio import SeqIO

import argparse
import os
import sys
import multiprocessing

def parse_and_validate(args):
    """
    Parse input args
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input_file",
                        help="input fast file",
                        type=str,
                        action="store")

    parser.add_argument("-o", "--output_dir",
                        help="output directory",
                        type=str,
                        action="store")

    parser.add_argument("-p", "--cpu",
                        help="number of cores",
                        type=int,
                        action="store")

    args = parser.parse_args()


    if not os.path.isfile(args.input_file):
        print("Input file {} does not exist".format(args.input_file))
        sys.exit(1)

    if not os.path.isdir(args.output_dir):
        print("Output directory {} does not exist".format(args.output_dir))
        sys.exit(1)

    return parser.parse_args()


def split_input(fasta_fp, input_name):
    """
    Split input fasta into 1000 sequences subset fasta files
    return a list of these filepaths to split fasta
    """

    n = 1000

    sequences = SeqIO.parse(fasta_fp, 'fasta')

    subset_files = []

    input_name = os.path.splitext(os.path.split(fasta_fp)[-1])[0]

    # file number index and sequence range i
    for index, i in enumerate(range(0, len(sequences), n)):
        subset_seqs = [x for x in sequences[i: i+n]]

        subset_fp = os.path.join('tmp',
                                 input_name + '_{}_subset.fasta'.format(index))

        SeqIO.write(subset_seqs, subset_fp, 'fasta')

        subset_files.append(subset_fp)

    return subset_files

def run_tmhmm(fasta_files, cores):
    """
    Run TMHMM on the subsets using multiprocessing
    Return list
    """

    cmds = []
    output_files = []

    for file_path in fasta_files:
        output_path = file_path + '.tmhmm'
        cmds.append('tmhmm {} | grep -v "PredHel=0" > {}'.format(file_path,
                                                                 output_path))
        output_files.append(output_path)


    pool = multiprocessing.Pool(processes = cores)

    pool_output = [pool.apply_async(subprocess.call,
                                    (str(cmd), ),
                                    {'stderr': subprocess.PIPE,
                                     'shell'; True})
                    for cmd in cmds]

    pool.close()
    pool.join()

    return output_files




def combine_and_clean(tmhmm_files, , output_dir):
    """
    Combine tmhmm files
    """

    cmd = "cat {} > {}".format(" ".join(output_files),

    exit = subprocess.run(cmd, shell=True)

    if exit.returncode == 0:
        shutil.rmtree('tmp')



if __name__ == '__main__':

    args = parse_and_validate(sys.argv)

    if not os.path.isdir('tmp'):
        os.mkdir('tmp')

    input_name = os.path.splitext(os.path.split(args.input_fasta)[-1])[0]

    subset_fps = split_input(args.input_file, input_name)

    subset_tmhmm_outputs = run_tmhmm(subset_fps, args.cpu)

    output_filename = combine_and_clean(subset_tmhmm_outputs, input_name,
                                        args.output_directory)
