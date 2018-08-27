import os
import sys
import glob

def openFile(filename, characteristic):
	count = 0
	filenameTemp = filename
	while os.path.exists(filenameTemp):
		filenameTemp = filename + "_" + count
		count += 1
	returnedFile = open(filenameTemp, characteristic)
	return returnedFile

def reduceNouns(nounsFile = "/Nouns/allNouns_Word.txt", numIndex = 1, minFreq = 100):
	print(minFreq)
	cwd = os.getcwd()
	filename = cwd + "/reducedNouns.txt"
	newFile = openFile(filename, "w")
	with open(cwd + nounsFile) as origFile:
		for nextLine in origFile:
			nextLine = nextLine.split()
			if (len(nextLine) != 2):
				break
			if (int(nextLine[numIndex]) > minFreq):
				writeString = str(nextLine[0]) + "\t" + str(nextLine[1]) + "\n"
				newFile.write(writeString)
	return
	newFile.close()

reduceNouns()