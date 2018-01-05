#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import glob
import os
import fnmatch
import shutil #used for file copy
from joblib import Parallel, delayed




def getBugCount(files):
	totalBugCount = 0
	passedLimit = []
	# abspath = os.path.abspath(__file__)
	# dname = os.path.dirname(abspath)
	# os.chdir(dname)
	# for file in glob.glob("*.json"):
	countDict = {}
	for file in files:
		data = json.loads(open(file).read())
		bugCount = 0
		for bug in data['bugs']:
			bugCount += 1
			if countDict.get(bug['product']) == None: countDict[bug['product']] = 1
			else: countDict[bug['product']] += 1
			# print data['bugs'][]['summary']
			#print file, bugCount
			if bugCount >= 10000:
				passedLimit.append(file)
		totalBugCount += bugCount
	d = sorted( ((v,k) for k,v in countDict.iteritems()), reverse=True)
	for v,k in d:
		print k,v
	print 'file:', file, 'total:', totalBugCount
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

def getAllComments(files):
	comments = []
	count = 0
	for file in files:
		count += 1
		if count % 1000 == 0 : print 'file passed', count
		try:
			data = json.loads(open(file).read())
			for comment in data['bugs'][file_base_name(os.path.basename(file))]['comments']:
				comments.append(comment['text'])
		except Exception as e: print e
	list = open('commentList.txt', 'w')
	for item in comments:
		list.write('{0}\n'.format(item.encode("utf-8")))
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

def copyComments():
	list = open('idList.txt', 'r')
	mydir = os.path.join(os.getcwd(), 'copied')
	#os.makedirs(mydir)
	for id in list:
		commentDir = os.path.join(directoryName(), 'comments', id.strip() +'.json')
		copyDir = os.path.join(directoryName(), 'copied', id.strip()+'.json')
		if not is_non_zero_file(copyDir):
			f = open(copyDir, 'w')
			f.close()
			try:
				shutil.copyfile(commentDir,copyDir)
			except Exception as e:
				print "Couldn't copy %s\nexception:\n%s" % (id, e)
	print 'done'

def copyCommentsParallel(id):
		commentDir = os.path.join(directoryName(), 'comments', id.strip() +'.json')
		copyDir = os.path.join(directoryName(), 'copied', id.strip()+'.json')
		if not is_non_zero_file(copyDir):
			f = open(copyDir, 'w')
			f.close()
			try:
				shutil.copyfile(commentDir,copyDir)
			except Exception as e:
				print "Couldn't copy %s\nexception:\n%s" % (id, e)


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

#extracts summary, description and id of bugs by severities
def getSummaryAndDescriptionBySeverity (bug_files, comments_path):
	sum_dict = {'blocker': [], 'critical': [], 'major': [], 'normal': [], 'minor': [], 'trivial': [], 'enhancement': []}
	id_dict = {'blocker': [], 'critical': [], 'major': [], 'normal': [], 'minor': [], 'trivial': [], 'enhancement': []}
	desc_dict = {'blocker': [], 'critical': [], 'major': [], 'normal': [], 'minor': [], 'trivial': [], 'enhancement': []}

	for file in bug_files:
		data = json.loads(open(file).read())
		for bug in data['bugs']:
			severity = bug['severity']
			list1 = sum_dict[severity]
			list1.append(bug['summary'].encode('utf-8'))
			list2 = id_dict[severity]
			list2.append(bug['id'])

	for k, v in sum_dict.iteritems():
		list = open('summary_%s.txt' % k, 'w')
		for item in v:
			list.write('%s\n' % item)
		list.close()

	print('Created summary files')

	for k, v in id_dict.iteritems():
		list = open('id_%s.txt' % k, 'w')
		for item in v:
			list.write('%s\n' % item)

			file_name = os.path.join(comments_path, '%s.json' % str(item))
			if is_non_zero_file(file_name):
				try:
					file = open(file_name, 'r')
					data = json.loads(file.read())
					description = data['bugs'][str(item)]['comments'][0]['text']
					descriptions = desc_dict[k]
					descriptions.append(description.encode('utf-8'))
					#desc_dict[k] = descriptions
				except Exception as e: print e
		list.close()

	print('Created id files')

	for k,v in desc_dict.iteritems():
		list = open('description_%s.txt' % k, 'w')
		for item in v:
			list.write('%s\n' % item)
		list.close()

	print('Created description files')

def filesWithin(directory_path, pattern="*"):
	for dirpath, dirnames, filenames in os.walk(directory_path):
		for file_name in fnmatch.filter(filenames, pattern):
			yield os.path.join(dirpath, file_name)

def directoryName():
	abspath = os.path.abspath(__file__)
	dname = os.path.dirname(abspath)
	return dname

#checks if file exists and is not empty(size > 0)
def is_non_zero_file(fpath):
	return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

#get file base name
def file_base_name(file_name):
	if '.' in file_name:
		separator_index = file_name.index('.')
		base_name = file_name[:separator_index]
		return base_name
	else:
		return file_name


#getAllIDs(filesWithin(directoryName(), '*.json'))
#severityAnalysis(filesWithin(dname, '*.json'))
#getBugCount(filesWithin(dname, '*.json'))
# getAllSummaries()
#copyComments()
# getAllComments(filesWithin(os.path.join(directoryName(), 'comments'), '*.json'))

#getSummaryAndDescriptionBySeverity(filesWithin(os.path.join(directoryName(), 'products'), '*.json'), os.path.join(directoryName(), 'comments'))

# if __name__ == '__main__':
#         list = open('idList.txt', 'r')
#         mydir = os.path.join(os.getcwd(), 'copied')
#         #os.makedirs(mydir)
#         Parallel(n_jobs=50)(delayed(copyCommentsParallel)(id) for id in list)