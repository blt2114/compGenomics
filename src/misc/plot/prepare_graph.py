__author__ = 'jeffrey'

from src.utils import FileProgress

fn = "out/nosplice_tss_chip.tsv.sort"
progress = FileProgress(fn, "Percent: ")

with open(fn) as f:
    for line in f:
        row = line.strip("\n").split("\t")
        if len(row) != 5:
            progress.update()
            continue
        seqname = row[0]
        pos = row[1]
        sample = row[2]
        mark = row[3]
        rpm = eval(row[4])

        print mark + "\t" + "\t".join(map(str, rpm))
        progress.update()

