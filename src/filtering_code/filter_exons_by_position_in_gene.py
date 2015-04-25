import sys
import json


if not len(sys.argv) == 3:
    sys.stderr.write("invalid usage: python trim_genes.py"+
            " <genes.json> <exons.json>\n")
    sys.exit(2)

genes_fn = sys.argv[1]
exons_fn = sys.argv[2]

genes_file= open(genes_fn)

genes_dict={}

for line in genes_file:
    gene = json.loads(line)
    gene_id = gene["gene"].split(".")[0]
    genes_dict[gene_id]={}
    start = max(gene["transcripts_starts"])
    genes_dict[gene_id]["start"]=start
    end = max(gene["transcripts_ends"])
    genes_dict[gene_id]["end"]=end
    
genes_file.close()

exons_file = open(exons_fn)

for line in exons_file:
    exon = json.loads(line)
    # ignore the the decimal portion of gene name
    gene_id= exon["gene_id"]
    
    # find beginning and end of the exon based on its orientation
    if exon["read_dir"]==1:
        ex_start= exon["five_p_loc"]
        ex_end=exon["three_p_loc"]
    else:
        ex_start= exon["three_p_loc"]
        ex_end= exon["five_p_loc"]
    gene=genes_dict[gene_id]
    if int(ex_start) > int(gene["start"]) and int(ex_end) < int(gene["end"]):
        print json.dumps(exon)
