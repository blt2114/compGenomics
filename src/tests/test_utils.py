import os, sys
import logging

from src.utils import GTF

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

def test_GTF_init():
    str = 'chr1	ENSEMBL	exon	7990339	7990408	.	-	.	gene_id "7699"; transcript_id "7699"; gene_type "tRNAscan"; gene_status "NULL"; gene_name "7699"; transcript_type "tRNAscan"; transcript_status "NULL"; transcript_name "7699"; level 3;'
    strn = 'chr1	ENSEMBL	exon	7990339	7990408	.	-	.	gene_id "7699"; transcript_id "7699"; gene_type "tRNAscan"; gene_status "NULL"; gene_name "7699"; transcript_type "tRNAscan"; transcript_status "NULL"; transcript_name "7699"; level 3;\n'

    a = GTF(str)
    b = GTF(strn)
    assert b.seqname == a.seqname
    assert b.feature == a.feature
    assert b.start == a.start
    assert b.attribute == a.attribute
    assert b.attribute['gene_id'] == '7699'
