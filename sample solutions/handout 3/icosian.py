import sys

# Describe a graph by its node (first letter) and its neighbors (following letters)
g0= [
    'bcgz','cbdp','dcfm','fgdk','gbfh',
    'qprz','pcnq','nmps','mdln','lkmt','kfjl','jhkv','hgjx','xhwz','zbqx',
    'rqsw','snrt','tlsv','vjtw','wrvx'
]

# Code the graph using a dictionary where each node is associated with its set of neighbor nodes
g={}
for n in g0:
    k=n[0]
    g[k]=set(n[1:])

# Consistency check for graph description:
#    if a is a neighbor of b then b is also a neighbor of a
for v,nnn in g.items():
    for n in nnn:
        if not v in g[n]:
            print("Error in graph description")
            print('n(',v,')=',nnn,'   n(',n,')=',g[n],sep='')
            sys.exit(1)



def add_route():
    """ Add route to global variable all_routes
    """
    route=[0]*20
    for k,v in visited.items():
        route[v]=k
    all_routes.add(''.join(route))


def traverse(root,step):
    """ Depth first traversal of global graph g looking for
        Hamiltonian circles
    """
    if step==20 and visited[root]==0:
		# Current node is first node on path and all 20 nodes have been visited
        add_route()
    elif root in visited:
		# Current node has already been visited
        return
    else:
		# an unvisited node
        visited[root] = step # visit node and ...
        for n in g[root]: ### ... continue with neighbors
            traverse(n,step+1)
        del visited[root] # unvisit node

visited={}
all_routes=set()
traverse('r',0)
for i,route in enumerate(all_routes):
    print("Route #{}: {}".format(i+1,route))
print("There are {} different Hamiltonian cycles starting at designated node 'r'".format(len(all_routes)))
