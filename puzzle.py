import numpy
import math
import cProfile, pstats
import timeit
import time
import copy
import cProfile
from collections import deque
import re
import cProfile, pstats

#--------------------------part 1--------------------------

#Loading and Representing Game States
# Argument: filepath
# Returns: 2d array
def loadFromFilePath(filepath):
    file = open(filepath, "r")
    #everything is in try and except to handle with possible bad input
    try:
        #handles possibility of non integer input
        n = int(next(file)[0])
        if n > 0:
            #making an n long 2d array
            puzzle = [[0 for i in range(n)] for j in range(n)]
            numbers = []
            currentLine = 0
            hole = 0
            for line in file:
                i = 0
                #this line makes sure n is not larger than the amount of numbers per line
                #if n were larger, than this would give an index of out bounds and go into the except
                line[(n*2)-2]
                list = line.split()
                for c in list:
                    #checking if the character is the hole
                    if c == "*":
                        hole += 1
                        #computeNeighbors needs the hole to be a 0
                        num = 0
                    else:
                        #handles possibility of non integer input
                        num = int(c)
                        #handles possibility of negative input
                        math.sqrt(num)
                    numbers.append(num)
                    puzzle[currentLine][int(i)] = num	
                    i += 1
                currentLine += 1
            #sorted(flatten(puzzle))
            #checks if there are duplicates or more than one or no holes
            if len(numbers) != len(set(numbers)) or hole != 1:
                print("Invalid Input")
                return
            file.close()
            return flatten(puzzle)
    except:
        print("Invalid Input")
        return

#--------------------------part 2--------------------------

def validNeighbor(zero_coord, target, prev_swap, state):
    #revert previous swap
    if prev_swap != -1:
        state[prev_swap],state[zero_coord] = state[zero_coord],0
    #moved
    moved = state[target]
    #swap
    state[zero_coord],state[target] = state[target],0
    return(( moved, state[:] ))

def ComputeNeighbors(state):
    out = []
    L = len(state)
    l = int(math.sqrt(L))
    for i in range(L):
        if state[i] == 0:
            zero = i
    swapped = -1
    row = math.ceil((zero+1)/l)

    if zero-l >= 0:
        out.append(validNeighbor( zero, zero-l, swapped, state ))
        swapped = zero - l
    if zero+l < L:
        out.append(validNeighbor( zero, zero+l, swapped, state ))
        swapped = zero + l
    if math.ceil((zero+2)/l) == row:
        out.append(validNeighbor( zero, zero+1, swapped, state ))
        swapped = zero + 1
    if math.ceil((zero)/l) == row:
        out.append(validNeighbor( zero, zero-1, swapped, state ))
        swapped = zero - 1

    state[swapped],state[zero] = state[zero],0
    return out

#Is goal
# Argument: 2d array
# Returns: boolean
def isGoal(state):
    mat = [i for i in range(1, len(state)+1)]
    mat[-1] = 0
    return mat == state

def findGoal(state):
    goal = []
    for i in range(len(state)):
        goal.append(i + 1)
    goal[len(state) - 1] = 0
    return goal

#--------------------------part 3--------------------------

def flatten(state):
    flattened = []
    for x in state:
        flattened += x
    return flattened

#Breadth First Search (BFS)
# Arguments: 2d array
# Returns: array
def BFS(state):
    total = 0
    #this will be false if loadFromFilePath detects bad input
    if state:
        frontier = deque([state])
        #making discovered a set of flattened tuples
        discovered = {tuple(state)}
        #making parents a dictionary 
        parents = {tuple(state): ()}
        while frontier:
            #isgoal
            currentState = frontier.popleft()
            # currentState = deque(frontier).popleft()
            if isGoal(currentState):
                return parents[tuple(currentState)]
            neighbors = ComputeNeighbors(currentState)
            for i in range(len(neighbors)):
                s = tuple(neighbors[i][1])
                if s not in discovered:
                    discovered.add(s)
                    frontier.append(list(s))
                    newPath = list(parents[tuple(currentState)])
                    newPath.append(neighbors[i][0])
                    parents[s] = tuple(newPath)
            #print(total)
        print("Failure")

#Depth First Search (DFS)
# Arguments:
# Returns: Array
def DFS(state):
    total1 = 0
    count = 0
    #this will be false if loadFromFilePath detects bad input
    if state:
        frontier = [state]
        #making discovered a set of flattened tuples
        discovered = {tuple(state)}
        #making parents a dictionary 
        parents = {tuple(state): ()}
        while frontier:
            #isgoal
            currentState = frontier.pop(0)
            print(currentState)
            count += 1
            print(count)
            # currentState = deque(frontier).popleft()
            if isGoal(currentState):
                return parents[tuple(currentState)]
            neighbors = ComputeNeighbors(currentState)
            for i in range(len(neighbors)):
                s = tuple(neighbors[i][1])
                if s not in discovered:
                    discovered.add(s)
                    frontier.insert(0, list(s))
                    newPath = list(parents[tuple(currentState)])
                    newPath.append(neighbors[i][0])
                    parents[s] = tuple(newPath)
        print("Failure")

def BDS(state):
    goal = findGoal(state)
    total = 0
    #this will be false if loadFromFilePath detects bad input
    if state:
        frontier_front = [state]
        frontier_back = [goal]
        #making discovered a set of flattened tuples
        discovered_front = {tuple(state)}
        discovered_back = {tuple(goal)}
        #making parents a dictionary 
        parents_front = {tuple(state): ()}
        parents_back = {tuple(goal): ()}

        while frontier_front and frontier_back:
            currentState_front = frontier_front.pop(0)
            currentState_back = frontier_back.pop(0)
            
            t1 = time.time()
            neighbors_front = ComputeNeighbors(currentState_front)
            neighbors_back = ComputeNeighbors(currentState_back)
            total += (time.time()-t1)

            for i in range(len(neighbors_front)):
                s_front = tuple(neighbors_front[i][1])
                if s_front not in discovered_front:
                    discovered_front.add(s_front)
                    frontier_front.append(list(s_front))
                    newPath_front = list(parents_front[tuple(currentState_front)])
                    newPath_front.append(neighbors_front[i][0])
                    parents_front[s_front] = tuple(newPath_front)
                                
                if bool(discovered_front.intersection(discovered_back)):
                    # print(list(discovered_front))
                    shared_member = discovered_front.intersection(discovered_back)
                    shared_member = [item for t in shared_member for item in t]
                    print(shared_member)
                    # new_arr = list(parents_front[tuple(shared_member)])
                    # print(list(parents_front[tuple(shared_member)]))
                    # print(list(parents_back[tuple(shared_member)]))
                    # for i in range(len(list(parents_back[tuple(shared_member)]))):
                    #     new_arr.append(list(reversed(parents_back[tuple(shared_member)])))
                    new_arr = []
                    new_arr.append(list(parents_front[tuple(shared_member)]))
                    new_arr.append(list(reversed(parents_back[tuple(shared_member)])))
                    
                    return new_arr

            for i in range(len(neighbors_back)):
                s_back = tuple(neighbors_back[i][1])
                if s_back not in discovered_back:
                    discovered_back.add(s_back)
                    frontier_back.append(list(s_back))
                    newPath_back = list(parents_back[tuple(currentState_back)])
                    newPath_back.append(neighbors_back[i][0])
                    parents_back[s_back] = tuple(newPath_back)
                     
        print("Failure")

print(BFS(loadFromFilePath("input.txt")))




