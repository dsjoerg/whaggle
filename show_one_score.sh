#!/bin/bash

# compute score for each truth sample, by looking back for the most recent contestant heart-rate estimate

THEDIR=$1
DT_UID=$2
MAXROWS=10000000

echo -n "For ${THEDIR}/${DT_UID}: "

TRUTHFILES=$THEDIR/${DT_UID}.truth

for truthfile in $TRUTHFILES;
do
    prefix=${truthfile%.truth}
    head -${MAXROWS} ${prefix}.py.hr.txt  | awk -v OFS=, '{print "PYHR", $0}' > /tmp/foo.$$
    head -${MAXROWS} ${prefix}.truth  | awk -v OFS=, '{print "TRUTH", $0}' >> /tmp/foo.$$
    sort -t, -n -k2,2 /tmp/foo.$$ > /tmp/sorted.$$
    cat /tmp/sorted.$$ | awk -F, -v OFS=, '$1 == "PYHR" {latest_pyhr = $3} $1 == "TRUTH" {print $0, latest_pyhr}' > /tmp/joined.$$
    RMSE=$( awk -F, 'BEGIN { sumsq=0; count=0} { sumsq += ($4 - $3)**2; count++} END {print sqrt(sumsq/count)}' /tmp/joined.$$)
    echo ${prefix##*/} $RMSE

    echo ''
    echo 'distribution of TRUTH:'
    awk -F, '{ print ($3) }' /tmp/joined.$$ | histogram.py
    echo ''
    
    echo 'distribution of PYHR:'
    awk -F, '{ print ($4) }' /tmp/joined.$$ | histogram.py
    echo ''

    echo 'distribution of ERROR:'
    awk -F, '{ print ($4 - $3) }' /tmp/joined.$$ | histogram.py
done
