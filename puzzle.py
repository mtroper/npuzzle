import numpy
import math

#--------------------------part 1--------------------------

#Loading and Representing Game States
# Argument: filepath
# Returns: 2d array
def loadFromFilePath(filepath):
    file = open(filepath, "r")
    #everything is in try and except to handle with possible bad input
    try:
        #handles possibility of non integer input
        n = int(next(file))
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
        #checks if there are duplicates or more than one or no holes
        if len(numbers) != len(set(numbers)) or hole != 1:
            print("Invalid Input")
            return
        file.close()
        return puzzle
    except:
        print("Invalid Input")
        return

#--------------------------part 2--------------------------

def validNeighbor(zero_coord, target, state):
    (z_x, z_y) = zero_coord
    (x, y) = target
    if(x >= len(state) or y >= len(state) or x < 0 or y < 0):
      return None
    out_list = numpy.array(state).copy()
    out_list[z_y][z_x] = out_list[y][x]
    out_list[y][x] = 0
    return(( state[y][x], numpy.array(out_list).flatten().tolist() ))

#Compute Neighbors
# Argument: 2d array
# Returns: collection of pairs, pairs consist of (int,1d array)
def ComputeNeighbors(state):
    out = []
    (zero_y,zero_x) = [ind for ind, num in numpy.ndenumerate(numpy.array(state)) if num == 0][0]
    #up, down, left, right
    out.append(validNeighbor( (zero_y, zero_x),(zero_y-1, zero_x),state  ))
    out.append(validNeighbor( (zero_y, zero_x),(zero_y+1, zero_x),state  ))
    out.append(validNeighbor( (zero_y, zero_x),(zero_y, zero_x-1),state  ))
    out.append(validNeighbor( (zero_y, zero_x),(zero_y, zero_x+1),state  ))
    return list(filter(None, out))

#Is goal
# Argument: 2d array
# Returns: boolean
def isGoal(state):
    mat = [numpy.arange(i, i+len(state)).tolist() for i in range(1, len(state)**2, len(state))]
    mat[-1][-1] = 0
    return mat == state

#--------------------------part 3--------------------------

#Convert State
# Arguments: Collection of pairs
# Returns 3d Arrayoo
def convertStates(neighbors):
   n = int(math.sqrt(len(neighbors[0][1])))
   states = []
   for i in neighbors:
        list = i[1]
        state = [[0 for i in range(n)] for j in range(n)]
        line = 0
        for x in range(len(list)):
            if x%n == 0 and x != 0:
                line += 1 
            state[line][x%n] = list[x]
        states.append(state)
   return states

#Breadth First Search (BFS)
# Arguments: 2d array
# Returns: array
def BFS(state):
    frontier = [state]
    discovered = [state]
    parents = {tuple(map(tuple, state)): ()}
    while frontier:
        currentState = frontier.pop(0)
        if isGoal(currentState):
            return parents[tuple(map(tuple, currentState))]
        neighbors = convertStates(ComputeNeighbors(currentState))
        for i in range(len(neighbors)):
            s = neighbors[i]
            print(s)
            if s not in discovered:
                discovered.append(s)
                frontier.append(s)
                newPath = list(parents[tuple(map(tuple, currentState))])
                newPath.append(ComputeNeighbors(currentState)[i][0])
                parents[tuple(map(tuple, s))] = tuple(newPath)
    print("Failure")
    return None
#Depth First Search (DFS)
# Arguments
# Returns: Array
def DFS(state):
    frontier = [state]
    discovered = [state]
    parents = {tuple(map(tuple, state)): ()}
    while frontier:
        current_state = frontier.pop(0)
        if isGoal(current_state):
            return parents[tuple(map(tuple, current_state))]
        neighbors = convertStates(ComputeNeighbors(current_state))
        for i in range(len(neighbors)):
            option = neighbors[i]
            if option not in discovered:
                discovered.insert(0, option)
                frontier.insert(0, option)
                newPath = list(parents[tuple(map(tuple, current_state))])
                newPath.insert(0, ComputeNeighbors(current_state)[i][0])
                parents[tuple(map(tuple, option))] = tuple(newPath)

print(BFS(loadFromFilePath("input.txt")))