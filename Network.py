import itertools
import pickle
import copy

from datetime import timedelta
from Class import Node
import Nodes
from Nodes import source, epoch


Net = []        # nodes by name
lines = []      # a list of node pairs for PERT line connections
paths = []      # a list of node chains for each pair of start/end nodes
Deps = [[]]     # dependencies, row # determines dependence level
Start = []      # start nodes
End = []        # end nodes
level = 0

# load saved nodes into list
try:
    file = open(source, "x")
    file.close()
except:
    pass
file = open(source, "rb")
try:
    allNodes = pickle.load(file)
except:
    allNodes = []
file.close()

# update Node class registry with loaded nodes
for obj in allNodes:
    try:
        obj.registry.remove(getattr(Nodes, obj.name))
        print("Updated event " + obj.name)
    except:     # this should occur if a new node is created
        print("Created event " + obj.name)
    setattr(Nodes, obj.name, copy.deepcopy(obj))
    Obj = getattr(Nodes, obj.name)
    Obj.registry.append(Obj)

print("Network.py was called")

# overwrite the save file with Node class registry data
open(source, "w").close()
allNodes = []

for obj in Node.registry:
    allNodes.append(obj)

file = open(source, "wb")
pickle.dump(allNodes, file)
file.close()


# find all start nodes, aka events without dependencies
for elem, nodeObj in enumerate(allNodes):
    Net.append(nodeObj.name) # also collects all nodes

    # identify all independent nodes, aka start nodes
    if not nodeObj.dep:
        Start.append(nodeObj.name)
        Deps[level].append(nodeObj.name)
        nodeObj.lvl = level
        nodeObj.x = int((nodeObj.start - epoch) / timedelta(days=1))    # set the x position in the mainframe
        nodeObj.y = int(elem)                                               # set the y position in the mainframe
        nodeObj.end = nodeObj.start + timedelta(days=nodeObj.dur)           # set end date of the start node

# find all end nodes, events that are not dependencies of other events
for elem, nodeObj in enumerate(allNodes):
    End += nodeObj.dep

End = list(set(Net) - set(End))

# pathfinding
paths = []  # paths currently being traced
s2e = []    # start-to-end paths


def searchPaths():
    for nodeName in End:
        obj = getattr(Nodes, nodeName)
        for depName in obj.dep:
            path = [nodeName]
            depObj = getattr(Nodes, depName)
            if depName in Start:
                path += depName
                s2e.append(path)
                return []
            else:
                path += searchPaths()


# rank all other nodes that have dependencies on longest dependency path
while not set(Net) == set(list(itertools.chain.from_iterable(Deps))):
    level += 1
    Deps.append([])
    Deps_itr = copy.deepcopy(Deps)

    # iterate over all nodes
    index = 0
    for elem, nodeObj in enumerate(allNodes):

        # identify nodes that only have registered dependencies
        if nodeObj.dep and set(nodeObj.dep).issubset(set(list(itertools.chain.from_iterable(Deps))))\
                and not set(nodeObj.name).issubset(list(itertools.chain.from_iterable(Deps))):
            Deps_itr[level].append(nodeObj.name)
            nodeObj.lvl = level
            latest = nodeObj.start

            # find the latest start date from dependencies
            for depName in nodeObj.dep:
                depObj = getattr(Nodes, depName)
                lines.append([depObj.name, nodeObj.name])   # connect nodes

                # record the latest start date
                if depObj.end >= latest:
                    latest = depObj.end
                    nodeObj.crit = depObj.name   # mark critical path

            nodeObj.start = latest
            nodeObj.end = nodeObj.start + timedelta(days=nodeObj.dur)
            nodeObj.x = int((nodeObj.start - epoch) / timedelta(days=1)) * 10
            nodeObj.y = index*5 + level
            index += 1

    Deps = copy.deepcopy(Deps_itr)

# eliminate redundant dependencies

for pair in lines:
    for item in Net:
        if [pair[0], item] in lines and [item, pair[1]] in lines:
            lines.remove(pair)

print(Start)
