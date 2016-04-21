#!/usr/bin/env python3

import csv
import argparse

def to_fasta(line):
    pass

def write_tab_row(dr, begin, length, fasta_seq, prev_line):
    dr.writerow({
        'chr': prev_line['chr'],
        'start': begin,
        'stop': prev_line['stop'],
        'strand': prev_line['strand'],
        'gene_id': prev_line['gene_id'],
        'transcript_id': prev_line['transcript_id'],
        'length': length,
        'FASTA_seq': fasta_seq
    })


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
        prev_line = tab_reader.__next__()
        fasta_seq = prev_line['FASTA_seq']
        length = int(prev_line['stop']) - int(prev_line['start'])
        begin = int(prev_line['start'])

        # Write the header row
        tab_writer.writeheader()

        curr_line = tab_reader.__next__()
        while True:
            try:
                if curr_line['transcript_id'] != prev_line['transcript_id']:
                    # Write the new row to the output
                    write_tab_row(tab_writer, begin, length, fasta_seq, prev_line)
                    begin, length = curr_line['start'], 0
                    fasta_seq = ''

                else:
                    # We're on the same transcript, so add to the
                    # length and concat the next nucleotides
                    length += int(curr_line['stop']) - int(curr_line['start'])
                    fasta_seq += str(curr_line['FASTA_seq'])

                prev_line = curr_line
                curr_line = tab_reader.__next__()

            except StopIteration:
                # Print the last row
                write_tab_row(tab_writer, begin, length, fasta_seq, prev_line)
                break


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='path to input file')
    # parser.add_argument('sep', default='\t', help='field delimiter')
    args = parser.parse_args()
    generate_tab_file(args.path)


if __name__ == "__main__":
    main()
