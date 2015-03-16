# This function calls awk to collapse a single ngram gzip file,
# summing the frequencies over all years. Wrap it in a bash function
# to avoid needing to escape everything for parallel
collapse_ngrams() {
  OUT=$(basename $1 .gz).bz2
  gzcat $1 | ~/Documents/Workspace/kaggle/BillionWordImputation/scripts/BillionWordImputation/build/Release/collapse_ngrams | pbzip2 -c > $OUT
}

export -f collapse_ngrams
# Run 8 awk processes, pipe them all into a single Python script
# The awk process is rate-limiting. Unfortunately if one of the files
# is much larger than the others, it will be rate-limiting, but the
# files need to be processed serially. Process the files in order
# of decreasing size, so that the longest-running file starts first,
# and smaller files can backfill.
ls -S *.gz | parallel -j 8 -k collapse_ngrams {}