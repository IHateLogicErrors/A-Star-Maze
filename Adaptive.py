import heapq as hpq
from datetime import datetime
import numpy as np
import ui
import Utility

SIZE = 101
GOAL = [100, 100]
openList = []
closed = dict() # always empty at start
curPath = []
finalPath = []
nodes = 0
start = [0, 0]
maxSize = 0

# updates map before planning route
def updateMap(loc):
    for x in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
        a = np.add(loc, x)
        a = list(a)
        if Utility.inRange(a, SIZE):
            currentMap[a[0], a[1]] = currentMap[a[0], a[1]] % 2


# expands each node around current and makes sure we haven't been
# there or isn't blocked
def createPossible(loc):
    locs = []
    global openList
    for x in [[-1,0], [1, 0], [0,-1], [0, 1]]:
        a = np.add(loc, x)
        a = list(a)
        if Utility.inRange(a, SIZE) and currentMap[a[0], a[1]] != 1 and not any(x.loc == a for x in openList) \
                and a not in curPath:
                locs.append(a)
    return locs

# while we have nodes to go to

# print path by starting at goal
def getPath(start, g, current):
    cur = current
    global closed
    for x in curPath: # only update ones we went to
        closed[str(x)] = g - closed[str(x)]
    pathL = [cur.loc]
    while cur.loc != start:
        cur = cur.parent
        pathL.append(cur.loc)
    pathL.reverse()
    return pathL


# finds a path using A*
def findPath(start):
    g = 0 # used for adaptive
    global openList
    global closed
    openList = []
    hpq.heappush(openList, Utility.Node(start, hi=Utility.distance(start, GOAL)))
    foundGoal = False
    current = None
    while openList:
        current = hpq.heappop(openList) # get next best position
        if current.loc == GOAL: # found goal
            g = current.g  # get final g
            foundGoal = True
            break

        closed[str(current.loc)] = current.g  # add node to closed list
        curPath.append(current.loc)

        #print(current)
        global nodes
        nodes += 1

        possibleMoves = createPossible(current.loc)  # get list of all possible nodes
        for x in possibleMoves:
            node = Utility.Node(x, current, current.g + 1, Utility.distance(x, GOAL, closed))
            hpq.heappush(openList, node)  # add it to binary heap

    if foundGoal:
        return getPath(start, g, current)
    else:
        return []


# move agent and remove fog of war
def moveAgent(path):
    global finalPath
    for y,x in enumerate(path):
        global finalPath
        if currentMap[x[0], x[1]] == 0:
            updateMap(x)  # remove fog of war
            global agent
            agent = x
            finalPath.append(x)
        else:
            finalPath = finalPath[:-1]
            global curPath
            curPath = [path[y-1]] # reset current path
            break

def Start(start, goal, mapA):
    startTime = datetime.now()
    global size
    size = len(mapA)
    global currentMap
    currentMap = mapA + 2
    global GOAL
    GOAL = goal
    global agent
    agent = start
    updateMap(agent)  # remove fog of war
    global nodes
    nodes = 0
    global finalPath
    while agent != goal:
        path = findPath(agent)  # get path (need to create one for reverse)
        # print(path)
        if path:  # if there is a path, move agent
            moveAgent(path)
        else:  # no path, unable to get to goal
            finalPath = []
            #print("No path found")
            break

    closed.clear()
    # if finalPath:
    #     print("Final path = {}".format(finalPath))
    # ui.gui(currentMap, len(currentMap), start, goal, finalPath)
    return [nodes, datetime.now() - startTime,bool(finalPath)]