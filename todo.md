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
* Write script to break output of ChIP_extract.py into individual experiment (i.e. by gene or by tissue type)
* Use ChIP-Seq Metadata to scale read-count by number of reads in experiment


###Other Things###
* Find out if a logistic model can be trained if not all data points have every feature defined
* consider inclduding expression of snRNAs as additona features in the feature vector we train on.

###Completed###
* ~~Write first iteration of ChIP-Seq read count extraction~~ -- **DONE**
* ~~Update find_sites.py to take experiment ID and sample ID as command line argumentsand carry them into the output~~ -- **DONE**
* ~~update find_sites.py to take gene orientation into account~~ -- **DONE**
* ~~Write bash script to automate the running of this script once the TSS coordinates are available~~ -- **DONE**
        -download, decompress, parse revelant info and delete continuously
* ~~Script to break up list of experiments into chunks and run extract_chip.sh~~ -- **DONE**
* ~~Python Script to merge the results from multiple outputs of extract_ChIP.sh~~ -- **DONE**
* ~~Python Script to sort JSON dictionaries by chromosome and location~~ -- **DONE**

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

Consider ignoring splicing that does not go through the major splicing pathway
        -It is possible that the selection mechanisms are different from the major pathways so including them may introduce noise into our data.

Consider adding reads within upstream/ dowstream ranges as separate features

###TSS###
#####Possible Experimental Question:#####
For genes with two TSS observed in our data set, can histone state around these sites predict which TSS predominates?

#####General Data Subset Selection#####
Limit data pool to the set of genes, G, such that for every g_i in G
* g_i has exactly two observed TSS in our data-set
* The two TSSs of g_i are sufficiently separated to be differentiaed by ChIP labels (ideally ~1Kb cutoff)
* A significant portion of cell-line samples use the other TSS (perhaps ~20% cutoff)
**drop data points from samples where the level of expression is below some threshold

#####Feature Vectors and Labels#####
For all g_i in G, we will have a feature vector x_i and a label y_i.
*x_i is a 10 dimentional vector, 5 dimensions representing the states of the core histone marks for each TSS.
*y_i is a real number, that is the portion of transcripts that used the first site 
**we can consider binarizing this (e.g. TSS 1 is most frequently used)

###AS###

