import sys,string

from  fastatools import *


def cDna(seq):
	""" Determine the complementary DNA
	"""
	cdna=seq.translate(str.maketrans("ACGTacgt","TGCAtgca"))[::-1]
	return cdna

# Alternate solution to cDNA	
def cDnaAlt(seq):
	""" Determine the complementary DNA
	"""
	cdict={'A':'T','C':'G','G':'T','T':'A'}
	cdna=""
	for c in reversed(seq):
		cdna += cdict[C]
	return cdna

def getOrf(seq,startCodon="ATG",stopCodons=["TAA","TAG","TGA"]):
	# Keep track of start codon in each reading frame
	start = [None,None,None]
	
	# ORFs are kept in a list of tuples
	orfs=[]
	for i in range(len(seq)-3):
		rf = i%3
		codon = seq[i:i+3]
		if start[rf]!=None and codon in stopCodons:
			# A stop codon and a corresponding start codon upstream has been found
			orfs.append((start[rf],i+2))
			start[rf] = None # 'reset' start codon
		if not start[rf] and codon==startCodon:
			# 'first' start codon after stop codon (in the corresponding reading frame)
			start[rf] = i
	return orfs

def writeOrfs(outf,header,orfs,seq,startCodon='ATG'):
	of = open(outf,'w')

	for s,e in orfs:
		if seq[s:s+3]=='ATG':
			# ORF on normal strand
			write_fasta(of,header+":%d-%d"%(s+1,e+1),seq[s:e+1])
		else:
			# ORF on complementary strand
			write_fasta(of,header+":c%d-%d"%(e+1,s+1),cDna(seq[s:e+1]))
	of.close()
	
		

if __name__=='__main__':
	outf = sys.argv[2]
	inf = open(sys.argv[1])
	hd,seq = read_fasta_sequence(inf)
	orfHeader=hd.split()[0] # header to use for orfs
	# Get orfs on one strand
	orfs = getOrf(seq)
	# Get orfs on c-strand
	corfs = getOrf(cDna(seq))
	# Merge orfs and corfs:
	n = len(seq)-1
	for s,e in corfs:
		orfs.append((n-e,n-s))
	orfs.sort()
	writeOrfs(outf,orfHeader,orfs,seq)
	

