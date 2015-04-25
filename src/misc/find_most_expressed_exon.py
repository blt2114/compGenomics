# this goes through the exon RPKM file and finds the exon that most
# frequently the most expressed exon by rpkm for that gene so that this
# value can be used as a baseline to calculate the portion of transcripts
# that include other exons on under the assumption that the most expressed
# exon of any gene is constituatively expressed in every transcript.  This
# assumption is likely false an many circumstances but seems to generally
# hold true and is likely a better proxy for the quantity of transcripts
# present than the RPKM value of the genes as a whole.
import json
from collections import Counter
import sys

if len(sys.argv)is not 2:
    sys.stderr.write("invalid usage: python find_most_expressed_exon.py"+
            " <exon_sorted_by_gene.RPKM>")
    sys.exit(2)

max_threshold=1 # the threshold that the most expressed exon of a gene must
                # be above for it to be considered an expressed gene
                # in units of RPKM

exon_file = open(sys.argv[1])

reads_dict={}
first_line=exon_file.readline()
sample_ids=first_line.strip("\n").split("\t")
empty_gene_values={}
gene_lines=[]
empty_gene_values["exons"]=[]
for i in sample_ids:
    empty_gene_values[i]=0 # this is the index of the exon with the largest
    # RPKM for each sample

most_expressed_exons={}

current_gene=None
for line in exon_file:
    parsed=line.strip("\n").split("\t")
    if parsed[1] != current_gene:
        if not current_gene is None:
            exon_indices= []
            for k in sample_ids[2:]:
                # the most highly expressed exon is expressed below the
                # threshold, then the sample is not considered for that gene
                if float(gene_lines[gene_values_by_sample[k]][sample_ids.index(k)])<max_threshold:
                    continue
                exon_indices.append(int(gene_values_by_sample[k]))
            if len(exon_indices)>=1:
                most_expressed_exon=gene_lines[Counter(exon_indices).most_common()[0][0]][0]
                most_expressed_exons[current_gene]=most_expressed_exon
        current_gene=parsed[1]
        gene_values_by_sample=empty_gene_values.copy()
        gene_lines=[]
    gene_lines.append(parsed)
    gene_values_by_sample["exons"].append(parsed[0])
    for i in range (2,len(parsed)-1):
        # if the current exon has the highest RPKM for the sample at hand...
        exon_expr = float(parsed[i])
        highest_exon_expr=  float(gene_lines[gene_values_by_sample[sample_ids[i]]][i])
        if exon_expr>highest_exon_expr:
            #set the current index of the highest to the current exon.
            gene_values_by_sample[sample_ids[i]]=len(gene_lines)-1
exon_file.close()
print json.dumps(most_expressed_exons)
