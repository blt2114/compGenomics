import sys
import json


if not len(sys.argv) == 2:
    sys.stderr.write("invalid usage: python trim_genes.py"+
            " <genes.json>\n")
    sys.exit(2)

genes_fn = sys.argv[1]
genes_file= open(genes_fn)

read_dirs={"+":1,"-":-1}
for line in genes_file:
    gene = json.loads(line)
    gene_dict={}
    gene_dict["gene"]=gene["attribute"]["gene_id"]
    gene_dict["read_dir"]=read_dirs[gene["strand"]]
    gene_dict["chrom"]=gene["seqname"]
    gene_dict["location"]=gene["start"]
    gene_dict["transcripts_starts"]=[]
    gene_dict["transcripts_ends"]=[]
    for t_name in gene["transcripts"].keys():
        t=gene["transcripts"][t_name]
        gene_dict["transcripts_ends"].append(t["end"])
        gene_dict["transcripts_starts"].append(t["start"])
    print json.dumps(gene_dict)

genes_file.close()
