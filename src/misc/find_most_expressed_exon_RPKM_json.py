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
import numpy as np

if len(sys.argv)is not 2:
    sys.stderr.write("invalid usage: python find_most_expressed_exon.py"+
            " <exon.RPKM.json>\n")
    sys.exit(2)

max_threshold=1 # the threshold that the most expressed exon of a gene must
                # be above for it to be considered an expressed gene
                # in units of RPKM

exon_file = open(sys.argv[1])

genes_dict={}
for l in exon_file:
    exon_dict= json.loads(l);
    gene_id=exon_dict["gene_id"]
    if genes_dict.has_key(gene_id):
        genes_dict[gene_id]["exons"].append(exon_dict)
    else:
        genes_dict[gene_id]={"exons":[exon_dict]}

exon_file.close()
most_expressed_exons={}
count =0
num_genes=len(genes_dict)
for gene_id in genes_dict.keys():
    if count%1000 ==0:
        sys.stderr.write("processed "+str(count)+" of "+str(num_genes) +" genes\n")
    sample_names= genes_dict[gene_id]["exons"][0]["RPKM_by_sample"].keys()
    genes_dict[gene_id]["exons_p"]=[[]]*len(genes_dict[gene_id]["exons"])
    for sample in sample_names:
        sum_of_RPKMS_in_exons=0
        for exon in genes_dict[gene_id]["exons"]:
            sum_of_RPKMS_in_exons+= exon["RPKM_by_sample"][sample]
        if sum_of_RPKMS_in_exons==0:
#            sys.stderr.write("for gene_id: "+gene_id+" sample: "+sample+"sum of RPKMS is 0\n")
            # in this case set all values to 0
            for i in range(0,len(genes_dict[gene_id]["exons"])):
                genes_dict[gene_id]["exons_p"][i].append(0)
            continue
        for i in range(0,len(genes_dict[gene_id]["exons"])):
            exon= genes_dict[gene_id]["exons"][i]
            rpkm_over_sum = exon["RPKM_by_sample"][sample]/sum_of_RPKMS_in_exons
            genes_dict[gene_id]["exons_p"][i].append(rpkm_over_sum)
    genes_dict[gene_id]["exons_p_ave"]=[0]*len(genes_dict[gene_id]["exons"])
    for i in range(0,len(genes_dict[gene_id]["exons"])):
        genes_dict[gene_id]["exons_p_ave"][i]=np.mean(genes_dict[gene_id]["exons_p"][i])
    idx_of_most_expressed_exon=genes_dict[gene_id]["exons_p_ave"].index(max(genes_dict[gene_id]["exons_p_ave"]))
    most_expressed_exons[gene_id]=genes_dict[gene_id]["exons"][i]
    count +=1
print json.dumps(most_expressed_exons)
