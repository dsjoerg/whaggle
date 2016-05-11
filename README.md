
# requirements

`pip install data_hacks` (https://github.com/bitly/data_hacks)


# to compute score for a directory

`./compute_score.sh samples_20160426/running/`

or

`for dir in samples_20160426/*; do ./compute_score.sh $dir; echo; echo; done`


# to get some basic descriptive statistics on a directory

`./descriptive_stats.sh samples_20160426/running 100000000`


# to try the python scoring function

`python scorer.py`


# to look at distributions of truth and pyhr from one sample

`./show_one_score.sh 20160510_from_ritscher_working_copy/tltraw 160224_190025_740`
