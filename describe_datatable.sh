#!/bin/bash

DATATABLE_FILE=$1
xlsx2csv $1 > /tmp/datatable.$$

NUMCOLS=$( cat /tmp/datatable.$$ | head -1 | awk -F, '{print NF}' )

for i in `seq 1 $NUMCOLS`;
do
    COLNAME=$( head -1 /tmp/datatable.$$ | awk -F, '{print $'$i'}' )
    echo -n "column $i: $COLNAME" 
    cat /tmp/datatable.$$ | awk -F, '{print $'$i'}' | tail +2 | sort | uniq -c | wc -l
done
