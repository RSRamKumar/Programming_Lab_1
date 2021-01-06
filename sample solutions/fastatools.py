def single_fasta_sequence(filename):
    with open(filename) as f:
        header = next(f)
        header = header[1:].strip()
        seq = []
        for x in f:
            if x[0]=='>':
                break
            seq.append(x.strip())
        return header, ''.join(seq)
    
def single_fasta_sequence_alt(filename):
    with open(filename) as f:
        header = next(f)
        header = header[1:].strip()
        seq = ''.join(x.strip() for x in f)
        return header, seq

def fasta_list(filename):
    with open(filename) as infile:
        seqList=[]
        seqAcc=[]
        header=None
        for line in infile:
            line = line.strip()
            if line.startswith('>'):
                if header!=None:
                    newSeq = (header,''.join(seqAcc))
                    seqList.append(newSeq)
                header = line[1:]
                seqAcc=[]
            else:
                seqAcc.append(line)
        newSeq = (header,''.join(seqAcc)) # last sequence
        seqList.append(newSeq)
        return seqList

# alternate solution returning a dictionary where the keys are the headers
# and the sequences the values
def fasta_dict(filename):
    with open(filename) as infile:
        seqDict={}
        for line in infile:
            line = line.strip()
            if line.startswith('>'):
                currentHeader = line[1:]
                seqDict[currentHeader] = ""
            else:
                seqDict[currentHeader] += line
        return seqDict

def fasta_sequences(filename):
    with open(filename) as infile:
        header = None
        sequence=[]
        for line in infile:
            if line.startswith(">"):
                if header:
                    yield header,''.join(sequence)
                header = line[1:].strip()
                sequence=[]
            else:
                sequence.append(line.strip())
        if header:
            yield header,''.join(sequence)

def fasta_sequences_alt(filename):
    with open(filename) as infile:
        line = infile.readline()
        while line:
            assert line.startswith('>'),"Malformed FASTA file"
            header = line[1:].strip()
            line = infile.readline()
            seq = []
            while line and not line.startswith('>'):
                seq.append(line.strip())
                line = infile.readline()
            yield header,''.join(seq)


def write_fasta(infile,header,sequence):
	infile.write('>'+header+'\n')
	i=0
	while i<len(sequence):
		infile.write(sequence[i:i+70])
		infile.write('\n')
		i += 70
