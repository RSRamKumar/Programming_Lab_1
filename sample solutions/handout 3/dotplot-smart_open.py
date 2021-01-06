import numpy as np
import sys
import contextlib

@contextlib.contextmanager
def smart_open(filename=None):
    if filename and filename != '-':
        fh = open(filename, 'w')
    else:
        fh = sys.stdout

    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()
			
def read_fasta(filename):
	f = open(filename)
	hd = f.readline().strip()[1:]
	seq=''.join(x.strip() for x in f)
	return hd,seq

def dotplot(seqA,seqB,w,s):
	m = len(seqA)
	n = len(seqB)
	dp = np.zeros((m,n))
	offset = (w-1)//2
	for i in range(offset,m-offset):
		wA = seqA[i-offset:i+offset+1]
		for j in range(offset,n-offset):
			wB = seqB[j-offset:j+offset+1]
			matches = len(list(filter(lambda x: x[0]==x[1],zip(wA,wB))))
			if matches>=s:
				dp[i,j] = 1
	return dp

def dotplot2Ascii(dp,seqA,seqB,title,outfile):
	with smart_open(outfile) as out:
		out.write(title)
		out.write('\n\n')
		m = len(seqA)
		n = len(seqB)
		out.write(' |')
		out.write(seqB)
		out.write('\n')
		out.write('-+'+'-'*n+'\n')
		for i in range(m):
			out.write(seqA[i])
			out.write('|')
			for j in range(n):
				if dp[i,j]==1:
					out.write('*')
				else:
					out.write(' ')
			out.write('\n')

def dotplot2Plot(dp,seqA,seqB,title,outfile):
	import matplotlib.pyplot as plt
	plt.figure(figsize=(8,8))
	plt.axis([0,len(seqB)+1,len(seqA)+1,0])
	x=[]
	y=[]
	xd,yd = dp.shape
	for i in range(xd):
		for j in range(yd):
			if dp[i,j]:
				y.append(i)
				x.append(j)
	plt.plot(x,y,',')
	plt.savefig(outfile,dpi=300)
	plt.show()

def dotplot2Img(dp,seqA,seqB,title,outfile):
	import matplotlib.pyplot as plt
	plt.figure(figsize=(8,8))
	#plt.axis([0,len(seqA)+1,len(seqB)+1,0])
	plt.set_cmap('gray_r')
	plt.imshow(dp,origin='upper',)
	plt.savefig(outfile,dpi=300)
	plt.show()

	
if __name__=='__main__':
	w = int(sys.argv[1])
	s = int(sys.argv[2])
	hdA,seqA = read_fasta(sys.argv[3])
	hdB,seqB = read_fasta(sys.argv[4])
	dp = dotplot(seqA,seqB,w,s)
	title = sys.argv[5]
	outfile = sys.argv[6]
	if outfile.endswith('.txt') or outfile[0]=='-':
		dotplot2Ascii(dp,seqA,seqB,title,outfile)
	elif outfile.endswith('.img.png'):
		dotplot2I(dp,seqA,seqB,title,outfile)
	elif outfile.endswith('.png'):
		dotplot2Plot(dp,seqA,seqB,title,outfile)



