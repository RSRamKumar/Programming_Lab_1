import numpy

from tools_handout4 import read_blosum, read_fasta_sequence, pprint_alignment
import numpy as np
from pprint import pprint
#
import sys
                

def needle(sA,sB,sc,d,e):
    match = 0
    left = 1
    up = -1
    stop = 99999999
    sA = " "+sA
    sB = " "+sB

    mat = np.zeros((len(sA),len(sB)))
    tb = np.zeros((len(sA),len(sB)),int)
    

    for i in range(1,len(sA)):
        mat[i,0] = d+(i-1)*e
        tb[i,0] = up
    for j in range(1,len(sB)):
        mat[0,j] = d+(j-1)*e
        tb[0,j] = left
    mat[0,0] = 0
    tb[0,0]=stop
    for i in range(1,len(sA)):
        for j in range(1,len(sB)):
            leftScore = mat[i,j-1]+d
            leftSteps = 1
            for k in range(2,j+1):
                ls = mat[i,j-k]+d+e*(k-1)
                if ls>leftScore:
                    leftScore = ls
                    leftSteps = k
            upScore = mat[i-1,j]+d
            upSteps = 1
            for k in range(2,i+1):
                us = mat[i-k,j]+d+e*(k-1)
                if us>upScore:
                    upScore = us
                    upSteps = k
            matchScore = mat[i-1,j-1]+sc[sA[i]+sB[j]]
            if matchScore>= leftScore and matchScore>=upScore:
                mat[i,j] = matchScore
                tb[i,j] = match
            else:
                if leftScore>=upScore:
                    mat[i,j] = leftScore
                    tb[i,j] = left*leftSteps
                else:
                    mat[i,j] = upScore
                    tb[i,j] = up*upSteps
    alignA=""
    alignB=""
    i=len(sA)-1
    j=len(sB)-1
    score = mat[i,j]
    #pprint(mat)
    while tb[i,j]!=stop:
        if tb[i,j]==match:
            alignA += sA[i]
            alignB += sB[j]
            i -= 1
            j -= 1
        elif tb[i,j]*up>0:
            lgth = abs(tb[i,j])
            alignA += sA[i:i-lgth:-1]
            alignB += '-'*lgth
            i -= lgth
        elif tb[i,j]*left>0:
            lgth = abs(tb[i,j])
            alignA += '-'*lgth
            alignB += sB[j:j-lgth:-1]
            j -= lgth
        #print(i,j)
    return alignA[::-1], alignB[::-1], score



if __name__ == '__main__':
    go = int(sys.argv[1])
    if go>0:
        go = -go
    ge = int(sys.argv[2])
    if ge>0:
        ge = -ge

    mat = read_blosum(sys.argv[3])
    hA,sA = read_fasta_sequence(open(sys.argv[4]))
    hB,sB = read_fasta_sequence(open(sys.argv[5]))

    result = needle(sA,sB,mat,go,ge)

    print("Score=",result[2])
    pprint_alignment(result[0],result[1],mat)


