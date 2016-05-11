#!/usr/bin/env python

import re, sys, xlrd
from random import shuffle
from collections import Counter

def extract_date(date_time_and_id):
    thing = re.match('([0-9]+)_.*', date_time_and_id)
    return thing.group(1)

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
    print sublist_name, 'size:', len(sublist)
    print sublist_name, 'activities:', Counter([duas[2] for duas in sublist]).most_common()
    print sublist_name, 'skintones:', Counter([duas[3] for duas in sublist]).most_common()

def do_it(data_table_path):

    # open excel file
    wb = xlrd.open_workbook(data_table_path)
    sh = wb.sheet_by_index(0)

    # note the first reported skintone for each user
    user_skintone = build_skintone_dict(sh)

    # read in unique combinations of date, user, activity, skinton
    duas_set = set()
    for rownum in range(2, sh.nrows):
        duas = extract_duas(sh.row_values(rownum))
        # set the users skintone to the first skintone seen
        user = duas[1]
        if user in user_skintone:
            duas[3] = user_skintone[user]
        duas_set.add(tuple(duas))
    print 'There are', len(duas_set), 'distinct DUAS combinations.'

    # sort by activity and then skintone
    duas_list = list(duas_set)
    sorted_duas_list = sorted(duas_list, key=lambda duas: str(duas[2]) + '_' + str(duas[3]))

    # divide sorted list into sublists
    training = sorted_duas_list[::4] + sorted_duas_list[1::4]
    leaderboard = sorted_duas_list[2::4]
    test = sorted_duas_list[3::4]

    sublist_summary('training', training)
    sublist_summary('leaderboard', leaderboard)
    sublist_summary('test', test)
    

if __name__ == '__main__':
    do_it(sys.argv[1])


#  Assignment procedure:
#  * read in the xlsx
#  * correct skintones for the 6 who were messed up
#  * list the unique combinations of user-date-activity-skintone
#  * sort by activity and then skintone
#  * walk through picking 2 for train, 1 for leaderboard, 1 for test, and repeat
#  * report on each group's distribution of activity and skintone
