#!/usr/bin/env python

import os, re, shutil, sys, xlrd
from random import shuffle
from collections import Counter, defaultdict

def extract_date(date_time_and_id):
    thing = re.match('([0-9]+)_.*', date_time_and_id)
    return thing.group(1)

def extract_time(date_time_and_id):
    thing = re.match('([0-9]+)_([0-9]+).*', date_time_and_id)
    return thing.group(2)

def extract_duas_dict(row):
    date = extract_date(row[0])
    return {'date': date,
            'user': row[2],
            'activity': row[3],
            'skintone': row[18]}

def extract_duas(row):
    date = extract_date(row[0])
    return [date, row[2], row[3], row[18]]

def build_skintone_dict(sh):
    # remember what is the first skintone we saw for each user
    user_skintone = dict()
    for rownum in range(2, sh.nrows):
        row = sh.row_values(rownum)
        user = row[2]
        skintone = row[18]
        if (user not in user_skintone) and skintone:
            user_skintone[user] = skintone
    return user_skintone

def sublist_summary(sublist_name, sublist):
    print sublist_name, 'num # date-user-activity combinations:', len(sublist)
    print sublist_name, 'activities:', Counter([duas[2] for duas in sublist]).most_common()
    print sublist_name, 'skintones:', Counter([duas[3] for duas in sublist]).most_common()
    print sublist_name, 'date-user-activity examples:', sublist[0:3]

def do_it(data_table_path, sampleroot):

    # open excel file
    wb = xlrd.open_workbook(data_table_path)
    sh = wb.sheet_by_index(0)

    # note the first reported skintone for each user
    user_skintone = build_skintone_dict(sh)

    # read in unique combinations of date, user, activity, skinton
    duas_set = set()
    duas_to_dtui = defaultdict(list)
    for rownum in range(2, sh.nrows):
        row = sh.row_values(rownum)
        duas = extract_duas(row)
        # set the users skintone to the first skintone seen
        user = duas[1]
        if user in user_skintone:
            duas[3] = user_skintone[user]
        duas_set.add(tuple(duas))

        date = extract_date(row[0])
        time = extract_time(row[0])
        dtui = (date + '_' + time + '_' + str(int(row[1]))).encode('ascii')
        duas_to_dtui[tuple(duas)].append(dtui)
                
    print 'There are', len(duas_set), 'distinct DUAS combinations.'

    # sort by activity and then skintone
    duas_list = list(duas_set)
    sorted_duas_list = sorted(duas_list, key=lambda duas: str(duas[2]) + '_' + str(duas[3]))

    # divide sorted list into sublists
    training = sorted_duas_list[::4] + sorted_duas_list[1::4]
    leaderboard = sorted_duas_list[2::4]
    test = sorted_duas_list[3::4]

    # report on each group's distribution of activity and skintone
    for name, sublist in [('training', training), ('leaderboard', leaderboard), ('test', test)]:
        sublist_summary(name, sublist)
        dtuis = [item for duas in sublist for item in duas_to_dtui[tuple(duas)]]
        print len(dtuis), name, 'dtuis:', dtuis[0:5]
        print


    training_dtuis = [item for duas in training for item in duas_to_dtui[tuple(duas)]]
    leaderboard_dtuis = [item for duas in leaderboard for item in duas_to_dtui[tuple(duas)]]
    test_dtuis = [item for duas in test for item in duas_to_dtui[tuple(duas)]]
    
    # move files around accordingly
    #
    # *.truth --> {training -> contestant_data/train,
    #              leaderboard -> leaderboard_truth,
    #              test -> test_truth}
    # everything else --> {training -> contestant_data/train,
    #                      leaderboard -> contestant_data/leaderboard_and_final,
    #                      test        -> contestant_data/leaderboard_and_final}
    #
    for dirpath, dirs, files in os.walk(sampleroot):
        for filename in files:
            dtui_match = re.match('([0-9]+_[0-9]+_[0-9]+).*', filename)
            dest = None
            if dtui_match:
                # only move files that contain sample data
                dtui = dtui_match.group(1)
                if filename.endswith('truth'):
                    # only truth files get moved into the sensitive *_truth directories
                    if dtui in training_dtuis:
                        # but the training data stays in the samples directory
                        dest = 'contestant_data/train'
                    elif dtui in leaderboard_dtuis:
                        dest = 'leaderboard_truth'
                    elif dtui in test_dtuis:
                        dest = 'test_truth'
                else:
                    if dtui in training_dtuis:
                        dest = 'contestant_data/train'
                    elif dtui in leaderboard_dtuis:
                        dest = 'contestant_data/leaderboard_and_final'
                    elif dtui in test_dtuis:
                        dest = 'contestant_data/leaderboard_and_final'

            if False:
                if dest:
                    print filename, 'to be moved to', dest
                else:
                    print filename, 'should be left alone'

            if dest:
                # first check if dest exists with os.path.isfile() and dont do it if it does
                fulldest = os.path.join(sampleroot, dest)
#                print 'fulldest=', fulldest
                if os.path.isfile(fulldest):
                    print 'hmm, a file is already there, cowardly doing nothing'
                else:
#                    print 'could move it'
                    if dirpath != fulldest:
                        fullsrc = os.path.join(dirpath, filename)
                        if os.path.isfile(fullsrc):
#                            print 'src file:', fullsrc, 'exists'
                            shutil.move(fullsrc, fulldest)
                        else:
                            print 'src file:', fullsrc, 'DOES NOT EXIST WTF'
                    else:
#                        print 'Not moving, its already there'
                        pass
        
if __name__ == '__main__':
    do_it(sys.argv[1], sys.argv[2])


#  Assignment procedure:
#  * read in the xlsx
#  * correct skintones for the 6 who were messed up
#  * list the unique combinations of user-date-activity-skintone
#  * sort by activity and then skintone
#  * walk through picking 2 for train, 1 for leaderboard, 1 for test, and repeat
#  * report on each group's distribution of activity and skintone
