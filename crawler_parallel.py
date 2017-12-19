# Download Product List from bugzilla.mozilla.org and JSON file for those products
# Use with Python 2.7

#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import os
import datetime
import json
import requests
import sys
import time

from joblib import Parallel, delayed


def downloadWithDateParallel(mydir, product, year, month):
        # Don't remove this
        product = product.replace('\xc2\xa0', ' ').replace('-', '').strip()
        endMonth = month
        endDate = year
        if month == 12:
            endDate += 1
            endMonth = 1
        else: endMonth += 1
        startTime = time.time()
        dateWithMonth = str(year) + '-' + str('%02d' % month)
        endDateWithMonth = str(endDate) + '-' + str('%02d' % endMonth)
        print 'Starting to retrieve %s %s' % (product.strip(), dateWithMonth.strip())
        payload = {'product': product, 'f1':'creation_ts', 'f2':'creation_ts', 'o1':'greaterthaneq', 'o2':'lessthan', 'v1':dateWithMonth.strip(), 'v2':endDateWithMonth.strip()}
        request = requests.get('https://bugzilla.mozilla.org/rest/bug', params=payload)
        data = request.json()
        filename = '{0}_{1}.json'.format(
            product.strip(), dateWithMonth.strip()).decode('utf-8')
        mydir = os.path.join(mydir, product.strip())
        if not os.path.exists(mydir):
            os.makedirs(mydir)
        file = open(mydir + '/' + filename, 'w')
        # file.write(data)
        json.dump(data, file)
        file.close()
        print 'Retrieved %s_%s.json, It took %d seconds' % (product.strip(), dateWithMonth.strip(), time.time() - startTime)

if __name__ == '__main__':

    if os.path.exists('productList.txt') == True:
        beginTime = time.time()
        products = open('productList.txt', 'r')
        mydir = os.path.join(
            os.getcwd(), datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        os.makedirs(mydir)
        print 'Location for downloads:', mydir

        dateList = []
        for i in range(2007,2018):
            dateList.append(i)
        monthList = []
        for i in range(1,13):
            monthList.append(i)

        Parallel(n_jobs=100)(delayed(downloadWithDateParallel)(mydir, product, year, month) for product in products for year in dateList for month in monthList)

        print 'Total time : %d seconds = %.2f minutes' % (time.time() - beginTime, (time.time() - beginTime) / 60)

    else:
        print 'productList.txt does not exist'
        sys.exit()
