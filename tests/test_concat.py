import pytest
import shutil, csv

from fastacat import fastacat

def test_length_addition(tmpdir):
    # Generate a tabular file
    test_csv_in = tmpdir.join('test.csv')
    test_csv_out = tmpdir.join('out.csv')
    shutil.copy('tests/test.csv', test_csv_in.dirname)
    prev = tmpdir.chdir()
    fastacat.generate_tab_file(test_csv_in.open(), test_csv_out.open(mode='w'))

    pass
