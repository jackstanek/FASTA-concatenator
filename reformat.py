#!/usr/bin/env python3

import csv, argparse

def exon_length(dr):
    pass

def to_fasta(line):
    pass

def generate_tab_file(path):
    tab_in_path = path
    tab_out_path = ".".join([tab_in_path.split(".")[0] + '_NEW', tab_in_path.split(".")[1]])
    fasta_out_path = ".".join([tab_in_path.split(".")[0], 'fasta'])
    with open(tab_in_path, newline='') as tab_in_file, open(tab_out_path, mode="w", newline='') as tab_out_file:

        # Get the reader
        tab_reader = csv.DictReader(tab_in_file, delimiter='\t')

        # Get the writer
        fields = tab_reader.fieldnames.copy()
        fields.insert(len(fields) - 2, 'length')
        fields.remove('exon')

        tab_writer = csv.DictWriter(tab_out_file, fieldnames=fields, delimiter='\t')

        # Get first row, setup for the next rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    generate_tab_file(args.path)


if __name__ == "__main__":
    main()
