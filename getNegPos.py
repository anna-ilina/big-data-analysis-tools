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

print ("positiveWords = " + str(positiveWords) + ";")

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

print ("negativeWords = " + str(negativeWords) + ";")

with open("negPosWords.txt", 'wb') as outFile:
	outFile.write("positiveWords = " + str(positiveWords) + ";\n")
	outFile.write("negativeWords = " + str(negativeWords) + ";\n")