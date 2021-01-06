import sys

def getBalancedAccuracy(tp,fp,tn,fn,siz):
	ba = 0.5*tp/(tp+fn)+0.5*tn/(tn+fp)
	print("Thresh:",siz,"ba:",ba)
	return ba

def readPositions(filename,size=0):
	f = open(filename)
	ranges={}
	spliced = 0
	tooSmall = 0
	for line in f:
		if line.startswith('>'):
			range = line.split()[0].split(':')[1]
			items = range.split('-')
			start = items[0]
			end = items[-1]
			if len(items)!=2:
				# Spliced genes are given with multiple ranges
				# skip these
				spliced += 1
				continue
			if start.startswith('c'):
				start = start[1:]
			start = int(start)
			end = int(end)
			if abs(end-start)<size:
				# Discard too small ORFs during reading (if size parameter is specified)
				tooSmall += 1
				continue
			ranges[end]=start
	f.close()
	print("Spliced: ",spliced)
	print("too small: ",tooSmall)
	return ranges

orfFile = sys.argv[1]
geneFile = sys.argv[2]

orfPositions = readPositions(orfFile)
genePositions = readPositions(geneFile)
orfs = list(orfPositions.items())

# sort orfs by decreaasing length
orfs.sort(key=lambda x: -abs(x[0]-x[1]))

# Geet total number of gene coding and non gene coding ORFS
allPositives = 0
allNegatives = 0
for s,e in orfs:
	if s in genePositions:
		allPositives += 1
	else:
		allNegatives += 1


# For an extremely large threshold 
# no ORFs will be classified as genes
truePositives = 0
falsePositives = 0
falseNegatives = allPositives
trueNegatives = allNegatives
bestThreshold = 123456789
# The ba should be 0.5
bestBa=getBalancedAccuracy(truePositives,falsePositives,trueNegatives,falseNegatives,bestThreshold)
bestTP = truePositives
bestFP = falsePositives
bestTN = trueNegatives
bestFN = falseNegatives
oldLength = abs(orfs[0][0]-orfs[0][1])
# Iterate over ORFS in decreasing length
for e,s in orfs:
	newLength=abs(e-s)
	if newLength!=oldLength:
		# balanced accuracy is recalculated each time the length changes
		ba = getBalancedAccuracy(truePositives,falsePositives,trueNegatives,falseNegatives,oldLength)
		if ba>=bestBa:
			bestBa=ba
			bestThreshold = oldLength
			bestTP = truePositives
			bestFP = falsePositives
			bestTN = trueNegatives
			bestFN = falseNegatives
		oldLength = newLength
	# Each ORF will now be classified either as true or false positives
	# adjust numbers accordingly
	if e in genePositions:
		truePositives +=1
		falseNegatives -= 1
	else:
		falsePositives += 1
		trueNegatives -= 1

# redundant as ba=0.5 if everything is classified as gene.
ba = getBalancedAccuracy(truePositives,falsePositives,trueNegatives,falseNegatives,0)
if ba>=bestBa:
	bestBa=ba
	bestThreshold = e-s
	bestTP = truePositives
	bestFP = falsePositives
	bestTN = trueNegatives
	bestFN = falseNegatives

print("Best threshold: ",bestThreshold)
print("Best ba:",bestBa)
print("True positives: ",bestTP)
print("False negatives: ",bestFN)
print("True negatives: ",bestTN)
print("False positives: ",bestFP)
