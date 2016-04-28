#!/bin/bash

THEDIR=$1
echo "Computing score for ${THEDIR}"

./join_truth_to_pyhr.sh ${THEDIR} 1000000 > ${THEDIR}/joined.csv
awk -F, 'BEGIN { sum=0; count=0} { sum += ($4 - $3)**2; count++} END {print count, sum/count, sqrt(sum/count)}' ${THEDIR}/joined.csv