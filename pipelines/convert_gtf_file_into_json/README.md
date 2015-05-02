Simple Tool to Convert GTF File into a nested json file
-------------------------------------------------------

### Background ###

It is well known that the H3K27Ac histone mark correlates well with the start of transcription. Since this is
**known** information, it would be worthwhile to test whether any ML that we construct can validate something 
that is **extremely** well established in literature. 

Programs and Commands
---------------------

### Input Files ###
* files/gen10.long.gtf
* src/gtftools.py

### Step 1: Filter gtf file into three partitions ###
    python src/gtftools.py -v -i files/gen10.long.gtf -o files/gen10.long.gtf.genes -f feature=gene
    python src/gtftools.py -v -i files/gen10.long.gtf -o files/gen10.long.gtf.transcripts -f feature=transcript
    python src/gtftools.py -v -i files/gen10.long.gtf -o files/gen10.long.gtf.exons -f feature=exon
    
### Step 2: Run the conversion script ###
Note: To use the gtf2dict.py script, you need to:

    export PYTHONPATH={path to the compgenomics folder}

Command Used:

    python gtf2dict.py ../../files/gen10_files/gen10.long.gtf.genes ../../files/gen10_files/gen10.long.gtf.transcripts ../../files/gen10_files/gen10.long.gtf.exons > ../../files/gen10_files/genes.json
    
stderr output:

    Estimating compute time.
    Starting to load genes.
    Part 1/3: 100%
    Starting to load transcripts.
    Part 2/3: 100%
    Starting to load exons.
    Part 3/3: 100%
    Beginning to print.

Sample Output:

    {
      "seqname": "chr19", 
      "end": 41302847, 
      "start": 41277553, 
      "attribute": {
        "gene_status": "KNOWN", 
        "level": "3", 
        "transcript_type": "protein_coding", 
        "gene_id": "ENSG00000167578.10", 
        "transcript_id": "ENSG00000167578.10", 
        "transcript_name": "MIA", 
        "gene_type": "protein_coding", 
        "transcript_status": "KNOWN", 
        "gene_name": "MIA"
      }, 
      "frame": ".", 
      "feature": "gene", 
      "source": "ENSEMBL", 
      "score": ".", 
      "transcripts": {
        "ENST00000263369.2": {
          "seqname": "chr19", 
          "end": 41283392, 
          "exons": [
            {
              "seqname": "chr19", 
              "end": 41281574, 
              "start": 41281300, 
              "attribute": {
                "gene_status": "KNOWN", 
                "level": "3", 
                "transcript_type": "protein_coding", 
                "tag": "CCDS", 
                "gene_id": "ENSG00000167578.10", 
                "transcript_id": "ENST00000263369.2", 
                "ccdsid": "CCDS12566.1", 
                "transcript_name": "MIA-201", 
                "gene_type": "protein_coding", 
                "transcript_status": "KNOWN", 
                "gene_name": "MIA"
              }, 
              "frame": ".", 
              "feature": "exon", 
              "source": "ENSEMBL", 
              "score": ".", 
              "strand": "+"
            }, 
            {
              "seqname": "chr19", 
              "end": 41281790, 
              "start": 41281657, 
              "attribute": {
                "gene_status": "KNOWN", 
                "level": "3", 
                "transcript_type": "protein_coding", 
                "tag": "CCDS", 
                "gene_id": "ENSG00000167578.10", 
                "transcript_id": "ENST00000263369.2", 
                "ccdsid": "CCDS12566.1", 
                "transcript_name": "MIA-201", 
                "gene_type": "protein_coding", 
                "transcript_status": "KNOWN", 
                "gene_name": "MIA"
              }, 
              "frame": ".", 
              "feature": "exon", 
              "source": "ENSEMBL", 
              "score": ".", 
              "strand": "+"
            }, 
            {
              "seqname": "chr19", 
              "end": 41282984, 
              "start": 41282874, 
              "attribute": {
                "gene_status": "KNOWN", 
                "level": "3", 
                "transcript_type": "protein_coding", 
                "tag": "CCDS", 
                "gene_id": "ENSG00000167578.10", 
                "transcript_id": "ENST00000263369.2", 
                "ccdsid": "CCDS12566.1", 
                "transcript_name": "MIA-201", 
                "gene_type": "protein_coding", 
                "transcript_status": "KNOWN", 
                "gene_name": "MIA"
              }, 
              "frame": ".", 
              "feature": "exon", 
              "source": "ENSEMBL", 
              "score": ".", 
              "strand": "+"
            }, 
            {
              "seqname": "chr19", 
              "end": 41283392, 
              "start": 41283302, 
              "attribute": {
                "gene_status": "KNOWN", 
                "level": "3", 
                "transcript_type": "protein_coding", 
                "tag": "CCDS", 
                "gene_id": "ENSG00000167578.10", 
                "transcript_id": "ENST00000263369.2", 
                "ccdsid": "CCDS12566.1", 
                "transcript_name": "MIA-201", 
                "gene_type": "protein_coding", 
                "transcript_status": "KNOWN", 
                "gene_name": "MIA"
              }, 
              "frame": ".", 
              "feature": "exon", 
              "source": "ENSEMBL", 
              "score": ".", 
              "strand": "+"
            }
          ], 
          "start": 41281300, 
          "attribute": {
            "gene_status": "KNOWN", 
            "level": "3", 
            "transcript_type": "protein_coding", 
            "tag": "CCDS", 
            "gene_id": "ENSG00000167578.10", 
            "transcript_id": "ENST00000263369.2", 
            "ccdsid": "CCDS12566.1", 
            "transcript_name": "MIA-201", 
            "gene_type": "protein_coding", 
            "transcript_status": "KNOWN", 
            "gene_name": "MIA"
          }, 
          "frame": ".", 
          "feature": "transcript", 
          "source": "ENSEMBL", 
          "score": ".", 
          "strand": "+"
        }, 
        "ENST00000378307.4": {
          "seqname": "chr19", 
          "end": 41302847, 
          "exons": [
            {
              "seqname": "chr19", 
              "end": 41284296, 
              "start": 41284213, 
              "attribute": {
                "gene_status": "KNOWN", 
                "level": "3", 
                "transcript_type": "protein_coding", 
                "gene_id": "ENSG00000167578.10", 
                "transcript_id": "ENST00000378307.4", 
                "transcript_name": "MIA-203", 
                "gene_type": "protein_coding", 
                "transcript_status": "KNOWN", 
                "gene_name": "MIA"
              }, 
              "frame": ".", 
              "feature": "exon", 
              "source": "ENSEMBL", 
              "score": ".", 
              "strand": "+"
            }, 
            {
              "seqname": "chr19", 
              "end": 41286004, 
              "start": 41285924, 
              "attribute": {
                "gene_status": "KNOWN", 
                "level": "3", 
                "transcript_type": "protein_coding", 
                "gene_id": "ENSG00000167578.10", 
                "transcript_id": "ENST00000378307.4", 
                "transcript_name": "MIA-203", 
                "gene_type": "protein_coding", 
                "transcript_status": "KNOWN", 
                "gene_name": "MIA"
              }, 
              "frame": ".", 
              "feature": "exon", 
              "source": "ENSEMBL", 
              "score": ".", 
              "strand": "+"
            }, 
            {
              "seqname": "chr19", 
              "end": 41286404, 
              "start": 41286290, 
              "attribute": {
                "gene_status": "KNOWN", 
                "level": "3", 
                "transcript_type": "protein_coding", 
                "gene_id": "ENSG00000167578.10", 
                "transcript_id": "ENST00000378307.4", 
                "transcript_name": "MIA-203", 
                "gene_type": "protein_coding", 
                "transcript_status": "KNOWN", 
                "gene_name": "MIA"
              }, 
              "frame": ".", 
              "feature": "exon", 
              "source": "ENSEMBL", 
              "score": ".", 
              "strand": "+"
            }, 
            {
              "seqname": "chr19", 
              "end": 41289745, 
              "start": 41289683, 
              "attribute": {
                "gene_status": "KNOWN", 
                "level": "3", 
                "transcript_type": "protein_coding", 
                "gene_id": "ENSG00000167578.10", 
                "transcript_id": "ENST00000378307.4", 
                "transcript_name": "MIA-203", 
                "gene_type": "protein_coding", 
                "transcript_status": "KNOWN", 
                "gene_name": "MIA"
              }, 
              "frame": ".", 
              "feature": "exon", 
              "source": "ENSEMBL", 
              "score": ".", 
              "strand": "+"
            }, 
            {
              "seqname": "chr19", 
              "end": 41292665, 
              "start": 41292570, 
              "attribute": {
                "gene_status": "KNOWN", 
                "level": "3", 
                "transcript_type": "protein_coding", 
                "gene_id": "ENSG00000167578.10", 
                "transcript_id": "ENST00000378307.4", 
                "transcript_name": "MIA-203", 
                "gene_type": "protein_coding", 
                "transcript_status": "KNOWN", 
                "gene_name": "MIA"
              }, 
              "frame": ".", 
              "feature": "exon", 
              "source": "ENSEMBL", 
              "score": ".", 
              "strand": "+"
            }, 
            {
              "seqname": "chr19", 
              "end": 41292883, 
              "start": 41292753, 
              "attribute": {
                "gene_status": "KNOWN", 
                "level": "3", 
                "transcript_type": "protein_coding", 
                "gene_id": "ENSG00000167578.10", 
                "transcript_id": "ENST00000378307.4", 
                "transcript_name": "MIA-203", 
                "gene_type": "protein_coding", 
                "transcript_status": "KNOWN", 
                "gene_name": "MIA"
              }, 
              "frame": ".", 
              "feature": "exon", 
              "source": "ENSEMBL", 
              "score": ".", 
              "strand": "+"
            }, 
            {
              "seqname": "chr19", 
              "end": 41302847, 
              "start": 41302475, 
              "attribute": {
                "gene_status": "KNOWN", 
                "level": "3", 
                "transcript_type": "protein_coding", 
                "gene_id": "ENSG00000167578.10", 
                "transcript_id": "ENST00000378307.4", 
                "transcript_name": "MIA-203", 
                "gene_type": "protein_coding", 
                "transcript_status": "KNOWN", 
                "gene_name": "MIA"
              }, 
              "frame": ".", 
              "feature": "exon", 
              "source": "ENSEMBL", 
              "score": ".", 
              "strand": "+"
            }
          ], 
          "start": 41284213, 
          "attribute": {
            "gene_status": "KNOWN", 
            "level": "3", 
            "transcript_type": "protein_coding", 
            "gene_id": "ENSG00000167578.10", 
            "transcript_id": "ENST00000378307.4", 
            "transcript_name": "MIA-203", 
            "gene_type": "protein_coding", 
            "transcript_status": "KNOWN", 
            "gene_name": "MIA"
          }, 
          "frame": ".", 
          "feature": "transcript", 
          "source": "ENSEMBL", 
          "score": ".", 
          "strand": "+"
        }, 
        "ENST00000419646.2": {
          "seqname": "chr19", 
          "end": 41289707, 
          "exons": [
            {
              "seqname": "chr19", 
              "end": 41277968, 
              "start": 41277553, 
              "attribute": {
                "gene_status": "KNOWN", 
                "level": "3", 
                "transcript_type": "protein_coding", 
                "gene_id": "ENSG00000167578.10", 
                "transcript_id": "ENST00000419646.2", 
                "transcript_name": "MIA-204", 
                "gene_type": "protein_coding", 
                "transcript_status": "KNOWN", 
                "gene_name": "MIA"
              }, 
              "frame": ".", 
              "feature": "exon", 
              "source": "ENSEMBL", 
              "score": ".", 
              "strand": "+"
            }, 
            {
              "seqname": "chr19", 
              "end": 41281574, 
              "start": 41281442, 
              "attribute": {
                "gene_status": "KNOWN", 
                "level": "3", 
                "transcript_type": "protein_coding", 
                "gene_id": "ENSG00000167578.10", 
                "transcript_id": "ENST00000419646.2", 
                "transcript_name": "MIA-204", 
                "gene_type": "protein_coding", 
                "transcript_status": "KNOWN", 
                "gene_name": "MIA"
              }, 
              "frame": ".", 
              "feature": "exon", 
              "source": "ENSEMBL", 
              "score": ".", 
              "strand": "+"
            }, 
            {
              "seqname": "chr19", 
              "end": 41281790, 
              "start": 41281657, 
              "attribute": {
                "gene_status": "KNOWN", 
                "level": "3", 
                "transcript_type": "protein_coding", 
                "gene_id": "ENSG00000167578.10", 
                "transcript_id": "ENST00000419646.2", 
                "transcript_name": "MIA-204", 
                "gene_type": "protein_coding", 
                "transcript_status": "KNOWN", 
                "gene_name": "MIA"
              }, 
              "frame": ".", 
              "feature": "exon", 
              "source": "ENSEMBL", 
              "score": ".", 
              "strand": "+"
            }, 
            {
              "seqname": "chr19", 
              "end": 41282984, 
              "start": 41282874, 
              "attribute": {
                "gene_status": "KNOWN", 
                "level": "3", 
                "transcript_type": "protein_coding", 
                "gene_id": "ENSG00000167578.10", 
                "transcript_id": "ENST00000419646.2", 
                "transcript_name": "MIA-204", 
                "gene_type": "protein_coding", 
                "transcript_status": "KNOWN", 
                "gene_name": "MIA"
              }, 
              "frame": ".", 
              "feature": "exon", 
              "source": "ENSEMBL", 
              "score": ".", 
              "strand": "+"
            }, 
            {
              "seqname": "chr19", 
              "end": 41286004, 
              "start": 41285924, 
              "attribute": {
                "gene_status": "KNOWN", 
                "level": "3", 
                "transcript_type": "protein_coding", 
                "gene_id": "ENSG00000167578.10", 
                "transcript_id": "ENST00000419646.2", 
                "transcript_name": "MIA-204", 
                "gene_type": "protein_coding", 
                "transcript_status": "KNOWN", 
                "gene_name": "MIA"
              }, 
              "frame": ".", 
              "feature": "exon", 
              "source": "ENSEMBL", 
              "score": ".", 
              "strand": "+"
            }, 
            {
              "seqname": "chr19", 
              "end": 41286404, 
              "start": 41286290, 
              "attribute": {
                "gene_status": "KNOWN", 
                "level": "3", 
                "transcript_type": "protein_coding", 
                "gene_id": "ENSG00000167578.10", 
                "transcript_id": "ENST00000419646.2", 
                "transcript_name": "MIA-204", 
                "gene_type": "protein_coding", 
                "transcript_status": "KNOWN", 
                "gene_name": "MIA"
              }, 
              "frame": ".", 
              "feature": "exon", 
              "source": "ENSEMBL", 
              "score": ".", 
              "strand": "+"
            }, 
            {
              "seqname": "chr19", 
              "end": 41289707, 
              "start": 41289683, 
              "attribute": {
                "gene_status": "KNOWN", 
                "level": "3", 
                "transcript_type": "protein_coding", 
                "gene_id": "ENSG00000167578.10", 
                "transcript_id": "ENST00000419646.2", 
                "transcript_name": "MIA-204", 
                "gene_type": "protein_coding", 
                "transcript_status": "KNOWN", 
                "gene_name": "MIA"
              }, 
              "frame": ".", 
              "feature": "exon", 
              "source": "ENSEMBL", 
              "score": ".", 
              "strand": "+"
            }
          ], 
          "start": 41277553, 
          "attribute": {
            "gene_status": "KNOWN", 
            "level": "3", 
            "transcript_type": "protein_coding", 
            "gene_id": "ENSG00000167578.10", 
            "transcript_id": "ENST00000419646.2", 
            "transcript_name": "MIA-204", 
            "gene_type": "protein_coding", 
            "transcript_status": "KNOWN", 
            "gene_name": "MIA"
          }, 
          "frame": ".", 
          "feature": "transcript", 
          "source": "ENSEMBL", 
          "score": ".", 
          "strand": "+"
        }, 
        "ENST00000357052.2": {
          "seqname": "chr19", 
          "end": 41302847, 
          "exons": [
            {
              "seqname": "chr19", 
              "end": 41284296, 
              "start": 41284171, 
              "attribute": {
                "gene_status": "KNOWN", 
                "level": "3", 
                "transcript_type": "protein_coding", 
                "tag": "CCDS", 
                "gene_id": "ENSG00000167578.10", 
                "transcript_id": "ENST00000357052.2", 
                "ccdsid": "CCDS33030.1", 
                "transcript_name": "MIA-202", 
                "gene_type": "protein_coding", 
                "transcript_status": "KNOWN", 
                "gene_name": "MIA"
              }, 
              "frame": ".", 
              "feature": "exon", 
              "source": "ENSEMBL", 
              "score": ".", 
              "strand": "+"
            }, 
            {
              "seqname": "chr19", 
              "end": 41286004, 
              "start": 41285924, 
              "attribute": {
                "gene_status": "KNOWN", 
                "level": "3", 
                "transcript_type": "protein_coding", 
                "tag": "CCDS", 
                "gene_id": "ENSG00000167578.10", 
                "transcript_id": "ENST00000357052.2", 
                "ccdsid": "CCDS33030.1", 
                "transcript_name": "MIA-202", 
                "gene_type": "protein_coding", 
                "transcript_status": "KNOWN", 
                "gene_name": "MIA"
              }, 
              "frame": ".", 
              "feature": "exon", 
              "source": "ENSEMBL", 
              "score": ".", 
              "strand": "+"
            }, 
            {
              "seqname": "chr19", 
              "end": 41286404, 
              "start": 41286290, 
              "attribute": {
                "gene_status": "KNOWN", 
                "level": "3", 
                "transcript_type": "protein_coding", 
                "tag": "CCDS", 
                "gene_id": "ENSG00000167578.10", 
                "transcript_id": "ENST00000357052.2", 
                "ccdsid": "CCDS33030.1", 
                "transcript_name": "MIA-202", 
                "gene_type": "protein_coding", 
                "transcript_status": "KNOWN", 
                "gene_name": "MIA"
              }, 
              "frame": ".", 
              "feature": "exon", 
              "source": "ENSEMBL", 
              "score": ".", 
              "strand": "+"
            }, 
            {
              "seqname": "chr19", 
              "end": 41289745, 
              "start": 41289683, 
              "attribute": {
                "gene_status": "KNOWN", 
                "level": "3", 
                "transcript_type": "protein_coding", 
                "tag": "CCDS", 
                "gene_id": "ENSG00000167578.10", 
                "transcript_id": "ENST00000357052.2", 
                "ccdsid": "CCDS33030.1", 
                "transcript_name": "MIA-202", 
                "gene_type": "protein_coding", 
                "transcript_status": "KNOWN", 
                "gene_name": "MIA"
              }, 
              "frame": ".", 
              "feature": "exon", 
              "source": "ENSEMBL", 
              "score": ".", 
              "strand": "+"
            }, 
            {
              "seqname": "chr19", 
              "end": 41289980, 
              "start": 41289826, 
              "attribute": {
                "gene_status": "KNOWN", 
                "level": "3", 
                "transcript_type": "protein_coding", 
                "tag": "CCDS", 
                "gene_id": "ENSG00000167578.10", 
                "transcript_id": "ENST00000357052.2", 
                "ccdsid": "CCDS33030.1", 
                "transcript_name": "MIA-202", 
                "gene_type": "protein_coding", 
                "transcript_status": "KNOWN", 
                "gene_name": "MIA"
              }, 
              "frame": ".", 
              "feature": "exon", 
              "source": "ENSEMBL", 
              "score": ".", 
              "strand": "+"
            }, 
            {
              "seqname": "chr19", 
              "end": 41292665, 
              "start": 41292570, 
              "attribute": {
                "gene_status": "KNOWN", 
                "level": "3", 
                "transcript_type": "protein_coding", 
                "tag": "CCDS", 
                "gene_id": "ENSG00000167578.10", 
                "transcript_id": "ENST00000357052.2", 
                "ccdsid": "CCDS33030.1", 
                "transcript_name": "MIA-202", 
                "gene_type": "protein_coding", 
                "transcript_status": "KNOWN", 
                "gene_name": "MIA"
              }, 
              "frame": ".", 
              "feature": "exon", 
              "source": "ENSEMBL", 
              "score": ".", 
              "strand": "+"
            }, 
            {
              "seqname": "chr19", 
              "end": 41292883, 
              "start": 41292753, 
              "attribute": {
                "gene_status": "KNOWN", 
                "level": "3", 
                "transcript_type": "protein_coding", 
                "tag": "CCDS", 
                "gene_id": "ENSG00000167578.10", 
                "transcript_id": "ENST00000357052.2", 
                "ccdsid": "CCDS33030.1", 
                "transcript_name": "MIA-202", 
                "gene_type": "protein_coding", 
                "transcript_status": "KNOWN", 
                "gene_name": "MIA"
              }, 
              "frame": ".", 
              "feature": "exon", 
              "source": "ENSEMBL", 
              "score": ".", 
              "strand": "+"
            }, 
            {
              "seqname": "chr19", 
              "end": 41302847, 
              "start": 41302475, 
              "attribute": {
                "gene_status": "KNOWN", 
                "level": "3", 
                "transcript_type": "protein_coding", 
                "tag": "CCDS", 
                "gene_id": "ENSG00000167578.10", 
                "transcript_id": "ENST00000357052.2", 
                "ccdsid": "CCDS33030.1", 
                "transcript_name": "MIA-202", 
                "gene_type": "protein_coding", 
                "transcript_status": "KNOWN", 
                "gene_name": "MIA"
              }, 
              "frame": ".", 
              "feature": "exon", 
              "source": "ENSEMBL", 
              "score": ".", 
              "strand": "+"
            }
          ], 
          "start": 41284171, 
          "attribute": {
            "gene_status": "KNOWN", 
            "level": "3", 
            "transcript_type": "protein_coding", 
            "tag": "CCDS", 
            "gene_id": "ENSG00000167578.10", 
            "transcript_id": "ENST00000357052.2", 
            "ccdsid": "CCDS33030.1", 
            "transcript_name": "MIA-202", 
            "gene_type": "protein_coding", 
            "transcript_status": "KNOWN", 
            "gene_name": "MIA"
          }, 
          "frame": ".", 
          "feature": "transcript", 
          "source": "ENSEMBL", 
          "score": ".", 
          "strand": "+"
        }
      }, 
      "strand": "+"
    }
