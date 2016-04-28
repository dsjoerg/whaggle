#!/bin/bash

SUBMITDIR=$1
MAXROWS=$2
echo "Scoring ${SUBMITDIR}, looking only at the first ${MAXROWS} rows."

head -${MAXROWS} ${SUBMITDIR}/*.py.hr.txt  | awk -v OFS=, '{print "PYHR", $0}' > /tmp/foo.$$
head -${MAXROWS} ${SUBMITDIR}/*.truth  | awk -v OFS=, '{print "TRUTH", $0}' >> /tmp/foo.$$
sort -t, -n -k2,2 /tmp/foo.$$ | awk -F, -v OFS=, '$1 == "PYHR" {latest_pyhr = $3} $1 == "TRUTH" {print $0, latest_pyhr}'
