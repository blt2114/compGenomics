#!/usr/bin/env python

"""
This file filters a gtf file for genes that have only one tss start site.

By default, it will exclude pairs of genes that are closer than the defined granuality parameter.

Usage:
python filter_single_tss.py ../../files/gen10.long.gtf.transcripts 500 > single_tss.json

"""

__author__ = 'jeffrey'

import sys, tempfile, subprocess, json
from src.utils import GTF

# Main Method
def main(argv):
    if len(sys.argv) is not 3:
        sys.stderr.write("invalid usage: python filter_single_tss.py"+
                " <gen10.long.gtf.transcripts> "+
                " <granularity(int)>\n")
        sys.exit(2)

    # Initialize Variables
    gtf_fn = sys.argv[1]
    granularity = int(sys.argv[2])
    previous_gene = None
    gene_stack = []
    final_gene_list = []

    # Create Temporary file to store sorted GTF File
    temp = tempfile.NamedTemporaryFile()
    f = open(temp.name, 'r+b')

    # Sort GTF File
    sys.stderr.write('Sorting GTF file based on gene name, chr, start.\n')
    subprocess.call("sort -t $'\t' -k9,9 -k1,1 -k4,4 " + gtf_fn, shell=True, stdout=f)
    f.seek(0)

    # Read the sorted tempfile
    sys.stderr.write('Starting to read sorted GTF file.\n')
    passed_dict = {'total': 0, 'gene_type': {}, 'gene_status': {}}
    failed_dict = {'total': 0, 'gene_type': {}, 'gene_status': {}}
    gene_count = 0
    for line in f:
        gtf = GTF(line)
        if gtf.strand == '+':
            tss = gtf.start
        else:
            tss = gtf.end
        tup = (gtf, tss)
        if previous_gene is None:
            gene_stack.append(tup)
        elif gtf.attribute['gene_id'] == previous_gene:
            gene_stack.append(tup)
        else:
            gene_count += 1
            gene_stack = dump_stack(gene_stack, final_gene_list, passed_dict, failed_dict)
            if len(gene_stack) != 0:
                raise ValueError('Gene stack is not empty! Stack must be empty.')
            gene_stack.append(tup)
        previous_gene = gtf.attribute['gene_id']
    if len(gene_stack) < 1:
        raise ValueError('Gene stack is empty. Stack cannot be empty.')
    dump_stack(gene_stack, final_gene_list, passed_dict, failed_dict)
    sys.stderr.write('Finished sorting file. Now removing genes within granularity.\n')

    # Sort the final list by the tss position
    final_gene_list.sort(key=lambda t: (t[0].seqname, t[1]))
    count = 0
    previous_gene = None
    write_next = True
    for gene_tup in final_gene_list:
        if previous_gene is None:
            write_next = True
        elif previous_gene[0].seqname != gene_tup[0].seqname:
            # Can Write Previous Gene, the two genes are on different chromosomes
            if write_next:
                data = {
                    "read_dir" : previous_gene[0].strand,
                    "gene" : previous_gene[0].attribute['gene_id'].split('.')[0],
                    "chrom" :previous_gene[0].seqname,
                    "location" : previous_gene[1],
                    "gene_type" : previous_gene[0].attribute['gene_type'],
                    "gene_status" : previous_gene[0].attribute['gene_status'],
                    "gene_name" : previous_gene[0].attribute['gene_name'],
                }
                print json.dumps(data)
            write_next = True
        elif abs(previous_gene[1] - gene_tup[1]) < granularity:
            # Do not write previous gene
            # Do not write this gene
            if write_next: count += 2
            else: count += 1
            write_next = False
        else:
            # Implies the difference between the two genes is greater than the defined granularity
            if write_next:
                data = {
                    "read_dir" : previous_gene[0].strand,
                    "gene" : previous_gene[0].attribute['gene_id'].split('.')[0],
                    "chrom" :previous_gene[0].seqname,
                    "location" : previous_gene[1],
                    "gene_type" : previous_gene[0].attribute['gene_type'],
                    "gene_status" : previous_gene[0].attribute['gene_status'],
                    "gene_name" : previous_gene[0].attribute['gene_name'],
                }
                print json.dumps(data)
            write_next = True
        previous_gene = gene_tup
    # Write Previous Gene
    if write_next:
        data = {
            "read_dir" : previous_gene[0].strand,
            "gene" : previous_gene[0].attribute['gene_id'].split('.')[0],
            "chrom" :previous_gene[0].seqname,
            "location" : previous_gene[1],
            "gene_type" : previous_gene[0].attribute['gene_type'],
            "gene_status" : previous_gene[0].attribute['gene_status'],
            "gene_name" : previous_gene[0].attribute['gene_name'],
        }
        print json.dumps(data)
    f.close()

    sys.stderr.write('Program is done.\n')
    sys.stderr.write('Number of genes total: ' + str(gene_count+1) + '\n')
    sys.stderr.write('Number of genes w/ >1 TSS: ' + str(failed_dict['total']) + '\n')
    sys.stderr.write('Number of genes w/ 1 TSS: ' + str(len(final_gene_list)) + '\n')
    sys.stderr.write('Number of genes discarded due to granularity: ' + str(count) + '\n\n')
    sys.stderr.write('1 TSS Genes Status:\n' + str(passed_dict['gene_status']) + '\n')
    sys.stderr.write('>1 TSS Genes Status:\n' + str(failed_dict['gene_status']) + '\n\n')
    sys.stderr.write('1 TSS Genes Types:\n' + str(passed_dict['gene_type']) + '\n\n')
    sys.stderr.write('>1 TSS Genes Types:\n' + str(failed_dict['gene_type']) + '\n\n')



def dump_stack(gene_stack, final_gene_list, passed_dict, failed_dict):
    """
    :param gene_stack: A stack of tup(gtf, tss) that all share the same gene
    :param granularity: An int representing the minimum treshhold between genes
    :param final_gene_list: The list of genes we will print in the very end
    :return: none
    """
    if len(gene_stack) < 1:
                raise ValueError('Gene stack is empty. Stack cannot be empty.')

    previous_tup = None
    for tup in gene_stack:
        if previous_tup is None:
            previous_tup = tup[1]
        elif previous_tup[1] != tup[1]:
            # This means the last transcript and this transcript not share the same TSS, which fails our criteria
            failed_dict['total'] += 1
            if tup[0].attribute['gene_type'] in failed_dict['gene_type']:
                failed_dict['gene_type'][tup[0].attribute['gene_type']] += 1
            else:
                failed_dict['gene_type'][tup[0].attribute['gene_type']] = 1
            if tup[0].attribute['gene_status'] in failed_dict['gene_status']:
                failed_dict['gene_status'][tup[0].attribute['gene_status']] += 1
            else:
                failed_dict['gene_status'][tup[0].attribute['gene_status']] = 1
            if tup[0].attribute['gene_status'] in failed_dict['gene_status']:
                failed_dict['gene_status'][tup[0].attribute['gene_status']] += 1
            else:
                failed_dict['gene_status'][tup[0].attribute['gene_status']] = 1
            return []
        previous_tup = tup
    gene_tup = (previous_tup[0], previous_tup[1])
    final_gene_list.append(gene_tup)
    passed_dict['total'] += 1
    if previous_tup[0].attribute['gene_type'] in passed_dict['gene_type']:
        passed_dict['gene_type'][previous_tup[0].attribute['gene_type']] += 1
    else:
        passed_dict['gene_type'][previous_tup[0].attribute['gene_type']] = 1
    if previous_tup[0].attribute['gene_status'] in passed_dict['gene_status']:
        passed_dict['gene_status'][previous_tup[0].attribute['gene_status']] += 1
    else:
        passed_dict['gene_status'][previous_tup[0].attribute['gene_status']] = 1
    return []

# Execute this module as a command line script
if __name__ == "__main__":
    main(sys.argv[1:])

