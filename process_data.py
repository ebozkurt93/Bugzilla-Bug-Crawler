#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import glob
import os
import fnmatch


def getBugCount(files):
    totalBugCount = 0
    passedLimit = []
    # abspath = os.path.abspath(__file__)
    # dname = os.path.dirname(abspath)
    # os.chdir(dname)
    # for file in glob.glob("*.json"):
    for file in files:
        data = json.loads(open(file).read())
        bugCount = 0
        for bug in data['bugs']:
            bugCount += 1
        # print data['bugs'][]['summary']
        print file, bugCount
        if bugCount >= 10000:
            passedLimit.append(file)
        totalBugCount += bugCount
    print 'total', totalBugCount
    if(len(passedLimit) > 0):
        print 'Passed or equal to limit: ' + ', '.join(passedLimit)


def getAllSummaries(files):
    summaries = []
    # abspath = os.path.abspath(__file__)
    # dname = os.path.dirname(abspath)
    # os.chdir(dname)
    # for file in glob.glob("*.json"):
    for file in files:
        data = json.loads(open(file).read())
        for bug in data['bugs']:
            summaries.append(bug['summary'].encode('utf-8'))
    list = open('summaryList.txt', 'w')
    for item in summaries:
        list.write('{0}\n'.format(item))
    list.close()


def getAllIDs(files):
    summaries = []
    # abspath = os.path.abspath(__file__)
    # dname = os.path.dirname(abspath)
    # os.chdir(dname)
    # for file in glob.glob("*.json"):
    for file in files:
        data = json.loads(open(file).read())
        for bug in data['bugs']:
            summaries.append(bug['id'])
    list = open('idList.txt', 'w')
    for item in summaries:
        list.write('{0}\n'.format(item))
    list.close()


def severityAnalysis(files):
    severities = []
    blocker, critical, major, normal, minor, trivial, enhancement = (0 , ) * 7
    for file in files:
        data = json.loads(open(file).read())
        for bug in data['bugs']:
            severity = bug['severity'].encode('utf-8')
            if severity == 'blocker': blocker+=1
            if severity == 'critical': critical+=1
            if severity == 'major': major+=1
            if severity == 'normal': normal+=1
            if severity == 'minor': minor+=1
            if severity == 'trivial': trivial+=1
            if severity == 'enhancement': enhancement+=1
    print '''Severity analysis:
blocker: %d
critical: %d
major: %d
normal: %d
minor: %d
trivial: %d
enhancement: %d''' % (blocker, critical, major, normal, minor, trivial, enhancement)


def filesWithin(directory_path, pattern="*"):
    for dirpath, dirnames, filenames in os.walk(directory_path):
        for file_name in fnmatch.filter(filenames, pattern):
            yield os.path.join(dirpath, file_name)


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
#getAllIDs(filesWithin(dname, '*.json'))
severityAnalysis(filesWithin(dname, '*.json'))
# getAllSummaries()
