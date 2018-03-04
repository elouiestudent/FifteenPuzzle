#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6

import sys
import time
import queue
def allStates(numbers, states):
    l = set()
    index = numbers.find("_")
    for place in states[index]:
        newNum = numbers[:index] + numbers[place] + numbers[index + 1:]
        newNum = newNum[:place] + "_" + newNum[place + 1:]
        l.add(newNum)
    return l

def puzzling(start, states, goal, positions, finalPositions):
    puzzlesRemove = 0
    improve = 0
    counts = dict()
    keysSeen = set()
    closedSet = dict()
    openSet = queue.PriorityQueue()
    keysSeen.add(start)
    counts[start] = 0
    if start == goal:
        return closedSet, openSet.qsize(), puzzlesRemove, improve
    openSet.put((findManhattan(start, positions, finalPositions),start,""))
    while openSet:
        element = openSet.get(0)
        var = element[1]
        parent = element[2]
        puzzlesRemove += 1
        count = counts[var]
        newList = allStates(var,states)
        for i in newList:
            if i == goal:
                closedSet[i] = var
                closedSet[var] = parent
                return closedSet, openSet.qsize(), puzzlesRemove, improve
            if i in closedSet.keys(): continue
            heuristic = findManhattan(i, positions, finalPositions) + count + 1
            if i in keysSeen:
                improve += 1
            else:
                keysSeen.add(i)
            openSet.put((heuristic, i, var))
            counts[i] = count + 1
        closedSet[var] = parent
    return [], openSet.qsize(), puzzlesRemove, improve

def createStates():
    states = dict()
    states[0] = {1,4}
    states[1] = {0,2,5}
    states[2] = {1,3,6}
    states[3] = {2,7}
    states[4] = {0,5,8}
    states[5] = {1,4,6,9}
    states[6] = {2,5,7,10}
    states[7] = {3,6,11}
    states[8] = {4,9,12}
    states[9] = {5,8,10,13}
    states[10] = {6,9,11,14}
    states[11] = {7,10,15}
    states[12] = {8,13}
    states[13] = {9,12,14}
    states[14] = {10,13,15}
    states[15] = {11,14}
    return states

def createPositions():
    states = dict()
    states[0] = [0,0]
    states[1] = [1,0]
    states[2] = [2,0]
    states[3] = [3,0]
    states[4] = [0,1]
    states[5] = [1,1]
    states[6] = [2,1]
    states[7] = [3,1]
    states[8] = [0,2]
    states[9] = [1,2]
    states[10] = [2,2]
    states[11] = [3,2]
    states[12] = [0,3]
    states[13] = [1,3]
    states[14] = [2,3]
    states[15] = [3,3]
    return states

def createFinalPositions(goal,positions):
    finalPositions = dict()
    for i in range(len(goal)):
        finalPositions[goal[i]] = positions[i]
    return finalPositions

def findManhattan(test,positions,finalPositions):
    sum = 0
    for i in range(len(test)):
        if test[i] != "_":
            testPos = positions[i]
            finalPos = finalPositions[test[i]]
            for t,f in zip(testPos,finalPos):
                sum += abs(t - f)
    return sum

def printer(numbers):
    numbers = numbers[:4] + "\n" + numbers[4:8] + "\n" + numbers[8:12] + "\n" + numbers[12:]
    return numbers

def inversionCount(start):
    return len([1 for i in range(len(start) - 1) for j in range(i + 1, len(start)) if start[i] > start[j]])
#
# def anotherInversionCount(start):
#     return sum([start[i] > start[j] for i in range(len(start) - 1) for j in range(i + 1, len(start))])

def inversionCountParity(start):
    return len([1 for i in range(len(start) - 1) for j in range(i + 1, len(start)) if start[i] > start[j]]) & 1

def rowDifference(start, pos, fpos):
    sPos = pos[start.index("_")]
    return abs(sPos[1] - fpos["_"][1])

startTime = time.clock()
start = sys.argv[1]
goal = "ABCDEFGHIJKLMNO_"
pos = createPositions()
fpos = createFinalPositions(goal, pos)
states = createStates()
l = list()
if (inversionCount(start.replace("_","")) + rowDifference(start, pos, fpos)) & 1 != inversionCount(goal.replace("_","")) & 1:
    print("No Solution")
else:
    d, leno, puzzlesRemoved, improve = puzzling(start, states, goal, pos, fpos)
    key = goal
    l.append(printer(key))
    while len(d[key]) > 0:
        l.append(printer(d[key]))
        key = d[key]
    print("States:\n\n" + "\n\n".join(l[::-1]), "\n\nSteps:", len(l) - 1)
    print("Number of times improved in openSet:",improve)
    print("Number of elements in openSet:",leno)
    print("Number of elements in closedSet:",len(d))
    print("States removed from openSet:",puzzlesRemoved)
    print("Time:", time.clock() - startTime)