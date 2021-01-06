import matplotlib.pyplot as plt

def getDepth(node):
    if isinstance(node,tuple):
        return max(getDepth(node[0]),getDepth(node[1]))+1
    else:
        return 0

def showtree_rec(node,offset,depth,height=None):
    if not isinstance(node,tuple):
        x = offset
        y = height[node] if height else depth
        plt.plot([x,x],[0,y],'k')
        plt.text(x,0,node)
        return x,y,1
    else:
        xl,yl,nl = showtree_rec(node[0],offset,depth-1,height)
        xr,yr,nr = showtree_rec(node[1],offset+nl,depth-1,height)
        y = height[node] if height else depth
        plt.plot([xl,xl],[yl,y],'k')
        plt.plot([xr,xr],[yr,y],'k')
        plt.plot([xl,xr],[y,y],'k')
        return (xl+xr)/2,y,nl+nr

def showtree(node,height=None):
    showtree_rec(node,0,getDepth(node),height)
    axes = plt.gca()
    lim = axes.get_ylim()
    delta=(lim[1]-lim[0])*0.05
    axes.set_ylim(lim[0]-delta,lim[1]+delta)
    lim = axes.get_xlim()
    delta=(lim[1]-lim[0])*0.05
    axes.set_xlim(lim[0]-delta,lim[1]+delta)
    #plt.axis('off')
    plt.show()

def asciitree_rec(node):
    if not isinstance(node,tuple):
        return ['|',node],0,0
    else:
        left,left_left,left_right= asciitree_rec(node[0])
        right,right_left,right_right = asciitree_rec(node[1])
        lr_left = left_left+1+left_right+1
        lr_right = right_left+1+right_right+1
        
        horizontal_bar=' '*left_left+'/'+'-'*left_right+'-+-'+'-'*right_left+'\\'
        vert_bar=' '*lr_left+'|'
        joined = [vert_bar,horizontal_bar]
        l_format="{:<%d}"%lr_left
        max_depth=max(len(left),len(right))
        for l,r in zip([left[0]]*(max_depth-len(left))+left,[right[0]]*(max_depth-len(right))+right):
            lr = l_format.format(l)+"  "+r
            joined.append(lr)
        return joined,lr_left,lr_right
            
    
def asciitree(node):
    rv,_,_ = asciitree_rec(node)
    for s in rv:
        print(s)
        
