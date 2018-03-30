#!/usr/bin/env python
import sys
import string

positiveWords = []
negativeWords = []

# get positive words
with open("positive.txt", "rb") as posFile:
	lines = posFile.readlines()
	for line in lines:
		line = line.strip()
		if line.startswith(';') or line == "":
			pass
		else:
			positiveWords.append(line)

# get negative words
negativeWords = []
with open("negative.txt", "rb") as negFile:
	lines = negFile.readlines()
	for line in lines:
		line = line.strip()
		if line.startswith(';') or line == "":
			pass
		else:
			negativeWords.append(line)

# input comes from STDIN (standard input)
for line in sys.stdin:
    lineSplit = line.split("\t")
    try:
        productID = lineSplit[1]
        reviewText = lineSplit[7]
    except:
        continue # if line cannot be tab-split into 8 elements, skip it
    reviewText = reviewText.translate(None, string.punctuation) # remove punctuation from review text
    reviewText = reviewText.lower() # change all letters to lower case
    countPositiveWords = 0
    countNegativeWords = 0
    words = reviewText.split()
    for word in words:
        if word in positiveWords:
            countPositiveWords += 1
        elif word in negativeWords:
            countNegativeWords += 1

    if countPositiveWords > countNegativeWords:
        print '%s\t%s' % (productID, "positive-1") #todo: are -1 necessary?
    else:
        print '%s\t%s' % (productID, "negative-1")
