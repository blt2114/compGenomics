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
    
### Step 2: Filter the gtf file for transcripts that have only one TSS per gene -- DONE ###
    cat gen10.long.gtf | python gtftools.py -f feature=transcript > gen10.long.gtf.transcripts 

Note: To use the filter_single_tss.py script, you need to:

    export PYTHONPATH={path to the compgenomics folder}

Command Used:

    python filter_single_tss.py ../../files/gen10.long.gtf.transcripts 500 > single_tss.json

stderr output:

    Sorting GTF file based on gene name, chr, start.
    Starting to read sorted GTF file.
    Finished sorting file. Now removing genes within granularity.
    Program is done.
    Number of genes total: 43575
    Number of genes w/ >1 TSS: 19582
    Number of genes w/ 1 TSS: 23993
    Number of genes discarded due to granularity: 859

    1 TSS Genes Status:
    {'KNOWN': 15676, 'NOVEL': 4715, 'PUTATIVE': 3602}
    >1 TSS Genes Status:
    {'KNOWN': 16779, 'NOVEL': 2338, 'PUTATIVE': 465}

    1 TSS Genes Types:
    {'TR_J_pseudogene': 4, 'IG_C_pseudogene': 7, 'retained_intron': 8, 'antisense': 2753, 'IG_V_gene': 131, 'polymorphic_pseudogene': 4, 'IG_J_gene': 18, 'lincRNA': 4035, 'IG_J_pseudogene': 3, 'IG_C_gene': 14, 'protein_coding': 4291, 'TR_V_pseudogene': 27, 'sense_overlapping': 17, 'TR_J_gene': 74, 'IG_V_pseudogene': 151, 'pseudogene': 11017, 'TR_V_gene': 97, 'sense_intronic': 371, 'non_coding': 87, 'ambiguous_orf': 18, 'IG_D_gene': 27, 'ncrna_host': 11, 'TR_C_gene': 5, 'processed_transcript': 808, 'TR_D_gene': 3, '3prime_overlapping_ncrna': 12}

    >1 TSS Genes Types:
    {'IG_V_gene': 1, 'pseudogene': 1122, 'lincRNA': 1449, 'retained_intron': 2, 'antisense': 773, 'protein_coding': 15716, 'sense_intronic': 24, 'processed_transcript': 449, 'sense_overlapping': 1, 'ncrna_host': 3, 'polymorphic_pseudogene': 23, 'non_coding': 17, 'ambiguous_orf': 2}    
   

### Step 3: Get RNA data at these TSS positions ###

### Step 4: Get ChIP data at these TSS positions ###

### Step 5: Run on ML ###
