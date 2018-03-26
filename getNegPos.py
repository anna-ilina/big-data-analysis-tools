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

print (positiveWords)

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

print (negativeWords)