#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import glob
import os


def getBugCount():
    bugCount = 0

    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    for file in glob.glob("*.json"):
        data = json.loads(open(file).read())

        for bug in data['bugs']:
            bugCount += 1
        # print data['bugs'][]['summary']
    print bugCount


def getAllSummaries():
    summaries = []
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    for file in glob.glob("*.json"):
        data = json.loads(open(file).read())
        for bug in data['bugs']:
            summaries.append(bug['summary'].encode('utf-8'))
    list = open('summaryList.txt', 'w')
    for item in summaries:
        list.write('{0}\n'.format(item))
    list.close()


#getBugCount()
#getAllSummaries()
