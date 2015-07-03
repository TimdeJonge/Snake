#!/bin/python
import random
import time
from snake import Snake
from queue import PriorityQueue
from copy import deepcopy
#from Heatmap import mapHeat
###Initialisatie
# We lezen het doolhof en beginposities in

level_hoogte = int(input())         #Lees hoe groot het level is
level_breedte = int(input())
voedsel_posities = []
level = []                          #Lees het level regel voor regel
for y in range(level_hoogte):
    level.append(list(input()))

aantal_spelers = int(input())       #Lees het aantal spelers en hun posities
begin_posities = []
for i in range(aantal_spelers):
    begin_positie = [int(s) for s in input().split()]   #Maak lijst met x en y
    begin_posities.append(begin_positie)      #Voeg dit coordinaat toe aan begin_posities


speler_nummer = int(input())        #Lees welk spelernummer wij zijn
###De tijdstap
snakes = [Snake([(begin_posities[i][0], begin_posities[i][1])]) for i in range(aantal_spelers)]

# We beginnen op de volgende positie:
positie = begin_posities[speler_nummer]

# u=up, d=down, l=left, r=right
# dx en dy geven aan in welke richting 'u', 'r', 'd' en 'l' zijn:
dx = [ 0, 1, 0,-1, 0]
dy = [-1, 0, 1, 0, 0]


       #We kennen een waarde toe aan alle muren
       #Deze moet overgezet worden in het bestand waarin het gebruikt wordt.
wall_value = 1000
first_food = 0
            #Algemene flow van het programma zoals het nu gevormd is: 
            #1: mapLevel(). Vanaf het hoofd van onze slang worden de afstanden naar alle vakjes en bijbehorende paden berekend.
            #2: mapFood(). Eerst wordt een lijst gecre\"eerd van alle hoofden naar al het voedsel,
            #   daarna wordt uit die lijsten gekeken waar wij het dichtst bij zijn. 
            #   Return is de locaties van voedsel waar wij het dichtst bij zijn, en hoe veel verder de eerstvolgende is.
            #3: mapHeat(). We cre\"eren een heatmap waarin de muren en slangen allemaal bronnen zijn.
            #   Op deze wijze is het voordelig om naar een koud gebied te zijn, hier is immers het minste in de buurt. 
            #4: giveConclusion(). Gebruikmakend van voorgaande data trekken we onze conclusie over welk vakje we willen bezoeken.

#======== HULPFUNCTIE'S VOOR mapLevel() =============

        #Er kunnen maximaal 8 spelers zijn. 
        #Hierdoor hoeven we alleen deze lijst te checken om te kijken of een vakje begaanbaar is.
def isWall(node):
    if level[node[1]][node[0]] in ['0', '1', '2', '3', '4', '5' ,'6', '7', '#']:
        return True
    return False

    #Volgens mij doen we hier niets mee...
def isFood(node):
    if level[node[1]][node[0]] == 'x':
        return True
    return False

       #Lijst maken van alle buurvakjes
def neighbours(coordinate):
       neighbourList = []
       for i in range(4):
              neighbourList.append(((coordinate[0] + dx[i]) % level_breedte, (coordinate[1] + dy[i]) % level_hoogte))
       return neighbourList

#========= mapLevel() =============
        #Door middel van BFS wordt het hele bereikbare level een waarde toegekend. 
        #Onbereikbare elementen krijgen geen waarde, dit wordt later afgehandeld.
        #Output bestaat uit 2 dictionaries:
        #De eerste bevat de cost om naar ieder punt te gaan
        #De tweede bevat het afgelopen punt om te doorlopen.
    
def mapLevel(start):
    cost = {}
    came_from = {}
    frontier = PriorityQueue()
    frontier.put((0,start))

    cost[start] = 0
    came_from[start] = None
    while(not frontier.empty()):
        current = frontier.get()[1]
        neighbourList = neighbours(current)

        for node in neighbourList:
            new_cost = cost[current] + 1                                # Hier wordt de cost van iedere stap aangenomen als 1. Mogelijk wordt dit op enig punt veranderd.
            testBool = (node not in came_from or new_cost < cost[node]) and not isWall(node) 
            if testBool:
                came_from[node] = current
                cost[node] = new_cost
                frontier.put((new_cost,node))
    return([cost, came_from])
#========== mapFood() ==============
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
                foodDistance[food].append(-1)           #Hier het beloofde 
    print("foodDistance =", foodDistance)
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
            if aantal_spelers == 1:
                if minimum != 10**6:
                    close_food.append([food, next_best - minimum])
            elif next_best - minimum < 2000:          #Als wij niet de enige zijn:
                close_food.append([food, next_best - minimum])
    return(close_food)
    
    

#============== mapHeat() =============

def mapHeat():
       #Zorgen dat level aanpasbaar is (alles wordt 0)
       heatmap = [[0 for x in range(level_breedte)] for y in range(level_hoogte)]
       #Level wordt gekopieerd (stond in str, nu in array)
       for y in range(level_hoogte):
              for x in range(level_breedte):
                     heatmap[y][x] = level[y][x]
                     
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
       
       #We geven de warmte van de heatmap mee
       #We laten de warmte uitvloeien
       counter = 0
       max_counter = 4          #Arbitrair, maar voor het moment een goede balans
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


              counter += 1
       return(heatmap)
       
#======== Hulpfuncties voor giveConclusion() ==============

def giveDirection(start, goal):
       if start[0] == goal[0]:
              if start[1] == (goal[1] + 1) % level_hoogte:
                     direction = 'u'
              else:
                     direction = 'd'
       elif start[0] == (goal[0] + 1) % level_breedte:
              direction = 'l'
       else:
              direction = 'r'
       return(direction)
       
def calculateLimit(heatmap):
       totalSum = 0 
       counter = 0
       for y in range(level_hoogte):
              for x in range(level_breedte):
                     if heatmap[y][x] == wall_value:
                            continue
                     else:
                            totalSum += heatmap[y][x]
                            counter += 1
       average = totalSum / counter
       return((wall_value + average)/2)

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

#========== giveConclusion() ================
        #TO DO: Creeer een default voor als er geen voedsel is dat voldoet
        #TO DO: Test het feit dat we in mapFood ook distance mee kunnen geven voor een beslissing
def giveConclusion():       
    foodmap = mapFood()
    #print("Foodmap =", foodmap)
    heatmap = mapHeat()
    foodheat = {}
    foods = PriorityQueue()
    limit = 960
    for (food, distance) in foodmap:
        foodheat[food] = heatmap[food[1]][food[0]]
        
        if foodheat[food] < limit:
                foods.put((distance, food))
                #print("Ik overweeg om te gaan naar ", food)
    print("Foodheat =", foodheat)
    #if len(snakes[speler_nummer].segments) == 1:
        #direction = firstConclusion(foodmap, heatmap, foods)
    if not foods.empty():
        good_food = foods.get()[1]
        print("Ik ga naar", good_food)
        path = givePath(snakes[speler_nummer].head, good_food)
        direction = giveDirection(path[0], path[1])
        print("en dus in richting", direction)
    else:
        minimum = wall_value
        direction = -1
        head = snakes[speler_nummer].head
        backuplist = []
        for coordinate in neighbours(head):
            if heatmap[coordinate[1]][coordinate[0]] < minimum:
                direction = giveDirection(head, coordinate)
                minimum = heatmap[coordinate[1]][coordinate[0]]
            elif level[coordinate[1]][coordinate[0]] in ['.','x']:
                backuplist.append(coordinate)
        if direction == -1:
                if len(backuplist)!= 0:
                    direction = giveDirection(head,backuplist[0])
                else:
                    print("Goodbye, cruel world!")
                    direction = 'r'
    return direction
    
teller = 0
while True:
    start = time.time()
    
    print("Ik ben nu op coordinaat", snakes[speler_nummer].head)
    direction = giveConclusion()
    
    print('move')                   #Geef door dat we gaan bewegen
    print(direction)                 #Geef de richting door
    
    teller += 1
    end = time.time()
    print("Deze zet duurde " + str(end - start) + " seconden.")
    print("Aantel voedsel =", len(voedsel_posities))
    print("Timestep ", teller)
    
    line = input()                  #Lees nieuwe informatie

    if line == "quit":              #We krijgen dit door als het spel is afgelopen
        print("bye")                #Geef door dat we dit begrepen hebben
        break
    

    
    speler_bewegingen = line        #String met bewegingen van alle spelers
                                    #Nu is speler_bewegingen[i] de richting waarin speler i beweegd
    
                                    #Bekijkt richting die ingegeven wordt
                                    #Bepaalt nieuwe coördinaat in volgorde (x,y)
                                    #Beweegt naar nieuwe punt
    for j in range(len(snakes)):
        i = 'urdlx'.index(speler_bewegingen[j])
        coordinate = ((snakes[j].head[0] + dx[i]) % level_breedte, (snakes[j].head[1] + dy[i]) % level_hoogte)
        if level[coordinate[1]][coordinate[0]] == 'x':
            voedsel_posities.remove(coordinate)
        snakes[j].move(coordinate, level[coordinate[1]][coordinate[0]])
        
    #TO DO: volgorde van de zetten bepalen (wanneer welke speler een zet mag doen)
    
    for i in range(len(snakes)):
       coordinate = snakes[i].segments[-1]
       if level[coordinate[1]][coordinate[0]] == '.':
           coordinate2 = snakes[i].last_segment
           level[coordinate2[1]][coordinate2[0]] = '.'
       
       level[coordinate[1]][coordinate[0]] = str(i)

    aantal_voedsel = int(input())   #Lees aantal nieuw voedsel en posities
    if aantal_voedsel == 0:
        input()
    for i in range(aantal_voedsel):
        voedsel_positie = [int(s) for s in input().split()]
        # Sla de voedsel positie op in een lijst en in het level
        voedsel_posities.append((voedsel_positie[0], voedsel_positie[1]))
        level[voedsel_positie[1]][voedsel_positie[0]] = "x"
    
