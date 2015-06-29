import time
from queue import PriorityQueue
from snake import Snake

        #Het onderstaande is een simulatie van echte data zoals die binnen zou kunnen komen.
        #Dit zijn alle variabelen die we uit player.py nodig zullen hebben.
        #Het is ook alles wat we binnen dit bestand zullen gebruiken.
        #In dit bestand zijn coordinaten in de vorm (x,y).

dx = [0,  1, 0, -1]
dy = [-1, 0, 1,  0]
    
level=['0##..',
       '###.x',                                                                     
       '#.2..',
       '.#1x#',
       '.#..#',
       'x#..#']
level_hoogte = 6
level_breedte = 5
snakes = [Snake([(0,0)]), Snake([(2,3)]), Snake([(2,2)])]  
speler_nummer = 0
aantal_spelers = 3
aantal_voedsel = 3
voedsel_posities = [(4,1), (3,3), (0,5)]

        #map_start is toegevoegd om het testen van giveDistance en givePath mogelijk te maken.
        #TODO: Werk map_start weg op een efficiente manier.

map_start = snakes[0].head
    
        #Er kunnen maximaal 8 spelers zijn. 
        #Hierdoor hoeven we alleen deze lijst te checken om te kijken of een vakje begaanbaar is.
def isWall(node):
    if level[node[1]][node[0]] in ['0', '1', '2', '3', '4', '5' ,'6', '7', '#']:
        return True
    return False

def isFood(node):
    if level[node[1]][node[0]] == 'x':
        return True
    return False


        #mapLevel gebruikt variabele level om deze in kaart te brengen.
        #als output geeft hij een lijst van 2 dicts.
        #De eerste dict bevat voor elk bereikbaar vakje de cost om er te komen.
        #In de huidige code is de cost precies gelijk aan het aantal vakjes.
        #De tweede dict bevat voor elk bereikbaar vakje het afgelopen vakj wat gebruikt is om daar te komen.

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
        neighbours = [((current[0] + dx[i])%level_breedte, (current[1] + dy[i])%level_hoogte) for i in range(4)]           #

        for node in neighbours:
            new_cost = cost[current] + 1                                # Hier wordt de cost van iedere stap aangenomen als 1. Mogelijk wordt dit op enig punt veranderd.
            testBool = (node not in came_from or new_cost < cost[node]) and not isWall(node) 
            if testBool:
                came_from[node] = current
                cost[node] = new_cost
                frontier.put((new_cost,node))
    return([cost, came_from])

def givePath(goal):
    
    temp = mapLevel(map_start)
    lengthMap = temp[0]
    arrowMap = temp[1]
    
    current = goal
    path = [current]
    while lengthMap[current] != 0: 
        current = arrowMap[current]
        path.append(current)
    path.reverse()
    return path
    #Voor giveDistance wordt nu de hele map gescand om 1 afstand te bepalen.
    #Dit is inefficienter dan bijvoorbeeld A*.
    #Eigenlijk is het plan niet giveDistance nog te gebruiken, de functie
    #was vooral heel handig om mee te testen. 
def giveDistance(goal):

    return mapLevel(map_start)[0][goal]

def mapFood():

    foodDistance = {}
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
    return foodDistance

#print(mapFood())


source = 'http://www.redblobgames.com/pathfinding/a-star/introduction.html'