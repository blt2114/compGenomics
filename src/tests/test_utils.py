import os, sys
from utils import GTFRecord

def test_GTFRecord():
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
    b = GTFRecord(a)
    assert b.seqname == 'chr1'
    assert b.attribute['gene_id'] == '7699'

def test_GTFRecord_importTSS():
    list = GTFRecord.importTSS('../files/gen10.long.gtf')
    assert list[0].attribute['transcript_id'] == 'ENST00000390237.2'
