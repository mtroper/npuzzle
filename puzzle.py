import numpy
import math
import copy
from collections import deque

# LoadFromFile
# Argument: filepath
# Returns: 2d array
def LoadFromFile(filepath):
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
            if len(numbers) != len(set(numbers)) or hole != 1 or sorted(numbers) != [*range(len(numbers))]:
                print("Invalid Input")
                return
            file.close()
            return numbers
    except:
        print("Invalid Input")
        return

# Flatten
# Arguments: 2d array
# Returns: 1d array
def flatten(state):
    return [x for x in state]

# Valid Neighbor
# Arguments: int, int, int, 1d array
# Returns: tuple (int, 1d array)
def validNeighbor(zero_coord, target, prev_swap, state):
    #revert previous swap
    if prev_swap != -1:
        state[prev_swap],state[zero_coord] = state[zero_coord],0
    #moved
    moved = state[target]
    #swap
    state[zero_coord],state[target] = state[target],0
    return(( moved, state[:] ))

# Compute Neighbors
# Arguments: 1d array
# Returns: list of tuples (int, 1d array)
def ComputeNeighbors(state):
    out = []
    L = len(state)
    l = int(math.sqrt(L))
    #finds index of zero
    for i in range(L):
        if state[i] == 0:
            zero = i
    swapped = -1
    row = math.ceil((zero+1)/l)
	
    #checks and appends neighbors: Up, down, right, left
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
	#swaps back to original state
    state[swapped],state[zero] = state[zero],0
    return out

# Is goal
# Argument: 1d array
# Returns: boolean
def isGoal(state):
    #makes the goal state and checks if its the same as state
    mat = [i for i in range(1, len(state)+1)]
    mat[-1] = 0
    return mat == state

# Find Goal
# Argument: 1d array
# Returns: 1d array
def findGoal(state):
    #makes the ideal goal state
    goal = [i + 1 for i in range(len(state))]
    goal[-1] = 0
    return goal

#Breadth First Search (BFS)
# Arguments: 1d array
# Returns: tuple
def BFS(state):
    #only runs if the state is valid input
    if state:
        frontier = deque([state])
        #makes discovered a set of flattened tuples
        discovered = {tuple(state)}
        #makes parents a dictionary 
        parents = {tuple(state): ()}
        while frontier:
            currentState = frontier.popleft()
            #if the current state is correct, it returns parents
            if isGoal(currentState):
                return parents[tuple(currentState)]
            neighbors = ComputeNeighbors(currentState)
            #goes through every neighbor
            for i in range(len(neighbors)):
                s = tuple(neighbors[i][1])
                if s not in discovered:
                  	#if its not a discovered state, add it to frontier and discovered
                    discovered.add(s)
                    frontier.append(list(s))
                    newPath = list(parents[tuple(currentState)])
                    newPath.append(neighbors[i][0])
                    parents[s] = tuple(newPath)
        print("Failure")

# Depth First Search (DFS)
# Arguments: 1D array
# Returns: Tuple
def DFS(state):
    #only runs if the state is valid input
    if state:
        frontier = deque([state])
        #making discovered a set of flattened tuples
        discovered = {tuple(state)}
        #making parents a dictionary 
        parents = {tuple(state): ()}
        while frontier:
            # currentState = deque(frontier).popleft()
            currentState = frontier.popleft()
            #if the current state is correct, it returns parents
            if isGoal(currentState):
                return parents[tuple(currentState)]
            neighbors = ComputeNeighbors(currentState)
            for i in range(len(neighbors)):
                s = tuple(neighbors[i][1])
                if s not in discovered:
                  	#if its not a discovered state, add it to frontier and discovered
                    discovered.add(s)
                    #Adds the neighbor to the front, simulating a stack
                    frontier.insert(0, list(s))
                    newPath = list(parents[tuple(currentState)])
                    newPath.append(neighbors[i][0])
                    parents[s] = tuple(newPath)
        #if it exhausts all neighbors without a solution, it fails
        print("Failure")

# Bidirectional Search (BDS)
# Arguments: 1D Array
# Returns: Tuple
def BDS(state):
    goal = findGoal(state)
    #this will be false if loadFromFilePath detects bad input
    if state:
        frontier_front = deque([state])
        frontier_back = deque([goal])
        #making discovered front and back a set of flattened tuples
        discovered_front = {tuple(state)}
        discovered_back = {tuple(goal)}
        #making parents front and back a dictionary 
        parents_front = {tuple(state): ()}
        parents_back = {tuple(goal): ()}
		#this will return none if either frontier is empty without intersection
        while frontier_front or frontier_back:
            #creating front and back current state
            currentState_front = frontier_front.popleft()
            currentState_back = frontier_back.popleft()
    		#neighbors of front and back current states
            neighbors_front = ComputeNeighbors(currentState_front)
            neighbors_back = ComputeNeighbors(currentState_back)
            #looping through front BFS neighbors
            for i in range(len(neighbors_front)):
                s_front = tuple(neighbors_front[i][1])
                #if its not a discovered state, add it to frontier and discovered
                if s_front not in discovered_front:
                    discovered_front.add(s_front)
                    frontier_front.append(list(s_front))
                    newPath_front = list(parents_front[tuple(currentState_front)])
                    newPath_front.append(neighbors_front[i][0])
                    parents_front[s_front] = tuple(newPath_front)
                #checking intersection of discovered sets
                if bool(discovered_front.intersection(discovered_back)):
                    shared_member = discovered_front.intersection(discovered_back)
                    shared_member_orig = [item for t in shared_member for item in t]
                    shared_member = []
                    for i in range(len(state)):
                        shared_member.append(shared_member_orig[i])
                    #returning parents of front and back BFS
                    new_arr = []
                    new_arr = (list(parents_front[tuple(shared_member)]))
                    back_parents = list(reversed(parents_back[tuple(shared_member)]))
                    for i in range(len(back_parents)):
                        new_arr.append(back_parents[i])
                    return tuple(new_arr) 
            #loops through back BFS neighbors
            for i in range(len(neighbors_back)):
                s_back = tuple(neighbors_back[i][1])
                #if its not a discovered state, add it to frontier and discovered
                if s_back not in discovered_back:
                    discovered_back.add(s_back)
                    frontier_back.append(list(s_back))
                    newPath_back = list(parents_back[tuple(currentState_back)])
                    newPath_back.append(neighbors_back[i][0])
                    parents_back[s_back] = tuple(newPath_back)
        print("Failure")