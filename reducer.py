#!/usr/bin/env python
from operator import itemgetter
import sys

currentProductID = None
currentPositiveCount = 0
currentNegativeCount = 0
productID = None
value = None
valueCount = None

# input comes from STDIN
for line in sys.stdin:
    line = line.strip()
    productID, value = line.split("\t", 1)
    value, valueCount = value.split("-", 1)
    try:
        valueCount = int(valueCount)
    except ValueError:
        continue # improper format, ignore this entry

    if productID == currentProductID:
        if value == "positive":
            currentPositiveCount += valueCount
        elif value == "negative":
            currentNegativeCount += valueCount
    else:
        if currentProductID:
            totalReviews = currentPositiveCount + currentNegativeCount
            percentagePositiveReviews = (float(currentPositiveCount) / (totalReviews))*100
            print("{0}\t{1}-{2}".format(currentProductID, totalReviews,percentagePositiveReviews))
        currentProductID = productID
        if value == "positive":
            currentPositiveCount = valueCount
            currentNegativeCount = 0
        elif value == "negative":
            currentPositiveCount = 0
            currentNegativeCount = valueCount

# Output last word if needed
if productID == currentProductID:
    totalReviews = currentPositiveCount + currentNegativeCount
    percentagePositiveReviews = (float(currentPositiveCount) / (totalReviews))*100
    print("{0}\t{1}-{2}".format(currentProductID, totalReviews,percentagePositiveReviews))
