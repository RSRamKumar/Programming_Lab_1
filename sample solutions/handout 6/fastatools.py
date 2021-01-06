""" Handout 5
    Exercise 1
"""

from itertools import groupby

def read_fasta_sequence(fin):
    hd = next(fin).strip()[1:]
    seq= "".join(line.strip() for line in fin)
    return hd,seq


def read_fasta(filename):
    seqList=[]
    seqAcc=[]
    header=None
    for line in open(filename):
        line = line.strip()
        if line.startswith('>'):
            if header: # make sure header is valid
                newSeq = (header,''.join(seqAcc))
                seqList.append(newSeq)
            header = line[1:]
            seqAcc=[]
        else:
            seqAcc.append(line)
    if header:
        newSeq = (header,''.join(seqAcc)) # last sequence
        seqList.append(newSeq)
    return seqList

def read_fasta_alt(filename):
    with open(filename) as fin:
        it = groupby(fin,lambda line:line[0]==">")
        seqs=[]
        for k,lines in it:
            if k:
                header=''.join(x.strip() for x in lines)[1:]
            else:
                seq = ''.join(x.strip() for x in lines)
                seqs.append((header,seq))

    return seqs

def read_fasta_iter(filename):
    seqAcc=[]
    header=None
    for line in open(filename):
        line = line.strip()
        if line.startswith('>'):
            if header: # make sure header is valid
                yield (header,''.join(seqAcc))
            header = line[1:]
            seqAcc=[]
        else:
            seqAcc.append(line)
    if header:
        yield (header,''.join(seqAcc)) # last sequence

def read_fasta_iter_alt(filename):
    with open(filename) as fin:
        it = groupby(fin,lambda line:line[0]==">")
        seqs=[]
        for k,lines in it:
            if k:
                header=''.join(x.strip() for x in lines)[1:]
            else:
                seq = ''.join(x.strip() for x in lines)
                yield (header,seq)

# alternate solution returning a dictionary where the keys are the headers
# and the sequences the values
def read_fasta_dict(infile):
    seqDict={}
    for line in infile:
        line = line.strip()
        if line.startswith('>'):
            currentHeader = line[1:]
            seqDict[currentHeader] = ""
        else:
            seqDict[currentHeader] += line
    return seqDict

def write_fasta(infile,header,sequence):
    infile.write('>'+header+'\n')
    for i in range(0,len(sequence),70):
        infile.write(sequence[i:i+70])
        infile.write('\n')


if __name__ != "__main__":
    print("Importing!")
    
if __name__=='__main__':
    hd,seq = read_fasta_sequence(open("ecoli-genome.fna"))
    print("header:",hd)
    print("sequence length:",len(seq))
    
    print()
    seqs = read_fasta("ecoli-proteome.faa")
    
    shortest = seqs[0]
    longest = seqs[0]
    for hs in seqs:
        if len(hs[1])< len(shortest[1]):
            shortest = hs
        if len(hs[1])> len( longest[1]):
            longest  = hs
    last = seqs[-1]
    # One line solutions of shortest/longest sequence:
    # shortest = min(seqs,key=lambda x: len(x[1]))
    # longest  = max(seqs,key=lambda x: len(x[1]))
    print("Shortest sequence",shortest[0],"has length",len(shortest[1]))
    print("Longest  sequence", longest[0],"has length",len( longest[1]))
    print("Last sequence",last[0],"has length",len(last[1]))

    print()
    
    seqs = read_fasta_iter("ecoli-proteome.faa")
    
    shortest = next(seqs)
    longest = shortest
    for hs in seqs:
        if len(hs[1])< len(shortest[1]):
            shortest = hs
        if len(hs[1])> len( longest[1]):
            longest  = hs
        last = hs
    # One line solutions of shortest/longest sequence:
    # shortest = min(seqs,key=lambda x: len(x[1]))
    # longest  = max(seqs,key=lambda x: len(x[1]))
    print("Shortest sequence",shortest[0],"has length",len(shortest[1]))
    print(shortest[1])
    print("Longest  sequence", longest[0],"has length",len( longest[1]))
    print(longest[1])
    print("Last sequence",last[0],"has length",len(last[1]))
    print(last[1])
    
    
    print()
    f = open("sillySequence.faa","w")
    hd = "python"
    seq = "FLYINGCIRCVS"
    write_fasta(f,hd,seq)
    f.close()

    f = open("nudgenudge.faa","w")
    write_fasta(f,"albatross","WHATFLAVQRISIT")
    write_fasta(f,"lumberjack","ISLEEPALLNIGHTANDIWQRKALLDAY")
    write_fasta(f,"deadparrot","NQRWEGIANPLVE")
    f.close()