########################################
# This script is intended to extract the contexts of target words from text files
# From its working directory, a few folders are used to hold text files that:
#	provide the target words (cwd/InputLemmas)
#	provide the corpora which will be analyzed (cwd/WLP_Corpus Files and cwd/WLP_TestFiles)
#	provide a destination for the contexts in which the target words appeared in the corpora
#		(cwd/OutputWords)
#	
# 
#
#####################
### Start program ###
#####################
### Import packages
import re
import sys
import os
import glob


### Initialization of corpora
cwd = os.getcwd()
CORPORA_FILES = cwd + "/WLP_CorpusFiles"
TEST_FILES = cwd + "/WLP_TestFiles"
WORKING_FILES=TEST_FILES

window=5 #sets window - eg window=5 would grab the 5 words before and after target word



GEN_WORDS = False

### Structure of corpus documents
LEN_LINE = 5
WORD_INDEX = 2
LEMMA_INDEX = 3
POS_INDEX = 4
SPECIAL_POS_INDEX = 3
SPECIAL_WORD_INDEX = 2
SEP_CHAR = "\t"

WLP_WORD_INDEX = 0
WLP_LEMMA_INDEX = 1
WLP_POS_INDEX = 2

### Need to skip certain characters due to nature of raw text
SKIP_CHARS = ["@", ",", "(", ")", "-", "--", ":", "'s", "\"", "\'", "/", "<p>", "<", ">", "#"]
### ### We do not want to skip ".", ";", or "?" characters as those indicate the ends
### ### of sentences.


TARGET_INDEX=LEMMA_INDEX








### Custom file opening function
def openFile(filename, characteristic, new = False):
	count = 0
	filenameTemp = filename
	if (new == True):
		filetype = filename[-4:]
		filename = filename[:-4]
		while os.path.exists(filenameTemp):
			filenameTemp = filename + "_" + str(count) + filetype
			count += 1
	returnedFile = open(filenameTemp, characteristic)
	return returnedFile

def createEmoFiles(emoWordList):
	currDir = os.getcwd()
	if not os.path.exists(currDir + "/OutputWords"):
		os.makedirs(currDir + "/OutputWords")
	for word in emoWordList:
		outputFile = open(currDir+"/OutputWords/"+word+'.txt', 'a')
		corpusFiles=os.listdir(WORKING_FILES)
		corpusFiles=str(corpusFiles)+'\n'
		outputFile.write(corpusFiles)
		outputFile.close()

### Need to create files for each word. The following function creates a txt file for each word in wordList
### and then saves the path to that txt file in the array for the target noun.


def getEmoWords(emoWordList):
	emoOutList=[]
	with open(emoWordList,'rb') as inFile:
		for line in inFile:
			emoOutList.append(line.rstrip('\r\n'))
	# print "emoOutList="+str(emoOutList)
	return emoOutList

### Begin analysis of corpora
def generateDocuments(corpora, emoWordList): 
	for corpus_file in glob.glob(corpora + '/*.txt'): 
		doc = [[]]
		docDict = {}
		filename=corpus_file.split("Files")[-1]
		with open(corpus_file) as corpus:  # Open each corpus
			doc[0] = re.split(r'\t+', corpus.readline().strip().lower()) # Read in first line of document; make sure inputs are sanitized
			for lineIndex,nextLine in enumerate(corpus):			 
				nextLine = re.split(r'\t+', nextLine.strip().lower())
				nextLine.append(filename)
				nextLine.append(lineIndex)
				docDict[lineIndex]=nextLine

				doc.append(nextLine)
			print str(filename)+" loaded"
			searchTgt(doc, docDict, emoWordList, SKIP_CHARS)


def searchTgt(doc, docDict, emoWordList, SKIP_CHARS):
	###Each word in the corpus is read in as a dictionary pair with an index (#) as its key.  
	###This function scans a corpus doc and when it finds a word that's also in the word list,
	### it searches for the surrounding words by their indices relative to the matching word.
	### The function also excludes any results that are in the SKIP_CHARS list defined above
	wlpLen=5
	regLen=7
	context = []
	maxIndex= max(k for k, v in docDict.iteritems() if v != 0)

	for curLine in doc:
		print curLine
		curContext=[]
		if len(curLine)>wlpLen:
			wordColIndex=2
			lemmaColIndex=3
		else:
			wordColIndex=0
			lemmaColIndex=1			
		if len(curLine)>3 and type(curLine[-1]) == int and (curLine[-1]-maxIndex)<-5:  # MAY NEED TO ADD A CLAUSE HERE TO EXCLUSE FIRST 20 or so lines of file...

			curWord=curLine[lemmaColIndex]
			if curWord in emoWordList:
				curWordFile=open(cwd+"/OutputWords/"+curWord+".txt", "a")

				tgtIndex=curLine[-1] #this is the index of the current word within the corpus file, assigned when the corpus file was imported


				bumpFor=0
				bumpBack=0
				contextIndices=[tgtIndex+num for num in range(((-window) -bumpBack) ,window+1+bumpFor)]
				skipIndices=[]
				contextCounter=0
				okIndices=[]
				print contextIndices
				for contextIndex in contextIndices:
					###Make a new function that recalculates the context indices?
					if contextIndex not in skipIndices:

						contextWord=docDict[contextIndex][wordColIndex]
						if contextWord not in SKIP_CHARS:
							okIndices.append(contextIndex)

						else:
							if contextIndex-tgtIndex<0:
								bumpBack+=1
								skipIndices.append(contextIndex)
								addedIndex=tgtIndex-window-bumpBack
								contextIndices.append(addedIndex)
							if contextIndex-tgtIndex>0:
								bumpFor+=1
								skipIndices.append(contextIndex)
								contextIndices.append(tgtIndex+window+bumpFor)
				okLabels=[]		
				for item in okIndices:
					okLabels.append(docDict[item][-1])
				
				okIndices.sort()
				contextWords=[]
				for item in okIndices:
					contextWords.append(docDict[item][wordColIndex])
				contextWords=' '.join(contextWords)
				contextWords=contextWords+'\n'
				if len(curLine)<6:
					tgtLabel='none'
				else:
					tgtLabel=docDict[tgtIndex][1]
				tgtWord=docDict[tgtIndex][wordColIndex]
				corpFile=docDict[tgtIndex][-2]
				output=corpFile+', '+tgtLabel+', '+tgtWord+', '+contextWords
				print output
				curWordFile.write(output)

	print "doc done"	


# Run the program
def main():
	if (GEN_WORDS == False):
		emoWordList = getEmoWords(cwd+"/InputLemmas/testWordList.txt")
		createEmoFiles(emoWordList)
		generateDocuments(WORKING_FILES, emoWordList)  #Change CORPORA_FILES to another directory to analyze other files

main()
sys.exit()
