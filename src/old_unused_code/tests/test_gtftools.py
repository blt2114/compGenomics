from gtftools import GTF
import logging

def test_GTF_init():
     a = [
        'chr1',
        'ENSEMBL',
        'exon',
        '7990339',
        '7990408',
        '.',
        '-',
        '.',
        'gene_id "7699"; transcript_id "7699"; gene_type "tRNAscan"; gene_status "NULL"; gene_name "7699"; transcript_type "tRNAscan"; transcript_status "NULL"; transcript_name "7699"; level 3;',
        ]
     b = GTF(a)
     assert b.seqname == 'chr1'
     assert b.attribute['gene_id'] == '7699'
     return b

def test_GTF_repr():
     assert test_GTF_init().attribute == eval(repr(test_GTF_init())).attribute

