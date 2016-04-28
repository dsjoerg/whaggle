#!/bin/bash

# compute score for each truth sample, by looking back for the most recent contestant heart-rate estimate

THEDIR=$1
echo -n "For ${THEDIR}, "

./join_truth_to_pyhr.sh ${THEDIR} 1000000 > ${THEDIR}/joined.csv
awk -F, 'BEGIN { sumsq=0; count=0} { sumsq += ($4 - $3)**2; count++} END {print "RMSE score =", sqrt(sumsq/count)}' ${THEDIR}/joined.csv
echo
awk -F, '{ print ($4 - $3) }' ${THEDIR}/joined.csv | histogram.py
