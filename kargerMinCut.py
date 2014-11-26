import random
import copy

def Karger_cut (array, iteration):
    random.seed(iteration)
# while more than 2 vertices remain
    while len(array) > 2: 
        # pick an edge(u,v) uniformly at random
        head_vertex = random.choice(dict.keys(array))
        tail_vertex = random.choice(array[head_vertex])
        # add all edges from one list into the other
        array[head_vertex].extend(array[tail_vertex])
        
        # change all references to merged node to the surviving node
        for node in array:
            while tail_vertex in array[node]:
                array[node].remove(tail_vertex)
                array[node].append(head_vertex)

        # remove any self loops
        while head_vertex in array[head_vertex]:
            array[head_vertex].remove(head_vertex)

        # delete merged node
        del array[tail_vertex]
    # the remaining two nodes have an equal number of edges; return one
    result = len(dict.values(array)[0])
    return result


# build a dictionary from the file
filename = "/Users/timothyroy/Documents/Algorithms Design/kargerMinCut.txt"

#filename = "/Users/timothyroy/Documents/Algorithms Design/hw3test1.txt"

def makedict(file):
    array_dict = {}
    inFile = open(file, 'r', 0)
    for line in inFile.readlines():
        numlist = str.split(line)
        array_dict[numlist[0]] = numlist[1:]
    inFile.close()
    return array_dict

def keep_best_result(filename):
    result = 1000
    for iteration in range(200):
        array = makedict(filename)
        new_result = Karger_cut(array, iteration)
        if new_result < result:
            result = new_result
            print "updated result: ", result
    return result

print keep_best_result(filename)

