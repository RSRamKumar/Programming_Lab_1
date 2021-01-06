"""
Common functions used for various alignment scripts
"""

def read_fasta_sequence(infile):
    hd = infile.readline().strip()[1:]
    seq=[]
    for line in infile:
        if line.startswith('>'):
            break
        seq.append(line.strip())
    return hd,''.join(seq)

def read_blosum(fn):
    scores ={}
    with open(fn) as f:
        cols = next(f).split()
        for line in f:
            entries = line.split()
            if not entries: continue
            a=entries[0]
            for b,sc in zip(cols,entries[1:]):
                scores[a+b] = int(sc)
                scores[b+a] = int(sc)
    return scores

def pprint_alignment(sA,sB,mat,lw=80):
    line=""
    for a,b in zip(sA,sB):
        if a=='-' or b=='-' or mat[a+b]<=0:
            line += " "
        else:
            if a==b:
                line += '|'
            else:
                line += ':'
    n = len(sA)
    pA= (sA[i:i+lw] for i in range(0,n,lw))
    pM= (line[i:i+lw] for i in range(0,n,lw))
    pB= (sB[i:i+lw] for i in range(0,n,lw))
    print()
    for a,m,b in zip(pA,pM,pB):
        print(a,m,b,sep='\n')
        print()
