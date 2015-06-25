from queue import PriorityQueue
dx = [0,  1, 0, -1]
dy = [-1, 0, 1,  0]
legend = 'urdl'

level=['.##.....#.',
       '###....#..',
       '......x#.#',
       '.#.....#..',
       '.#..#x..##',
       '..........',
       '...x...#..',
       '..........',
       '......x.##',
       '#...#...#.']
head = (0,0)


def isWall(node):
    if level[node[0]][node[1]] == '#':
        return True
    return False

def isFood(node):
    if level[node[0]][node[1]] == 'x':
        return True
    return False
    

    
def mapLevel(start):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    foodlist = {}
    cost = {}
    came_from = {}
    cost[start] = 0
    came_from[start] = None
    while(not frontier.empty()):
        current = frontier.get()
        neighbours = [((current[0] + dx[i])%10, (current[1] + dy[i])%10) for i in range(4)]
        for node in neighbours:
            
            new_cost = cost[current] + 1
            testBool = (node not in came_from or new_cost < cost[node]) and not isWall(node) 
            if testBool:
                if isFood(node):
                    foodlist[node] = new_cost
                came_from[node] = current
                cost[node] = new_cost
                frontier.put(node, new_cost)
    print(foodlist)
    minimum = 10**6
    for node in foodlist:
        if foodlist[node] < minimum:
            closest_food = node
            minimum = foodlist[node]
    print(closest_food)
    return [came_from, cost, closest_food]

temp = mapLevel(head)
arrowMap, lengthMap, closest_food = temp[0], temp[1], temp[2]

def givePath(goal):
    current = goal
    path = [current]
    while current != head:
        current = arrowMap[current]
        path.append(current)
    path.reverse()
    return path

def giveDistance(goal):
   return lengthMap[goal]

print(givePath(closest_food))    


source = 'http://www.redblobgames.com/pathfinding/a-star/introduction.html'