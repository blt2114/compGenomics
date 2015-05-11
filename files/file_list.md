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

### distribution\_of\_some\_exon\_inclusion.png 
> This shows the distribution of expression of some exons.  
> This was produced to see if a strong trend of bimodality was present
> It seems that this is not the case for most exons in this sample.

### experiment\_read\_counts.json
> JSON dictionary with the read counts for every ChIP experiment for every sample
> This is necessary for scaling the read counts from individual experiments.
> The correct way to preform this scaling without introducing bias has decided.
> This information parsed out of "metadata.tsv"


### exons\_with\_all\_features\_and\_labels
> The contents of this are manifest in its title
> read counts are not scaled in any way.
> these results were used in the first trials of classification of inclusion using a random forest
> The exons are the same set present in \'exons\_labels\_sorted.txt\'

### exons\_with\_all\_features\_and\_scaled\_labels
> the same as above with labels scaled by read count
> currently this scaling is simply dividing by read cound and mulitplying by 1e7 (so that number are not as small)

### labeled\_exons\_in\_middle\_of\_genes.txt
> later iteration of exon selection.  Similar to those described above with two major differences:
>       1. The labels are obtained from division of exon RPKM value with that of a reference exon, chosen becuase it is thought generally be included constituatively.
>       2. No exons were included that are known to be outside of the normal range of transcripts.  This means that exons in this list are thought to only be excluded by AS, and could not be skipped by transcription beginning another TSS or transcription terminating early.


### raw/1254806-Supplementary-Tables.csv
> Table S13.4 from Brandon Frey's paper on AS.
> http://www.sciencemag.org/content/347/6218/1254806/suppl/DC1
> "The human splicing code reveals new insights into the genetic determinants of disease"
> Science December 2014

### Hs\_AS\_novel.bed/
> list of exon alternative splicing events
> obtained from http://zhanglab.c2b2.columbia.edu/index.php/Cortex\_AS


### known\_cassette\_exons.txt
> processed list of known cassette exons, used as input for script: filter\_cassette\_exons.py
