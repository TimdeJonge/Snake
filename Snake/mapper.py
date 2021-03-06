from level import Map
from snake import Snake
from queue import PriorityQueue
from copy import deepcopy 
dx = [ 0, 1, 0,-1, 0]
dy = [-1, 0, 1, 0, 0]
wall_value = 1000

#========= mapLevel() =============
    #Door middel van BFS wordt het hele bereikbare level een waarde toegekend. 
    #Onbereikbare elementen krijgen geen waarde, dit wordt later afgehandeld.
    #Output bestaat uit 2 dictionaries:
    #De eerste bevat de cost om naar ieder punt te gaan
    #De tweede bevat het afgelopen punt om te doorlopen.

def mapLevel(level, start):
    cost = {}
    came_from = {}
    frontier = PriorityQueue()
    frontier.put((0,start))

    cost[start] = 0
    came_from[start] = None
    while(not frontier.empty()):
        current = frontier.get()[1]
        neighbourList = level.neighbours(current)

        for node in neighbourList:
            new_cost = cost[current] + 1                                # Hier wordt de cost van iedere stap aangenomen als 1. Mogelijk wordt dit op enig punt veranderd.
            testBool = (node not in came_from or new_cost < cost[node]) and not level.isWall(node) 
            if testBool:
                came_from[node] = current
                cost[node] = new_cost
                frontier.put((new_cost,node))
    return([cost, came_from])

#TESTCODE

#print("MAPLEVEL OUTPUT")
#temp = mapLevel(level, level.snakes[0].head)
#lengthMap, arrowMap = temp[0], temp[1]
#print(level)
#tempQueue = PriorityQueue()
#for i in lengthMap:
#    tempQueue.put((lengthMap[i], i))
#while not tempQueue.empty():
#    temp = tempQueue.get()
#    level.level[temp[1][1]][temp[1][0]] = temp[0]
#print(level)
#print("EINDE MAPLEVEL")

#========== mapFood() ==============
    #mapFood gebruikt alleen de variabelen die uit player.py zouden komen.
    #Eerst bepaalt hij voor alle food de afstanden voor alle spelers tot dat voedsel
    #Daarna bepaalt hij wie het dichtst bij is, en hoeveel dichter bij die is dan de tweede.
    #Output is een lijst van lijsten met 
    #Eerste argument: afstand tot een stuk voedsel waar wij het dichtst bij zijn
    #Tweede arugment: bijbehorend stuk voedsel
def mapFood(level):
    foodDistance = {}
    close_food = []
    
    for food in level.voedsel_posities:
        foodDistance[food] = []                 
    for i in range(level.aantal_spelers):
        head = level.snakes[i].head
        temp = mapLevel(level, head)
        lengthMap = temp[0]
        
        for food in level.voedsel_posities:           #Mocht voedsel bereikbaar zijn, wordt de afstand van speler naar voedsel
                                                #gegeven door foodDistance[voedsel_positie][speler_nummer].
                                                #Mocht het niet bereikbaar zijn, levert dit -1.
            if food in lengthMap:
                foodDistance[food].append(lengthMap[food])  
            else:
                foodDistance[food].append(-1)           #Hier het beloofde 
    print("foodDistance =", foodDistance)
    for food in foodDistance:
        minimum = 10**6             #Waarde hoog gekozen zodat er duidelijk verschil is tussen het geval
        next_best = 10**6           #waar er 2 personen bij kunnen en waar er 1 persoon bij kan
        closest_player = (level.speler_nummer + 1) % level.aantal_spelers       #Default: Als niemand er bij kan, doe alsof iemand anders het dichtst bij is 
        
        for i in range(level.aantal_spelers):       #er is hier ook een oplossing mogelijk met de min() functie, maar deze leek me duidelijker
            distance = foodDistance[food][i]
            if distance == -1:                   
                continue
            elif distance > minimum:
                if distance < next_best:            #TODO: Use snake.score() to also run to sweets where you'll get first
                    next_best = distance
            else: 
                next_best = minimum
                minimum = distance
                closest_player = i
        if closest_player == level.speler_nummer:
            if level.aantal_spelers == 1:
                if minimum != 10**6:
                    close_food.append([minimum, food])
            if next_best - minimum < 2000 or level.snakes[level.speler_nummer + 1 % level.aantal_spelers].score > level.snakes[level.speler_nummer].score + 1000:
                close_food.append([minimum, food])
    #TESTCODE
    
    print("MAPFOOD OUTPUT")   
    printlevel = deepcopy(level)
    for i in close_food:
        print(i)
        printlevel.level[i[1][1]][i[1][0]] = i[0]
    print(printlevel)
    print("EINDE MAPFOOD")
    
    
    return(close_food)


def mapHeat(level):
    #Zorgen dat level aanpasbaar is (alles wordt 0)
    heatmap = deepcopy(level)
                 
    #Alle snakes krijgen waarde van muur
    #TO DO: laten schalen met lengte
    for i in range(len(heatmap.snakes)):
          for segment in heatmap.snakes[i].segments:
                 heatmap.level[segment[1]][segment[0]] = wall_value
   
    #Alle muren gaan we waarde geven, rest wordt 0.              
    for y in range(heatmap.level_hoogte):
          for x in range(heatmap.level_breedte):
                 if heatmap.level[y][x] == '#' or type(heatmap.level[y][x]) == int:
                        heatmap.level[y][x] = wall_value
                 else: 
                        heatmap.level[y][x] = 0
   
    #We geven de warmte van de heatmap mee
    #We laten de warmte uitvloeien
    counter = 0
    max_counter = 4          #Arbitrair, maar voor het moment een goede balans
    while counter <= max_counter:
        datamap = deepcopy(heatmap)
          
        for y in range(heatmap.level_hoogte):
             for x in range(heatmap.level_breedte):
                    value = 0
                    if datamap.level[y][x] == 4:
                        continue
                    if heatmap.level[y][x] in [wall_value, '#']:
                           heatmap.level[y][x] = wall_value
                    else:
                        for coordinate in heatmap.neighbours((x,y)):
                            value += datamap.level[coordinate[1]][coordinate[0]]
                        value /= 4
                        heatmap.level[y][x] = int(value)
        counter += 1
    return(heatmap)

def calculateLimit(heatmap):
       totalSum = 0 
       counter = 0
       for y in range(heatmap.level_hoogte):
              for x in range(heatmap.level_breedte):
                     if heatmap.level[y][x] == wall_value:
                            continue
                     else:
                            totalSum += heatmap.level[y][x]
                            counter += 1
       average = totalSum / counter
      
       #TESTCODE 
       
       #print(heatmap)
       #print(average)
       #print((3*wall_value + average) / 4)
       
       return((3*wall_value + average)/4)

def givePath(level, start, goal):
    
    temp = mapLevel(level, start)
    lengthMap = temp[0]
    arrowMap = temp[1]
        
    current = goal
    path = [current]
    while lengthMap[current] != 0: 
        current = arrowMap[current]
        path.append(current)
    path.reverse()
    
    #print(path)
    return path
#print(level)
#print(givePath(level, level.snakes[0].head, level.snakes[1].head))