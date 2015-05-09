A Computation Investigation into the Epigenetics of Transcript Isoform Selection
================================================================================

Course Project for Columbia Course in Computational Genomics 
CBMF W4761 

Taught by Itshack Pe'er

Brian Trippe and Jeffrey Zhou

Description
-----------

This github repository describes a pipeline to process ChIP-seq and RNA-seq data into a format that
can be provided to a Random Forest Classifer. In our project, we evaluate the accuracy of the learned
models with 5-fold bootstrapping and use this as a metric for how well correlated certain epigenetic
marks are to the RNA-seq data.

Please see the individual TSS and splicing sub-directories for instructions to proceed with each 
pipeline.

Requirements
------------

Hardware:

* A unix-based operating system
* 8GB RAM, ~300GB hard drive space (optional)

Software:

* Python 2.7
* C++
* rapidjson
* numpy, scipy, scikit-learn

Overall Workflow
----------------

### TSS Workflow ###

See [these](https://github.com/blt2114/compGenomics/tree/master/tss) instructions.

### Splicing Workflow ###

See [these] instructions.

Data Sources
------------

### GTF Annotations: gen10.long.gtf.gz ###

> This file contains all the gene/transcript/exon annotations 
> originally used by the roadmap project used to 
> perform RNA quantification.

[gen10.long.gtf.gz](http://egg2.wustl.edu/roadmap/data/byDataType/rna/annotations/gen10.long.gtf.gz)

### ChIP-seq data: Roadmap Epiegnetics Project###

> Read mappings of ChIP seq data used in the pipeline

[ChIP-data](http://egg2.wustl.edu/roadmap/data/byFileType/alignments/consolidated/)

### RNA-seq data: 57epigenomes.exon.N.pc ###

> RPKM matrix by exon of the RNA-seq data (protein coding genes) used in the pipeline

[57epigenomes.exon.N.pc.gz](http://egg2.wustl.edu/roadmap/data/byDataType/rna/expression/57epigenomes.exon.N.pc.gz)

### RNA-seq data: 57epigenomes.exon.N.nc ###

> RPKM matrix by exon of the RNA-seq data (non-coding genes) used in the pipeline

[57epigenomes.exon.N.nc.gz](http://egg2.wustl.edu/roadmap/data/byDataType/rna/expression/57epigenomes.exon.N.nc.gz)