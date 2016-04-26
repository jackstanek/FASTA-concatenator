#!/usr/bin/env python3

import os

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
        if not 'length' in fields:
            fields.insert(len(fields) - 2, 'length')

        fields.remove('exon')

        tab_writer = csv.DictWriter(tab_out_file, fieldnames=fields, delimiter='\t')

        # Get first row, setup for the next rows
        prev_line = next(tab_reader)
        fasta_seq = prev_line['FASTA_seq']
        begin = int(prev_line['start'])

        # Write the header row
        tab_writer.writeheader()

        curr_line = tab_reader.__next__()
        while True:
            try:
                if curr_line['transcript_id'] != prev_line['transcript_id']:
                    # Write the new row to the output
                    length = int(prev_line['stop']) - begin + 1
                    write_tab_row(tab_writer, begin, length, fasta_seq, prev_line)
                    begin = int(curr_line['start'])
                    fasta_seq = curr_line['FASTA_seq']

                else:
                    # We're on the same transcript, so add to the
                    # length and concat the next nucleotides
                    fasta_seq += str(curr_line['FASTA_seq'])

                prev_line = curr_line
                curr_line = next(tab_reader)

            except StopIteration:
                # Print the last row
                length = int(prev_line['stop']) - begin + 1
                write_tab_row(tab_writer, begin, length, fasta_seq, prev_line)
                break

def generate_fasta_file(tab_in_file, fasta_out_file):
    tab_reader = csv.reader(tab_in_file, delimiter='\t')

    # Throw out first line
    next(tab_reader, None)

    for line in tab_reader:
        fasta_seq = line.pop()

        fasta_out_file.write('>' + '_'.join(line) + '\n')
        fasta_out_file.write(fasta_seq + '\n')

def make_output_dir(name):
    run = 1
    if os.path.exists(name):
        while os.path.exists(name + str(run)):
            run += 1
        newname = name + str(run)
        os.mkdir(newname)
        return newname
    else:
        os.mkdir(name)
        return name

def fmt_tab_out_path(name):
    return os.path.splitext(name)[0] + '.tsv'

def fmt_fasta_out_path(name):
    return os.path.splitext(name)[0] + '.fasta'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='path to input file')
    # parser.add_argument('sep', default='\t', help='field delimiter')
    args = parser.parse_args()

    output_path = make_output_dir('output_' + os.path.splitext(args.input)[0])
    tab_out_path = os.path.join(output_path, fmt_tab_out_path(args.input))
    fasta_out_path = os.path.join(output_path, fmt_fasta_out_path(args.input))
    print("Writing output to ./" + output_path + "...")

    with open(args.input, newline='') as tab_in_file, open(tab_out_path, mode='w', newline='') as tab_out_file:
        generate_tab_file(tab_in_file, tab_out_file)

    with open(tab_out_path, mode='r', newline='') as tab_out_file, open(fasta_out_path, mode='w', newline='') as fasta_out_file:
        generate_fasta_file(tab_out_file, fasta_out_file)

    print("Done.")

if __name__ == '__main__':
    main()
