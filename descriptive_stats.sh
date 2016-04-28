#!/bin/bash

DIR_TO_ANALYZE=$1
MAX_ROWS=$2
echo "hi, analyzing ${DIR_TO_ANALYZE} limiting myself to ${MAX_ROWS} per file"

for fname in ${DIR_TO_ANALYZE}/*;
do
    echo "TIME RANGE for ${fname}"
    tail +3 ${fname}  | head -1 | awk '{print "first timestamp: ", $1}'
    tail -1 ${fname}  | awk '{print "last timestamp: ", $1}'
done
             

for i in `seq 2 4`;
do
    echo "COLUMN ${i} of ACCELEROMETER"
    tail +3 ${DIR_TO_ANALYZE}/*.acc  | head -${MAX_ROWS} | awk '{print $'"${i}"'}' | histogram.py
done

for i in `seq 2 8`;
do
    echo "COLUMN ${i} of AGC"
    tail +3 ${DIR_TO_ANALYZE}/*.agc  | head -${MAX_ROWS} | awk '{print $'"${i}"'}' | histogram.py
done

for i in `seq 2 3`;
do
    echo "COLUMN ${i} of OPT"
    tail +3 ${DIR_TO_ANALYZE}/*.opt  | head -${MAX_ROWS} | awk '{print $'"${i}"'}' | histogram.py
done

echo "PY.HR"
tail +3 ${DIR_TO_ANALYZE}/*.py.hr.txt  | head -${MAX_ROWS} | awk -F, '{print $2}' | histogram.py

echo "TRUTH"
tail +3 ${DIR_TO_ANALYZE}/*.truth  | head -${MAX_ROWS} | awk -F, '{print $2}' | histogram.py
