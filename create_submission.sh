#!/bin/bash

DATADIR=$1
SUFFIX=$2

rm -f /tmp/foo.$$
touch /tmp/foo.$$

for fullfile in ${DATADIR}/*.${SUFFIX}
do
    sanssuffix=${fullfile%%.*}
    sampleid=${sanssuffix##*/}
    awk -v OFS=, -v sampleid=$sampleid '{print sampleid, $0}' < $fullfile >> /tmp/foo.$$
done

cat /tmp/foo.$$
rm /tmp/foo.$$
