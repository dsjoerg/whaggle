#!/bin/bash

TRUTHDIR=$1

rm -f /tmp/foo.$$
touch /tmp/foo.$$

for fullfile in $TRUTHDIR/*.truth
do
    sanssuffix=${fullfile%%.*}
    sampleid=${sanssuffix##*/}
    awk -v OFS=, -v sampleid=$sampleid '{print sampleid, $0}' < $fullfile >> /tmp/foo.$$
done

cat /tmp/foo.$$
rm /tmp/foo.$$
