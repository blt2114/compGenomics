from utils import GTFRecord

def test_GTFRecord():
    a = GTFRecord(
        'chr1',
        'ENSEMBL',
        'exon',
        '7990339',
        '7990408',
        '.',
        '-',
        '.',
        'gene_id "7699"; transcript_id "7699"; gene_type "tRNAscan"; gene_status "NULL"; gene_name "7699"; transcript_type "tRNAscan"; transcript_status "NULL"; transcript_name "7699"; level 3;',
        )
    assert a.seqname == 'chr1'
    assert a.attribute['gene_id'] == '7699'
