#!/bin/bash

# compute score for a set of samples, by looking back for the most recent contestant heart-rate estimate

THEDIR=$1
MAXROWS=$2
echo "Looking at ${THEDIR}."

TRUTHFILES=$THEDIR/*.truth

for truthfile in $TRUTHFILES;
do
    prefix=${truthfile%.truth}
    head -${MAXROWS} ${prefix}.py.hr.txt  | awk -v OFS=, '{print "PYHR", $0}' > /tmp/foo.$$
    head -${MAXROWS} ${prefix}.truth  | awk -v OFS=, '{print "TRUTH", $0}' >> /tmp/foo.$$
    sort -t, -n -k2,2 /tmp/foo.$$ | awk -F, -v OFS=, '$1 == "PYHR" {latest_pyhr = $3} $1 == "TRUTH" {print $0, latest_pyhr}' > /tmp/joined.$$
    RMSE=$( awk -F, 'BEGIN { sumsq=0; count=0} { sumsq += ($4 - $3)**2; count++} END {print sqrt(sumsq/count)}' /tmp/joined.$$)
    echo ${prefix##*/} $RMSE
done
