Pipeline to Determine a ML model for a single TSS
-------------------------------------------------

### Background ###

It is well known that the H3K27Ac histone mark correlates well with the start of transcription. Since this is
**known** information, it would be worthwhile to test whether any ML that we construct can validate something 
that is **extremely** well established in literature. 

While this is not a very exciting experiment to perform, I think it is necessary because we need to validate our
ML approach and get a sense of what numbers are reasonable in a situation we should already know the outcome.

### Experimental Question ###

How well does the histone mark status at any arbitrary TSS correlate with the expression of its RNA?

Can we determine and rank which histone marks correlate the best with the expression of RNA?

***Hypothesis:*** H3K27Ac should correlate fairly well, even with arbitrary TSS's. This is well established in literature.

### Experimental Approach ###

We will test only genes with exactly ONE known transcriptional start site. Note that this does not necessarily signify
genes with only one reported transcript -- it signifies genes with transcripts that all have the same TSS.

We will include noncoding and protein coding mRNAs of long transcripts only. 

We will exclude all genes that are "too close" to each other based on their TSS positions. We define "too close" to mean
any size smaller than our ChIP-seq window size.

We will examine the RPKM by gene, since all the transcript variants should have the same TSS as defined in our criteria.
Gene with an RPKM < 1 should be considered not expressed, and >1 should be considered expressed.

Programs and Commands
---------------------

### Input Files ###
* gen10.long.gtf
* 57epigenomes.RPKM.nc
* 58epigenomes.RPKM.pc

### Step 1: Combine the two RPKM by gene files -- DONE ###
    head -1 57epigenomes.RPKM.pc >> 57epigenomes.exon.RPKM.all
    tail -q -n +2 57epigenomes.RPKM.pc 57epigenomes.RPKM.nc >> 57epigenomes.RPKM.all
    
### Step 2: Filter the gtf file for transcripts that have only one TSS per gene -- WIP ###
    cat gen10.long.gtf | python gtftools.py -f feature=transcript > gen10.long.gtf.transcripts 

    


### Step 3: Get RNA data at these TSS positions ###

### Step 4: Get ChIP data at these TSS positions ###

### Step 5: Run on ML ###
