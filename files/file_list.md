List of Files Needed to Run Pipeline
====================================

For storage purposes, we will not track large data files on
github. I ran into a few files that are several gigabytes in
size, so please keep the links to the files here.

File List
---------

### FILE: gen10.long.gtf.gz ###

> This file contains all the gene/transcript annotations that
> Misha Belinky from UBC (author of the project) used to 
> perform RNA quantification. 
>
> This dataset is a subset of the original GENCODE v10 from ncbi
> which is the full dataset of all transcripts/genes not including
> tRNAs. This "long" dataset only contains entries of long
> transcripts (protein coding, processed transcripts, pseduogenes).
> We will use this file for our parsing purposes and ignore small
> RNAs since Misha did not perform alignment to smaller RNAs.

[gen10.long.gtf.gz](http://egg2.wustl.edu/roadmap/data/byDataType/rna/annotations/gen10.long.gtf.gz)

### FILE: 57epigenomes.exon.N.pc ###

> Brian put this file here.

[57epigenomes.exon.N.pc.gz](http://egg2.wustl.edu/roadmap/data/byDataType/rna/expression/57epigenomes.exon.N.pc.gz)

### FILE: tss.json ###

> made with -m set to 50


### genes\_expressed\_in\_most\_samples.tsv
> made with grep command formed by filter\_genes\_by\_expression.sh
> filtered out genes with no more than 35 samples with expression less than 100 RPKM
> 334 genes in the list

### exon\_labels\_sorted.txt 
> Lines of exons in JSON formatwith labels for each sample of the inclusion ratio 
> (the RPKM for that exon/ the RPKM for the gene is in)
> This is a horrible metric, but was easy to come up with, later iterations are intended to 
> use a better metric and include a better subset of exons
> Dictionaries also include 5' and 3' locations.

### labeled\_exons\_with\_features.txt
> This was the first set of data used to train and test a model.
> lines are JSON dictionaries that include the chromatin states at the 3' and 
> 5' and the inclusion ratio for every sample in which the gene of 
> that exon is expressed.
