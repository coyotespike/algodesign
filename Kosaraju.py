"""
If we can implement Depth First Search iteratively, we win.

If we can consider how DFS plays with my data structure and how to begin
building Kosaraju's algorithm on top of DFS, we double win and get pizza.


Kosaraju's algorithm figures out which portions of a network are strongly connected.
Strongly Connected Components are clusters of nodes which know each other, but not others. 
You can get in, but you can't get out. Creepy.

Kosaraju's Algorithm has three steps.
    First, it takes a directed graph, runs DFS on it, and records the nodes' finish order.
    Second, it reverses the direction of the graph: incoming connections are outgoing, and vice versa.
    Third, it runs DFS on the graph using the "magic order." The new finish order tells us the leaders of the SCCs. 
       By counting how many nodes have the same leader, we know how many members are in each SCC.

If you follow a node to find its neighbor, the first node is the leader. 

My implementation below can be improved in many ways, but first of all, it exceeds my Mac's hard thread limit. 
Also it was slow. 

If we build the algorithm on an iterative implementation of DFS instead of recursive,
I think it will work better. 

(we could also try Stackless Python or decorators. I don't know decorators yet though) 


procedure DFS-iterative(G,v):
      let S be an empty stack
      S.push(v)
      while S is not empty
            v ← S.pop() 
            if v is not labeled as discovered:
                label v as discovered
                for each unvisited neighbor w of v
                    S.push(w)

"""

from collections import Counter


def basic_DFS (G, s):
    """
    Each node contains a binary variable to represent if it's been explored.
    """
    # mark the start node as explored
    G[s][2][0] = 1
    # for each neighbor
    for neighbor in G[s][0]:
        # if it hasn't been explored
        if G[neighbor-1][2] == 0:
                basic_DFS (G, neighbor-1)
    return G



def DFS_with_finish_time (G, s):
    G[s][2][0] = 1
    for neighbor in G[s][0]:
        if G[neighbor-1][2] == 0:
            DFS_with_finish_time (G, neighbor-1)
    # these three steps will be executed only when a node's neighbors have been explored.
    # the explored node gets moved to the end of the list. They will naturally line up in order.
    temp = G[s]
    G.remove(G[s])
    G.append(temp)

    return G



# build the graph
filename = "/Users/timothyroy/Documents/Algorithms Design/SCC_test3.txt"
G = makeDoubleDict(filename)

# initialize two holders to track which nodes have been visited, and what order they finished
visited_list = []
finishlist = []

def makeDoubleDict (file):
    """
    Dictionary has three lists in values. First is for incoming connections, second for
    outgoing connections, third will store leaders.
    
    Looks like: G{1:[[2,3], [4,5], [0]], 2:[[4,5], [6,7], [0]]...}

    These two lists for connections mean we don't have to reverse the graph! We just 
    use the first list on the first pass, and the second list on the second pass.
    """
    counter = 0
    G = dict()
    inFile = open(file, 'r', 0)
    for line in inFile.readlines():
        numlist = [int(x) for x in str.split(line)]
        
        if numlist[0] != counter:
            # get set up
            counter = numlist[0]
            if counter not in G:
                G[counter] = [[],[],[0]]
            # add outgoing
            G[counter][1].append(numlist[1])
            # if ingoing isn't in dictionary, add it
            if numlist[1] not in G:
                G[numlist[1]] = [[],[],[0]]
                # add as ingoing
            G[numlist[1]][0].append(counter)

        elif numlist[0] == counter:
            G[counter][1].append(numlist[1])

            if numlist[1] not in G:
                G[numlist[1]] = [[],[],[0]]
                # add as ingoing
            G[numlist[1]][0].append(counter)

    return G


# this must return the finishing times
# it does this by moving the node whose neighbors are "done"
# to the end of the list. 
def first_pass (G):
    def DFSloop (G, node):
        visited_list.append(node)
        for neighbor in G[node][0]:
            if neighbor not in visited_list:
                DFSloop(G, neighbor)
        finishlist.append(node)
        return G

    for node in range(1, len(G)+1):
        if node not in visited_list:
            DFSloop(G, node)
    return G

# here we go
first_pass(G)

# reset the list to track visited nodes in our search
visited_list = []

# this must search in decreasing order of finishing time to return the leaders in each SCC
# The third list in each dictionary entry used to serve as a boolean.
# Now that same list stores the "leaders"

def second_pass (G):
    tempnode = 0
    def DFSloop (G, node):
        G[node][2][0] = tempnode
        visited_list.append(node)
        for neighbor in G[node][1]:
            if neighbor not in visited_list:
                DFSloop(G, neighbor)
        return G

    for run in range(len(G)):
        node = finishlist.pop()
        if node not in visited_list:
            tempnode = node
            DFSloop(G, node)
    return G

second_pass(G)

# use a list comprehension to get all the values from the third lists in each dict value
final = [G[i][2][0] for i in G]

# count how many leaders there are. This is the number of members in each SCC.
print Counter(final)
