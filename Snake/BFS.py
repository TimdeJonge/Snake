import time
from queue import PriorityQueue
from snake import Snake

        #Het onderstaande is een simulatie van echte data zoals die binnen zou kunnen komen.
        #Dit zijn alle variabelen die we uit player.py nodig zullen hebben.
        #Het is ook alles wat we binnen dit bestand zullen gebruiken.
        #In dit bestand zijn coordinaten in de vorm (x,y).

dx = [0,  1, 0, -1]
dy = [-1, 0, 1,  0]
    
level = ['###.....##.#.....#.#.##...#..#...#..#.#.',
'....#..#...#...........###...###.#..#...',
'##.#...x#.#..##.#.#.##...#.....#...#..#.',
'.#.#..##..#..........#.#..##.#.#..###.0.',
'.#..#..##.###.#.#.#..#.#.#...##.#.......',
'..#..#.#.#....#.#.#..#.............#...#',
'##.#..#...#.#.#....#.#.#.#.#.###.#....#.',
'#..#..x#....#.###...#...##2.....#..#....',
'#....##.........#...#..#.....#.....#.#..',
'#.......#...#.#...#..#.#.....#.#.#......',
'#.#...##.##....#..##..#..#..#.....##.#..',
'..##.....#..3#....#.......##.####.....#.',
'##...#.#.#.#.#....#...#.#.#.....#...#.#.',
'#.##.#...#.#..####..##..#.1.#...#.#..##.',
'.....#.#.....#.....#..#.#..#....#.#.#...']

level_hoogte = 15
level_breedte = 40
snakes = [Snake([(38,3)]), Snake([(26,13)]), Snake([(26,7)]), Snake([(12,11)])]
speler_nummer = 0
aantal_spelers = 4
aantal_voedsel = 2
voedsel_posities = [(2,7), (7,6)]

        #map_start is toegevoegd om het testen van giveDistance en givePath mogelijk te maken.
        #TODO: Werk map_start weg op een efficiente manier.

map_start = snakes[0].head

        #Lijst maken van alle buurvakjes
def neighbours(coordinate):
       neighbourList = []
       for i in range(4):
              neighbourList.append(((coordinate[0] + dx[i]) % level_breedte, (coordinate[1] + dy[i]) % level_hoogte))
       return neighbourList
       
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
        neighbourList = neighbours(current)

        for node in neighbourList:
            new_cost = cost[current] + 1                                # Hier wordt de cost van iedere stap aangenomen als 1. Mogelijk wordt dit op enig punt veranderd.
            testBool = (node not in came_from or new_cost < cost[node]) and not isWall(node) 
            if testBool:
                came_from[node] = current
                cost[node] = new_cost
                frontier.put((new_cost,node))
    return([cost, came_from])

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
        #Voor giveDistance wordt nu de hele map gescand om 1 afstand te bepalen.
        #Dit is inefficienter dan bijvoorbeeld A*.
        #Eigenlijk is het plan niet giveDistance nog te gebruiken, de functie
        #was vooral heel handig om mee te testen. 
def giveDistance(goal):

    return mapLevel(map_start)[0][goal]
            
            #mapFood gebruikt alleen de variabelen die uit player.py zouden komen.
            #Eerst bepaalt hij voor alle food de afstanden voor alle spelers tot dat voedsel
            #Daarna bepaalt hij wie het dichtst bij is, en hoeveel dichter bij die is dan de tweede.
            #Output is een lijst van lijsten met 
            #Eerste argument: coordinaat van voedsel waar wij het dichtst bij zijn
            #Tweede arugment: Verschil in afstanden
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

#print(mapFood())


source = 'http://www.redblobgames.com/pathfinding/a-star/introduction.html'