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
