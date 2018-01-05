import math
import os
import json
import operator
import string 
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.stem.porter import PorterStemmer

cwd = os.getcwd()
dir_bugs = cwd +  "/All/Firefox"

# stemmer = PorterStemmer()

# def stem_tokens(tokens, stemmer):
#     stemmed = []
#     for item in tokens:
#         stemmed.append(stemmer.stem(item))
#     return stemmed

# def tokenize(corpus):
#     tokens = []
#     stems = []
#     for sent in corpus:
#         tokens += nltk.word_tokenize(sent)
#         stems += stem_tokens(tokens, stemmer)
#     return stems

def tfidf(corpus):
	vectorizer = TfidfVectorizer(min_df=1, stop_words='english')
	X = vectorizer.fit_transform(corpus)
	idf = vectorizer.idf_
	return dict(zip(vectorizer.get_feature_names(), idf))


test_cases = ["blocker", "critical", "major", "normal", "minor", "trivial", "enhancement"]
blocker, critical, major, normal, minor, trivial, enhancement = ([] for i in range(7))

for file in os.listdir(dir_bugs):

    file_path = os.getcwd() + "/All/Firefox/" + file
    data = json.load(open(file_path))
    
    for cnt in range(len(data["bugs"])):
        if data["bugs"][cnt]["severity"] == "blocker":
            blocker.append(data["bugs"][cnt]["summary"])

        if data["bugs"][cnt]["severity"] == "critical":
            critical.append(data["bugs"][cnt]["summary"])

        if data["bugs"][cnt]["severity"] == "major":
            major.append(data["bugs"][cnt]["summary"])

        if data["bugs"][cnt]["severity"] == "normal":
            normal.append(data["bugs"][cnt]["summary"])

        if data["bugs"][cnt]["severity"] == "minor":
            minor.append(data["bugs"][cnt]["summary"])

        if data["bugs"][cnt]["severity"] == "trivial":
            trivial.append(data["bugs"][cnt]["summary"])

        if data["bugs"][cnt]["severity"] == "enhancement":
            enhancement.append(data["bugs"][cnt]["summary"])

print("# of bugs reported in the followowing categories...")
print("blocker: ", len(blocker))
print("critical", len(critical))
print("major", len(major))
print("normal: ", len(normal))
print("minor: ", len(minor))
print("trivial: ", len(trivial))
print("enhancement: ", len(enhancement))

blocker = map(str.lower, blocker)
critical = map(str.lower, critical)
major = map(str.lower, major)
normal = map(str.lower, normal)
minor = map(str.lower, minor)
trivial = map(str.lower, trivial)
enhancement = map(str.lower, enhancement)

scores = []
scores.append(tfidf(blocker))
scores.append(tfidf(critical))
scores.append(tfidf(major))
scores.append(tfidf(normal))
scores.append(tfidf(minor))
scores.append(tfidf(trivial))
scores.append(tfidf(enhancement))

# get max 10 keyword scores
for case_no in range(len(test_cases)):
	print("# maximum valued 10 keywords is: ", test_cases[case_no])
	for i in range(10):
		word = max(scores[case_no], key=scores[case_no].get)
		print(word, scores[case_no][word])
		del scores[case_no][word]
	print("\n")
