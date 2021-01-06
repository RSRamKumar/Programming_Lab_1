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
				#print line
				#print range
				spliced += 1
				continue
			if start.startswith('c'):
				start = start[1:]
			start = int(start)
			end = int(end)
			if abs(end-start)<size:
				tooSmall += 1
				continue
			ranges[end]=start
	print("Spliced: ",spliced)
	print("too small: ",tooSmall)
	return ranges

orfFile = sys.argv[1]
geneFile = sys.argv[2]
if len(sys.argv)>3:
	size = int(sys.argv[3])
else:
	size = 0
orfPositions = readPositions(orfFile,size*3)
genePositions = readPositions(geneFile,0)
orfs = list(orfPositions.items())

if size>0:
	print("Only genes/orfs with at least %d amino acids were considered"%size)
print("Total number of orfs:",len(orfPositions))
print("Total number of genes:",len(genePositions))

good=0
perfect = 0
for x in orfPositions:
	if x in genePositions:
		good += 1
		if orfPositions[x]==genePositions[x]:
			perfect += 1

print("Total number of found genes:",good, "Percentage of ORFs:",float(good)/len(orfPositions))
print("Total number of correct genes:",perfect, "Percentage of ORFs:",float(perfect)/len(orfPositions))

notFound = 0

for x in genePositions:
	if x not in orfPositions:
		notFound += 1

print("Genes not found:",notFound)
