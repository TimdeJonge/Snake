from snake import Snake
from copy import deepcopy
from queue import PriorityQueue
       #Het onderstaande is een simulatie van echte data zoals die binnen zou kunnen komen.
       #Dit zijn alle variabelen die we uit player.py nodig zullen hebben.
       #Het is ook alles wat we binnen dit bestand zullen gebruiken.
       #In dit bestand zijn coordinaten in de vorm (x,y).

dx = [0,  1, 0, -1]
dy = [-1, 0, 1,  0]
    
level = ['..................................................',
'.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#', 
'.............................x..x.................',
'.#.#.#.#.#.#.#x#.#.#.#.#.#.#.#.#.#.#.#.#.#.#x#.#.#',
'.....................x...........................x',
'.#.#.#.#.#.#.#.#.#x#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#',
'............x.....................................',
'.#x#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#', 
'..0.......................................1.......',
'.#.#.#.#.#.#.#.#x#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#']
level_hoogte = 10
level_breedte = 50
snakes = [Snake([(2,8)]), Snake([(41,8)])]
speler_nummer = 0 
aantal_spelers = 2 
aantal_voedsel = 10
voedsel_posities = [(29,2), (32,2), (44,3), (14,3), (21,4), (49,4), (20,5), (12,6), (2,7), (16,9)]


       #We kennen een waarde toe aan alle muren
       #Deze moet overgezet worden in het bestand waarin het gebruikt wordt.
wall_value = 1000

       #Lijst maken van alle buurvakjes

def isWall(node):
    if level[node[1]][node[0]] in ['0', '1', '2', '3', '4', '5' ,'6', '7', '#']:
        return True
    return False

def isFood(node):
    if level[node[1]][node[0]] == 'x':
        return True
    return False

def givePath(start, goal):
    
    temp = mapLevel(start)
    lengthMap = temp[0]
    arrowMap = temp[1]
    
    current = goal
    path = [current]
    while lengthMap[current] != 0: 
        current = arrowMap[current]
        path.append(current)
    path.reverse()
    return path
    
def mapLevel(start):
    cost = {}
    came_from = {}
    frontier = PriorityQueue()
    frontier.put((0,start))

    cost[start] = 0
    came_from[start] = None
    while(not frontier.empty()):
        current = frontier.get()[1]

        #print(current, cost[current])          
        neighbourList = neighbours(current)

        for node in neighbourList:
            new_cost = cost[current] + 1                                # Hier wordt de cost van iedere stap aangenomen als 1. Mogelijk wordt dit op enig punt veranderd.
            testBool = (node not in came_from or new_cost < cost[node]) and not isWall(node) 
            if testBool:
                came_from[node] = current
                cost[node] = new_cost
                frontier.put((new_cost,node))
    return([cost, came_from])
    
def mapFood():
    foodDistance = {}
    close_food = []
    
    for food in voedsel_posities:
        foodDistance[food] = []                 #Dit is geen mooie oplossing, wat mij betreft
                                                #Ik ben er alleen nog niet zo uit hoe het wel te doen.
    for i in range(aantal_spelers):
        head = snakes[i].head
        temp = mapLevel(head)
        lengthMap = temp[0]
        
        for food in voedsel_posities:           #Mocht voedsel bereikbaar zijn, wordt de afstand van speler naar voedsel
                                                #gegeven door foodDistance[voedsel_positie][speler_nummer].
                                                #Mocht het niet bereikbaar zijn, levert dit -1.
            if food in lengthMap:
                foodDistance[food].append(lengthMap[food])  
            else:
                foodDistance[food].append(-1)

    #print(foodDistance)
    for food in foodDistance:
        minimum = 10**6             #Waarde hoog gekozen zodat er duidelijk verschil is tussen het geval
        next_best = 10**6           #waar er 2 personen bij kunnen en waar er 1 persoon bij kan
        closest_player = (speler_nummer + 1) % aantal_spelers       #Default: Als niemand er bij kan, doe alsof iemand anders het dichtst bij is 
        
        for i in range(aantal_spelers): 
            length = foodDistance[food][i]
            if length == -1:
                continue
            elif length > minimum:
                if length < next_best:
                    next_best = length
            else: 
                if minimum < 10**6:
                    next_best = minimum
                minimum = length
                closest_player = i
        if closest_player == speler_nummer:
            if next_best - minimum < 2000:          #Als wij niet de enige zijn:
                close_food.append([food, next_best - minimum])
    return(close_food)
    
    
def giveDirection(start, goal):
       if start[0] == goal[0]:
              if start[1] == goal[1] + 1:
                     direction = 'u'
              else:
                     direction = 'd'
       elif start[0] == goal[0] + 1:
              direction = 'l'
       else:
              direction = 'r'
       return(direction)


def neighbours(coordinate):
       neighbourList = []
       for i in range(4):
              neighbourList.append(((coordinate[0] + dx[i]) % level_breedte, (coordinate[1] + dy[i]) % level_hoogte))
       return neighbourList

def mapHeat():
       #Zorgen dat level aanpasbaar is (alles wordt 0)
       heatmap = [[0 for x in range(level_breedte)] for y in range(level_hoogte)]
       #Level wordt gekopieerd (stond in str, nu in array)
       for y in range(level_hoogte):
              for x in range(level_breedte):
                     heatmap[y][x] = level[y][x]
                     
       #for i in heatmap:
              #print(i)
       #print('\n')
       
       #Alle snakes krijgen waarde van muur
       #TO DO: laten schalen met lengte
       for i in range(len(snakes)):
              for segment in snakes[i].segments:
                     heatmap[segment[1]][segment[0]] = wall_value
       
       #Alle muren gaan we waarde geven, rest wordt 0.              
       for y in range(level_hoogte):
              for x in range(level_breedte):
                     if heatmap[y][x] == '#' or type(heatmap[y][x]) == int:
                            heatmap[y][x] = wall_value
                     else: 
                            heatmap[y][x] = 0
       #print(mapFood())
                            
       #for i in heatmap:
              #print(i)
       
       #We geven de warmte van de heatmap mee
       #We laten de warmte uitvloeien
       counter = 0
       max_counter = 4
       while counter <= max_counter:
              datamap = deepcopy(heatmap)
              
              for y in range(level_hoogte):
                     for x in range(level_breedte):
                            value = 0
                            if datamap[y][x] == 4:
                                   continue
                            if heatmap[y][x] in [wall_value, '#']:
                                   heatmap[y][x] = wall_value
                            else:
                                   for coordinate in neighbours((x,y)):
                                          value += datamap[coordinate[1]][coordinate[0]]
                                   value /= 4
                                   heatmap[y][x] = int(value)

              #for i in heatmap:
                     #print(i)
              #print('\n')
              counter += 1
       return(heatmap)
       
def calculateLimit(heatmap):
       totalSum = 0 
       counter = 0
       for y in range(level_hoogte):
              for x in range(level_breedte):
                     if heatmap[y][x] == 1000:
                            continue
                     else:
                            totalSum += heatmap[y][x]
                            counter += 1
       average = totalSum / counter
       return((3*wall_value + average)/4)
       
#for i in mapHeat():
#       print(i)

heatmap = mapHeat()
foodmap = mapFood()
#print("Limiet =", calculateLimit(heatmap))
#for i in heatmap:
       #print(i)
#print('\n')
#print(foodmap)

foodheat = {}
paths = PriorityQueue()
#temp = []
for (food, distance) in foodmap:
       path = givePath(snakes[speler_nummer].head, food)
       foodheat[food] = heatmap[food[1]][food[0]]
       if foodheat[food] < calculateLimit(heatmap):
              paths.put((len(path), path))
              #temp.append((path[-1], len(path)))
#print("foodheat =", foodheat)
#print("paths =", temp)

if not paths.empty():
       path = paths.get()[1]
       #print("Path = ", path)
       direction = giveDirection(path[0], path[1])

print(direction)