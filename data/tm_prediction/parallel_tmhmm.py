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
