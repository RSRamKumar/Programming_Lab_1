import numpy

from tools_handout4 import read_blosum, read_fasta_sequence, pprint_alignment
import numpy as np
from pprint import pprint
#
import sys


def argMax(mat):
    mi=0
    mj=0
    mv=mat[0,0]
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if mat[i,j]>mv:
                mv = mat[i,j]
                mi = i
                mj = j
    return mi,mj

def needle(sA,sB,sc,gp):
    match = 0
    left = 1
    up = 2

    sA = " "+sA
    sB = " "+sB

    mat = np.zeros((len(sA),len(sB)))
    tb = np.zeros((len(sA),len(sB)))
    
    for i in range(len(sA)):
        mat[i,0] = 0
        tb[i,0] = -1
    for j in range(len(sB)):
        mat[0,j] = 0
        tb[0,j] = -1
    tb[0,0]=-1
    for i in range(1,len(sA)):
        for j in range(1,len(sB)):
            leftScore = mat[i,j-1]+gp
            upScore = mat[i-1,j]+gp
            matchScore = mat[i-1,j-1]+sc[sA[i]+sB[j]]
            if matchScore>= leftScore and matchScore>=upScore:
                if matchScore>0:
                    mat[i,j] = matchScore
                    tb[i,j] = match
                else:
                    mat[i,j] = 0
                    tb[i,j] = -1
            else:
                if leftScore>=upScore:
                    if leftScore>0:
                        mat[i,j] = leftScore
                        tb[i,j] = left
                    else:
                        mat[i,j] = 0
                        tb[i,j] = -1
                else:
                    if upScore>0:
                        mat[i,j] = upScore
                        tb[i,j] = up
                    else:
                        mat[i,j] = 0
                        tb[i,j] = -1
    alignA=""
    alignB=""
    i,j=argMax(mat)
    score = mat[i,j]
    #pprint(mat)
    while tb[i,j]>=0:
        if tb[i,j]==match:
            alignA += sA[i]
            alignB += sB[j]
            i -= 1
            j -= 1
        elif tb[i,j]==up:
            alignA += sA[i]
            alignB += '-'
            i -= 1
        elif tb[i,j]==left:
            alignA += '-'
            alignB += sB[j]
            j -= 1
    return alignA[::-1], alignB[::-1], score


if __name__ == '__main__':
    gp = int(sys.argv[1])
    if gp>0:
        gp = -gp
    mat = read_blosum(sys.argv[2])
    hA,sA = read_fasta_sequence(open(sys.argv[3]))
    hB,sB = read_fasta_sequence(open(sys.argv[4]))

    result = needle(sA,sB,mat,gp)

    print("Score=",result[2])
    pprint_alignment(result[0],result[1],mat)


