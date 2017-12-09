import math
# global variables
maxRow = 4
maxCol = 5
obs = [[0] * maxCol for x in range(maxRow)] # keep track of obstacles
rhs = [[math.inf] * maxCol for x in range(maxRow)]
g = [[math.inf] * maxCol for x in range(maxRow)]
Sstart = []
Sgoal = []
Scurrent = []
openList = [] # holds vertices to be evaluated, s = [rhs, row, columm] for each s in openList
P = [] # current predecessors
tCost = [1, 1.4] # transition cost
SEARCHING = True

def calculate(Scurrent):

	minElem = math.inf
	node = [0,0]
	for i in range(Scurrent[0] - 1, Scurrent[0] + 2):
		for j in range(Scurrent[1] - 1, Scurrent[1] + 2):
			if i < 0 or j < 0 or i >= maxRow or j >= maxCol: # outside of workspace boundary
				continue;
			else:
				if rhs[i][j] < minElem:
					minElem = rhs[i][j]
					# print(minElem)
					node[0] = i
					node[1] = j
	return node

def initialize(target, start):
	global rhs

	for i in range(2):
		Sgoal.append(target[i] // 10)
		Sstart.append(start[i] // 10)
	rhs[Sgoal[0]][Sgoal[1]] = 0
	openList.append([0, Sgoal[0], Sgoal[1]])
	return

def updateObstacles(coord):
	global obs
	# coord is obstacle, update S
	# set all obstacles to infinity
	m = coord[0] // 10
	n = coord[1] // 10
	obs[m][n] = math.inf
	return

def updateVertex(s): 
	global rhs
	global g
	# find and check all predecessors
	findPredecessors(s)
	while len(P) > 0:
		elem = P.pop(0)
		if elem[0] < 0 or elem[1] < 0 or elem[0] >= maxRow or elem[1] >= maxCol or obs[elem[0]][elem[1]] != 0:
			continue
		else:
			if elem[2] == 0: # cost = 1
				rhs[elem[0]][elem[1]] = g[s[1]][s[2]] + tCost[0]
			else:
				rhs[elem[0]][elem[1]] = g[s[1]][s[2]] + tCost[1]
			if g[elem[0]][elem[1]] != rhs[elem[0]][elem[1]]: # if inconsistent, add to openlist
				temp = [rhs[elem[0]][elem[1]], elem[0], elem[1]]
				if temp not in openList: # check if already exists in openList
					openList.append(temp)
	return
def findPredecessors(s):
	# not quite right yet
	# need to figure out way of each node being predecessor to another, yet each node may have multiple successors
	global SEARCHING
	global P

	i = s[1]
	j = s[2]
	if i < Sstart[0] and j < Sstart[1]:
		P.append([i, j + 1, 0])
		P.append([i + 1, j, 0])
		P.append([i + 1, j + 1, 1])
	elif i > Sstart[0] and j > Sstart[1]:
		P.append([i, j - 1, 0])
		P.append([i - 1, j, 0])
		P.append([i - 1, j - 1, 1])
	elif i < Sstart[0] and j > Sstart[1]:
		P.append([i, j - 1, 0])
		P.append([i + 1, j, 0])
		P.append([i + 1, j - 1, 1])
	elif i > Sstart[0] and j < Sstart[1]:
		P.append([i, j + 1, 0])
		P.append([i - 1, j, 0])
		P.append([i - 1, j + 1, 1])
	elif i < Sstart[0] and j == Sstart[1]:
		P.append([i + 1, j - 1, 1])
		P.append([i + 1, j, 0])
		P.append([i + 1, j + 1, 1])
	elif i > Sstart[0] and j == Sstart[1]:
		P.append([i - 1, j - 1, 1])
		P.append([i - 1, j, 0])
		P.append([i - 1, j + 1, 1])
	elif i == Sstart[0] and j > Sstart[1]:
		P.append([i, j - 1, 0])
		P.append([i + 1, j - 1, 1])
		P.append([i - 1, j - 1, 1])
	elif i == Sstart[0] and j < Sstart[1]:
		P.append([i, j + 1, 0])
		P.append([i - 1, j + 1, 1])
		P.append([i + 1, j + 1, 1])
	else:
		print("found starting point")
		SEARCHING = False
	return

def shortestPath(obstacles):
	global g
	global Sgoal
	global SEARCHING

	for obstacle in obstacles:
		updateObstacles(obstacle)
	openList.sort()
	if len(openList) == 0:
		SEARCHING = False
		return
	s = openList.pop(0)  # pop min item on stack
	if g[s[1]][s[2]] != rhs[s[1]][s[2]]:
		g[s[1]][s[2]] = rhs[s[1]][s[2]]
	updateVertex(s)
	return 


def main():
	global Sstart

	path = []
	print("Grabbing target and obstacle coordinates...\n")
	start = [22, 44]
	target = [0, 0]
	obstacles = [[3, 23], [12, 12], [13, 23]]
	initialize(target, start)
	shortestPath(obstacles)
	while SEARCHING is True:
		if g[Sstart[0]][Sstart[1]] == rhs[Sstart[0]][Sstart[1]] and rhs[Sstart[0]][Sstart[1]] < openList[0][0]: # conditions satisfied, optimal path found
			break
		else:
			shortestPath(obstacles)

	Scurrent = Sstart
	while Sgoal != Scurrent:
		node = calculate(Scurrent)
		path.append(node)
		Scurrent = node
	# Now move motors to values along path (or skip every second value or some shit for larger subgoals)
	print(path)
	# print(obs)
	# print(g)
	# print(openList)
	print(rhs)
	print(Sstart)
	# print(Sgoal)
	return

if __name__ == '__main__':
	main()
