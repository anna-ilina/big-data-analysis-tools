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
            percentagePositiveReviews = (float(currentPositiveCount) / (currentPositiveCount + currentNegativeCount))*100
            if currentPositiveCount > currentNegativeCount:
                print("{}\t{}-{}-{}".format(currentProductID, "positive", 
                    str(currentPositiveCount), str(percentagePositiveReviews)))
            else:
                print("{}\t{}-{}-{}".format(currentProductID, "negative", 
                    str(currentNegativeCount), str(percentagePositiveReviews)))
        currentProductID = productID
        if value == "positive":
            currentPositiveCount = valueCount
            currentNegativeCount = 0
        elif value == "negative":
            currentPositiveCount = 0
            currentNegativeCount = valueCount

# Output last word if needed
if productID == currentProductID:
    percentagePositiveReviews = (float(currentPositiveCount) / (currentPositiveCount + currentNegativeCount))*100
    if currentPositiveCount > currentNegativeCount:
        print("{}\t{}-{}-{}".format(currentProductID, "positive", 
            str(currentPositiveCount), str(percentagePositiveReviews)))
    else:
        print("{}\t{}-{}-{}".format(currentProductID, "negative", 
            str(currentNegativeCount), str(percentagePositiveReviews)))
