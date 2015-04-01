Things that need to be done
---------------------------

* Take json of TSS coordinates and pull RNA-seq data into TSS data
* Get list of splice coordinates
* Write machine learning fun stuff

Things Jeff is Working On
-------------------------

###Priority:###
* ~~GTF class~~ -- **DONE**
* Import GTF file -- **CAN DO**
* Filter GTF file for feature or attributes -- **HACKED/DONE**
* Produce a list of TSS coordinate in json format -- **IN PROGRESS**

###Other Things:###
* Package GTF utils into one file
* Documentation

Things Brian is Working On
--------------------------

###Priority###
* ~~Write first iteration of ChIP-Seq read count extraction~~ -- **DONE**
* Download additional ChIP-Seq Tag files -- **much check memory requirements**
* ~~Update find_sites.py to take experiment ID and sample ID as command line argumentsand carry them into the output~~ -- **DONE**
* Write bash script to automate the running of this script once the TSS coordinates are available **CAN DO (pending run-time constraints)**
* ~~update find_sites.py to take gene orientation into account~~ -- **DONE**

###Other Things###
* Use ChIP-Seq Metadata to scale read-count by number of reads in experiment
* Find out if a logistic model can be trained if not all data points have every feature defined
* consider inclduding expression of snRNAs as additona features in the feature vector we train on.


###Additional things to think about/relevant papers###
http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2276655/pdf/nihms35172.pdf
        -H3K4me3 leads to recruitment of splicing factors
        -out of James Manleys goup


http://liulab.dfci.harvard.edu/publications/Kolasinska_H3K36me3_NatGen_2009.pdf
        -H3K36me3 at lower levels in AS exons
        -shirley Liu is a former student of Marty

null hypothesis supported by role of snRNAs:
http://en.wikipedia.org/wiki/Small_nuclear_RNA
 
Should we consider final exons? Perhaps their are signals for end of transcription (e.g.histone marks recruiting factors that end transcription)

When considering AS, it seems that for the 3 prime exon sites, we are primarily concerned with the state of the around the adenosine 20-40 bp upstream of the exon start that attacks the 5 prime exon end.
For 5 prime exon sites, we are concerned with the sequences downstream of the end of the exon.

