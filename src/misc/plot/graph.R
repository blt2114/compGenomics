tbl = read.table("graph.tsv", sep="\t", header=F)

colnames(tbl)[1] <- mark

by(tbl[, -1], mark, colvar)


h3k4me1 = tbl[tbl[1]=="H3K4me1",]
h3k4me1 =

h3k4me3 = tbl[tbl[1]=="H3K4me3",]
h3k27me3 = tbl[tbl[1]=="H3K27me3",]
h3k36me3 = tbl[tbl[1]=="H3K36me3",]
h3k9me3 = tbl[tbl[1]=="H3K9me3",]
h2az = tbl[tbl[1]=="H2A.Z",]
h3K4me2 = tbl[tbl[1]=="H3K4me2",]
h3k27ac = tbl[tbl[1]=="H3K27ac",]
h4k20me1 = tbl[tbl[1]=="h4k20me1",]
h3k9ac = tbl[tbl[1]=="H3K9ac",]
DNase = tbl[tbl[1]=="DNase",]
H3K79me2 = tbl[tbl[1]=="H3K79me2",]

