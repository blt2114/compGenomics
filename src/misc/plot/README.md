Plotting the Density Around the ChIP-seq data
=============================================

The input into this workflow is the tab-separated values produced by the chip extraction step of either
workflow.

As usual, it may be necessary to add the application root to pythonpath to run scripts.

### Step 1: Pre-process the tab-separated list ###

Run:

   python src/misc/plot/prepare_graph.py <path_to_tsv_file> > chip_for_plotting.tsv

Depending on the size of the file, this may take some time.

Now open R and run the following commands (for variance):

    tbl <- read.table("graph.tsv", sep="\t", header=F)
    colnames(tbl)[1] <- mark
    results = by(tbl[,-1], tbl$mark, function(x) {apply(x,2,var)})
    results2 = do.call(rbind, results)
    write.table(results2, "vars.tsv", sep="\t")

Now open R and run the following commands (for sums):

    results = by(tbl[,-1], tbl$mark, colSums)
    results2 = do.call(rbind, results)
    write.table(results2, "vars.tsv", sep="\t")
    
Now load the files into a spreadsheet and plot away!