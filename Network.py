import itertools
from Class import Node, timedelta
import Nodes


Net = []    # nodes by name
lines = []  # a list of node pairs for PERT line connections
Deps = []   # dependencies, row # determines dependence level
Ends = []   # end nodes
level = 0


# find all events (nodes) without dependencies, aka start nodes
for elem, nodeObj in enumerate(Node.registry):
    Deps.append([])
    Net.append(nodeObj.name)

    # identify all independent nodes, aka start nodes
    if not nodeObj.dep:
        Deps[level].append(nodeObj.name)
        nodeObj.lvl = level
        nodeObj.x = int((nodeObj.start - Nodes.epoch) / timedelta(days=1))    # set the x position in the mainframe
        nodeObj.y = int(elem)                                               # set the y position in the mainframe
        nodeObj.end = nodeObj.start + timedelta(days=nodeObj.dur)           # set end date of the start node


# find all events (nodes) that are not dependencies of other nodes, aka end nodes
for elem, nodeObj in enumerate(Node.registry):
    Ends += nodeObj.dep

Ends = list(set(Net)-set(Ends)-set(list(itertools.chain.from_iterable(Deps))))


# rank all other nodes that have dependencies on longest dependency path
while not set(Net) == set(list(itertools.chain.from_iterable(Deps)) + list(itertools.chain.from_iterable(Ends))):
    level += 1
    Deps.append([])
    Deps_itr = Deps

    # iterate over all nodes
    for elem, nodeObj in enumerate(Node.registry):

        # identify nodes that only have registered dependencies
        if nodeObj.dep and set(nodeObj.dep).issubset(set(list(itertools.chain.from_iterable(Deps_itr))))\
                and not set(nodeObj.name).issubset(list(itertools.chain.from_iterable(Deps_itr))):
            Deps_itr[level].append(nodeObj.name)
            nodeObj.lvl = level
            latest = nodeObj.start

            # ------------------------------------------------
            # code to eliminate redundant node dependency here
            # ------------------------------------------------

            # find the latest start date from dependencies
            for depName in nodeObj.dep:
                depObj = getattr(Nodes, depName)
                lines.append([nodeObj.name, depObj.name])   # connect nodes

                # record the latest start date
                if depObj.end >= latest:
                    latest = depObj.end
                    nodeObj.crit = depObj.name   # mark critical path

            nodeObj.start = latest
            nodeObj.end = nodeObj.start + timedelta(days=nodeObj.dur)
            nodeObj.x = int((nodeObj.start - Nodes.epoch) / timedelta(days=1))
            nodeObj.y = int(elem)

    Deps = Deps_itr
