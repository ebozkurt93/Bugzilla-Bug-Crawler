# Download Product List from bugzilla.mozilla.org and JSON file for those products
# Use with Python 2.7

#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import os
import datetime
import urllib
import json
import requests
from urlparse import urlparse
import sys
import time
import argparse

from joblib import Parallel, delayed
import multiprocessing
import itertools

# gets product list from bugzilla.mozilla.org
def createProductList():
    print 'Starting to retrieve product list'
    url = 'https://bugzilla.mozilla.org/describecomponents.cgi?full=1'
    r = requests.get(url)
    htmlFile = r.text
    dataset = []
    soup = BeautifulSoup(htmlFile, 'html.parser')
    for th in soup.find_all('th')[0:]:
        a = th.find_all('a')[0].text.encode('utf-8')
        dataset.append(a)
    list = open('productList.txt', 'w')
    for item in dataset:
        list.write('{0}\n'.format(item))
    list.close()
    print 'Retrieved product list to %s' % os.path.realpath(list.name)

# downloads a JSON file for each product
def downloadEachItem():
    if os.path.exists('productList.txt') == True:
        beginTime = time.time()
        list = open('productList.txt', 'r')
        mydir = os.path.join(
            os.getcwd(), datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        os.makedirs(mydir)
        print 'Location for downloads:', mydir
        for line in list.readlines()[:]:
            startTime = time.time()
            # Don't remove this
            line = line.replace('\xc2\xa0', ' ').replace('-', '').strip()
            print 'Starting to retrieve %s' % line.strip()
            payload = {'product': line}
            request = requests.get(
                'https://bugzilla.mozilla.org/rest/bug', params=payload)
            data = request.json()
            filename = '{0}.json'.format(line.strip()).decode('utf-8')
            file = open(mydir + '/' + filename, 'w')
            # file.write(data)
            json.dump(data, file)
            file.close()
            print 'Retrieved %s.json, It took %d seconds' % (line.strip(), time.time() - startTime)
        print 'Total time : %d seconds = %.2f minutes' % (time.time() - beginTime, (time.time() - beginTime) / 60)
    else:
        print 'productList.txt does not exist'
        sys.exit()

# downloads single JSON file for all products
def downloadAllAtOnce():
    if os.path.exists('productList.txt') == True:
        beginTime = time.time()
        list = open('productList.txt', 'r')
        mydir = os.path.join(
            os.getcwd(), datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        os.makedirs(mydir)
        print 'Location for downloads:', mydir
        items = []
        for line in list.readlines()[:]:
            # Don't remove this
            line = line.replace('\xc2\xa0', ' ').replace('-', '').strip()
            items.append(line)
        startTime = time.time()
        print 'Starting to retrieve all products'
        payload = {'product': items}
        request = requests.get(
            'https://bugzilla.mozilla.org/rest/bug', params=payload)
        data = request.json()
        filename = 'All.json'.decode('utf-8')
        file = open(mydir + '/' + filename, 'w')
        json.dump(data, file)
        file.close()
        filename = 'All.txt'.decode('utf-8')
        file = open(mydir + '/' + filename, 'w')
        for item in items:
            file.write('{0}\n'.format(item))
        file.close()
        print 'Retrieved all, total time : %d seconds = %.2f minutes' % (time.time() - beginTime, (time.time() - beginTime) / 60)
    else:
        print 'productList.txt does not exist'
        sys.exit()

# downloads a JSON file for each severity
def downloadEachItemBySeverity():
    if os.path.exists('productList.txt') == True:
        beginTime = time.time()
        list = open('productList.txt', 'r')
        mydir = os.path.join(
            os.getcwd(), datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        os.makedirs(mydir)
        print 'Location for downloads:', mydir
        for line in list.readlines()[:]:
            # Don't remove this
            line = line.replace('\xc2\xa0', ' ').replace('-', '').strip()
            severityList = ['Blocker', 'Critical', 'Major',
                            'Normal', 'Minor', 'Trivial', 'Enhancement']
            for severity in severityList:
                startTime = time.time()
                print 'Starting to retrieve %s %s' % (line.strip(), severity.strip())
                payload = {'product': line, 'severity': severity}
                request = requests.get(
                    'https://bugzilla.mozilla.org/rest/bug', params=payload)
                data = request.json()
                filename = '{0}_{1}.json'.format(
                    line.strip(), severity.strip()).decode('utf-8')
                file = open(mydir + '/' + filename, 'w')
                # file.write(data)
                json.dump(data, file)
                file.close()
                print 'Retrieved %s.json, It took %d seconds' % (line.strip(), time.time() - startTime)
        print 'Total time : %d seconds = %.2f minutes' % (time.time() - beginTime, (time.time() - beginTime) / 60)
    else:
        print 'productList.txt does not exist'
        sys.exit()

# downloads a group of JSON files with dates
def downloadWithDate():
    if os.path.exists('productList.txt') == True:
        beginTime = time.time()
        list = open('productList.txt', 'r')
        mydir = os.path.join(
            os.getcwd(), datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        os.makedirs(mydir)
        print 'Location for downloads:', mydir
        for line in list.readlines()[:]:
            # Don't remove this
            line = line.replace('\xc2\xa0', ' ').replace('-', '').strip()
            #severity = 'Normal'
            #statusList = ['ASSIGNED', 'CLOSED', 'NEW', 'NEEDINFO', 'REOPENED', 'RESOLVED', 'UNCONFIRMED', 'VERIFIED']
            dateList = []
            for i in range(2007,2018):
                dateList.append(i)
            #dateList = [2017,2016,2015,2014,2013]
            for date in dateList:
                for month in range(1, 13):
                    endMonth = month
                    endDate = date
                    if month == 12:
                        endDate += 1
                        endMonth = 1
                    else: endMonth += 1
                    startTime = time.time()
                    dateWithMonth = str(date) + '-' + str('%02d' % month)
                    endDateWithMonth = str(endDate) + '-' + str('%02d' % endMonth)
                    print 'Starting to retrieve %s %s' % (line.strip(), dateWithMonth.strip())
                    payload = {'product': line, 'f1':'creation_ts', 'f2':'creation_ts', 'o1':'greaterthaneq', 'o2':'lessthan', 'v1':dateWithMonth.strip(), 'v2':endDateWithMonth.strip()}
                    request = requests.get('https://bugzilla.mozilla.org/rest/bug', params=payload)
                    data = request.json()
                    filename = '{0}_{1}.json'.format(
                        line.strip(), dateWithMonth.strip()).decode('utf-8')
                    file = open(mydir + '/' + filename, 'w')
                    # file.write(data)
                    json.dump(data, file)
                    file.close()
                    print 'Retrieved %s_%s.json, It took %d seconds' % (line.strip(), dateWithMonth.strip(), time.time() - startTime)
        print 'Total time : %d seconds = %.2f minutes' % (time.time() - beginTime, (time.time() - beginTime) / 60)
    else:
        print 'productList.txt does not exist'
        sys.exit()


if __name__ == '__main__':

    for arg in sys.argv:
        if(arg == '1'):
            createProductList()
        elif(arg == '2'):
            downloadEachItem()
        elif(arg == '3'):
            downloadAllAtOnce()

# createProductList()
# downloadEachItem()
# downloadAllAtOnce()
# downloadWithDate()


# https://bugzilla.mozilla.org/rest/bug?include_fields=id,summary,status&f1=creation_ts&f2=creation_ts&o1=greaterthaneq&o2=lessthan&resolution=---&v1=-1w&v2=Now
