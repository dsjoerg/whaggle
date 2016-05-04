import csv, math, requests, StringIO
from collections import defaultdict

def download_truth():
    r =  requests.get('https://gist.githubusercontent.com/dsjoerg/0c93acfe7853ba26d692dc7ceac9d9ef/raw/e538c40194fc3d66bec2a0f6bc738c05e0af2a93/gistfile1.txt')
    return r.text

def download_sample_submission():
    r =  requests.get('https://gist.github.com/dsjoerg/31dc30981d59016df8c174b1960372d8/raw/b81ae0ba99b5666f725607d216b285a2f2b2787d/gistfile1.txt')
    return r.text
    
def parse_entry(entry, entrytype):
    ''' parse a big set of lines of format
    timestamp,value
    
    into a list of lists of [sampleid, timestamp, entrytype, value]
    '''
    result = list()
    f = StringIO.StringIO(entry)
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        result.append([row[0], row[1], entrytype, float(row[2])])
    return result
    
truth_entry = download_truth()
truth = parse_entry(truth_entry, 'truth')

def compute_score(submission_entry, debug):
    submission = parse_entry(submission_entry, 'submission')
    together = sorted(truth + submission, key=lambda x: x[1])
    sumsq = defaultdict(int)
    count = defaultdict(int)
    latest_submission = dict()
    for item in together:
        sampleid = item[0]
        entrytype = item[2]
        itemvalue = item[3]
        if entrytype == 'submission':
            latest_submission[sampleid] = item
        else:
            if sampleid in latest_submission:
                submission_value = latest_submission[sampleid][3]
            else:
                submission_value = 0
            sumsq[sampleid] = sumsq[sampleid] + ((itemvalue - submission_value) ** 2)
            count[sampleid] = count[sampleid] + 1

    sum_rmse = 0
    for sampleid in sumsq:
        rmse = math.sqrt(sumsq[sampleid] / count[sampleid])
        if debug:
            # NOTE that this debug output MUST NOT be shown on the website or to competitors
            print('For sample %s, RMSE is %f' % (sampleid, rmse))
        sum_rmse = sum_rmse + rmse

    avg_rmse = sum_rmse / len(sumsq)
    if debug:
        print('Submission score = avg RMSE = %f' % (avg_rmse))
    return avg_rmse


def do_sample_example():
    sample_entry = download_sample_submission()
    score = compute_score(sample_entry, True)

if __name__ == '__main__':
    do_sample_example()
