#!/usr/bin/env python3

import csv
import argparse

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

def generate_tab_file(tab_in_file, tab_out_file):
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
                    fasta_seq = curr_line['FASTA_seq']

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

def generate_fasta_file(tab_in_file, fasta_out_file):
    tab_reader = csv.reader(tab_in_file, delimiter='\t')

    # Throw out first line
    next(tab_reader, None)

    for line in tab_reader:
        fasta_seq = line.pop()

        # Discard length
        line.pop()

        fasta_out_file.write(">" + "_".join(line) + "\n")
        fasta_out_file.write(fasta_seq + "\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='path to input file')
    parser.add_argument('tab_output', help='path to tabular output file')
    parser.add_argument('fasta_output', help='path to fasta output file')
    # parser.add_argument('sep', default='\t', help='field delimiter')

    args = parser.parse_args()
    with open(args.input, newline='') as tab_in_file, open(args.tab_output, mode="w", newline='') as tab_out_file:
        generate_tab_file(tab_in_file, tab_out_file)

    with open(args.tab_output, mode='r', newline='') as tab_out_file, open(args.fasta_output, mode='w', newline='') as fasta_out_file:
        generate_fasta_file(tab_out_file, fasta_out_file)

if __name__ == "__main__":
    main()
