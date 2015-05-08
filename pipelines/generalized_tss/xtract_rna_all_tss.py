#!/usr/bin/env python

"""
The purpose of this script is to extract the RPKM data from a matrix of exon expressions, and append this
information to an overall JSON file that will eventually be fed into the Random Forest. The structure of
the output JSON file is as follows:

Each line is a TSS site. The number of TSS sites have been reduced to the number of exons inside the RPKM
matrix. The reasoning for this is that when multiple theoretical transcripts map to the same exon in the RPKM
matrix, the granularity of the data is limited to entire exons. Therefore, we will consider all transcripts
that map to the same exon as a group of TSS sites that aggregately hold this position.

Each effective TSS site contains a list of transcripts, along with a dictionary of samples and their expression
values. This scripts also calculates a lot of metadata, such as which exons are spliced and which in what
proportion of transcripts they are spliced.

"""

__author__ = 'jeffrey'

import sys, json, collections, copy
from src.utils import FileProgress

# Main Method
def main(argv):
    # parse args
    if len(sys.argv) is not 5:
        sys.stderr.write("invalid usage: python " + sys.argv[0] +
                " <all_tss.json> <57epigenomes.exon.RPKM.all> <chromosome_order.json> <granularity>\n")
        sys.exit(2)

    tss_fn = sys.argv[1]
    rna_fn = sys.argv[2]
    chromosomes_fn = sys.argv[3]
    granularity = int(sys.argv[4])
    progress1 = FileProgress(rna_fn, "Part 1/2: ")

    # load expected chromosome order from json into a dictionary
    with open(chromosomes_fn) as chromosomes_file:
        chromosomes = json.load(chromosomes_file)

    # Load JSON GTF file into memory
    gene_dict = {}
    with open(tss_fn, 'rb') as json_file:
        for line in json_file:
            gene = json.loads(line)
            gene_dict[gene['gene_id']] = gene
    sys.stderr.write("Loaded " + str(len(gene_dict)) + " genes into memory.\n")

    # Read RNA-seq data into memory
    # The purpose of this entire section is calculate leading and cassette exons
    gene_rna_dict = {}
    sample_names = {}
    with open(rna_fn) as rna_f:
        for line in rna_f:
            if progress1.count == 0:
                row = line.strip('\n').split('\t')
                for i in range(2, len(row)):
                    sample_names[row[i]] = i-2
            else:
                row = line.strip('\t\n').split('\t')
                gene = row[1]
                if gene in gene_dict:
                    start = int(row[0].split(':')[1].split('-')[0])
                    end = int(row[0].split('-')[1].split('<')[0])
                    strand = int(row[0].split('<')[1])
                    if gene not in gene_rna_dict:
                        gene_rna_dict[gene] = []
                    gene_rna_dict[gene].append( {
                        'gene' : gene,
                        'seqname' : row[0].split(':')[0],
                        'start' : start,
                        'end' : end,
                        'strand' : ('+' if strand==1 else '-'),
                        'samples' : row[2:],    # There's some weird formatting in the RPKM file
                        'tss' : (start if strand==1 else end)
                    } )
                    assert len(sample_names) == len(row[2:])
            progress1.update()

    # Main loop of genes
    progress2 = FileProgress(None, "Part 2/2: ", len(gene_rna_dict))
    sys.stderr.write("\nLoaded " + str(len(gene_rna_dict)) + " mRNA exons into memory.\n")
    for genes in sorted(gene_rna_dict.values(), key=lambda k: ( chromosomes[k[0]['seqname']], k[0]['tss'] )):
        gene = genes[0]['gene']
        if gene in gene_dict:

            # Iterate through the genes and calculate the exon number
            genes.sort(key=lambda x: x['start'])
            if genes[0]['strand'] == '+':
                for i in range(1, len(genes) + 1):
                    genes[i-1]['exon_number'] = i
            else:
                for i in range(1, len(genes) + 1):
                    genes[len(genes)-i]['exon_number'] = i

            # Calculate cell with from samples maximum value
            max_exon = None
            max_rpkm = 0
            for exon in genes:
                for sample_rpkm in exon['samples']:
                    if float(sample_rpkm) >= max_rpkm:
                        max_exon = exon['samples']
                        max_rpkm = float(sample_rpkm)
            assert max_exon is not None

            # Iterate through exons within this gene
            printlist = []
            for i in range(0, len(genes)):
                exon = genes[i]
                samples = exon['samples']

                # Assign all transcripts that map to this exon
                exon_transcripts = []
                splice_count = 0
                splice_before = 0
                coverage_count = 0
                for transcript in gene_dict[gene]['transcripts'].itervalues():
                    if transcript['tss'] > exon['start'] - granularity and transcript['tss'] < exon['end'] + granularity:
                        exon_transcripts.append(transcript)
                    for intron in transcript['introns']:
                        if exon['start'] > intron[1] or exon['end'] < intron[0]:
                            # not spliced out
                            pass
                        else:
                            splice_count += 1
                        if exon['strand'] == '+':
                            if intron[1] < exon['start']:
                                splice_before += 1
                        else:
                            if intron[0] > exon['end']:
                                splice_before += 1
                    if exon['strand'] == '+':
                        if transcript['end'] < exon['start']:
                            splice_before += 1
                    else:
                        if transcript['end'] < exon['start']:
                            if transcript['start'] > exon['end']:
                                splice_before += 1
                    for transcript_exon in transcript['exons']:
                        if exon['start'] > transcript_exon[1] or exon['end'] < transcript_exon[0]:
                            # not covered by exon
                            pass
                        else:
                            coverage_count += 1

                # If a transcript mapped to one of the exons
                if len(exon_transcripts) > 0:

                    # Save this transcript
                    d = collections.OrderedDict()
                    d['seqname'] = exon['seqname']
                    d['tss'] = exon['tss']
                    d['strand'] = exon['strand']
                    d['gene_id'] = gene
                    d['exon_number'] = exon['exon_number']
                    d['exon_total'] = len(genes)
                    d['splice_count'] = splice_count
                    d['splice_before'] = splice_before
                    d['coverage_count'] = coverage_count
                    d['tss_mapped'] = len(exon_transcripts)
                    d['tss_total'] = 0
                    d['transcript_total'] = len(gene_dict[gene]['transcripts'])
                    d['transcripts'] = copy.deepcopy(exon_transcripts)
                    d['samples'] = {}
                    for sample_name, i in sample_names.iteritems():
                        if sample_name not in d['samples']:
                            d['samples'][sample_name] = {}
                        d['samples'][sample_name]['rpkm'] = float(samples[i])
                        d['samples'][sample_name]['max_rpkm'] = float(max_exon[i])
                    printlist.append(d)

            # Iterate through the exons again (this time of the accepted list)
            # We calculate the delta_rpkm to the previous transcript start site
            for k in range(0, len(printlist)):
                d = printlist[k]
                for sample_name in sample_names.iterkeys():
                    d['tss_total'] = len(printlist)
                    if len(printlist) == 1:
                         d['samples'][sample_name]['delta_rpkm'] = d['samples'][sample_name]['rpkm']
                    else:
                        try:
                            if d['strand'] == '+':
                                d['samples'][sample_name]['delta_rpkm'] = d['samples'][sample_name]['rpkm'] - printlist[k-1]['samples'][sample_name]['rpkm']
                            else:
                                d['samples'][sample_name]['delta_rpkm'] = d['samples'][sample_name]['rpkm'] - printlist[k+1]['samples'][sample_name]['rpkm']
                        except IndexError:
                            d['samples'][sample_name]['delta_rpkm'] = d['samples'][sample_name]['rpkm']
                # Delete redundant information to reduce size of the file
                for this_transcript in d['transcripts']:
                    this_transcript.pop("exons")
                    this_transcript.pop("introns")
                    this_transcript.pop("length")
                    this_transcript.pop("score")
                    this_transcript.pop("frame")
                    this_transcript.pop("feature")
                    this_transcript.pop("strand")
                    this_transcript.pop("seqname")
                    this_transcript.pop("start")
                    this_transcript.pop("end")
                print json.dumps(d)
        progress2.update()

    sys.stderr.write("\nAll done!\n")

# Execute this module as a command line script
if __name__ == "__main__":
    main(sys.argv[1:])





