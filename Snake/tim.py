#!/bin/python
import random
from queue import PriorityQueue
###Initialisatie
# We lezen het doolhof en beginposities in

level_hoogte = int(input())         #Lees hoe groot het level is
level_breedte = int(input())

level = []                          #Lees het level regel voor regel
for y in range(level_hoogte):
    level.append(list(input()))

aantal_spelers = int(input())       #Lees het aantal spelers en hun posities
begin_posities = []
for i in range(aantal_spelers):
    begin_positie = [int(s) for s in input().split()]   #Maak lijst met x en y
    begin_posities.append(begin_positie)      #Voeg dit coordinaat toe aan begin_posities

speler_nummer = int(input())        #Lees welk spelernummer wij zijn

def isWall(node):
    if level[node[1]][node[0]] == '#':
        return True
    return False

#Breadth First Search. Gegeven een punt start maakt het een Queue en twee dicts aan. 
#Uit de Queue haalt de functie elke keer het punt met de laagste afstand dat nog niet behandeld is.
#Hiervan zoekt het de buren, bekijkt of we deze al behandeld hebben, en voegt deze toe aan de Queue.
#Output is twee dicts, een om het pad te vormen (arrowMap, wordt gebruikt in givePath)
#En 

def mapLevel(start):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    cost = {}
    came_from = {}
    cost[start] = 0
    came_from[start] = None
    i = 0 
    while(not frontier.empty()):
        current = frontier.get()
        #print(current, level[current[1]][current[0]])
        
        neighbours = [((current[0] + dx[i])%10, (current[1] + dy[i])%10) for i in range(4)]
        for node in neighbours:
            new_cost = cost[current] + 1
            testBool = (node not in came_from or new_cost < cost[node]) and not isWall(node) 
            if testBool:
                came_from[node] = current
                cost[node] = cost[current] + 1
                frontier.put(node, cost[node])

        i+=1
    return [came_from, cost]
###De tijdstap

# We beginnen op de volgende positie:
positie = begin_posities[speler_nummer]

# u=up, d=down, l=left, r=right
# dx en dy geven aan in welke richting 'u', 'r', 'd' en 'l' zijn:
dx = [ 0, 1, 0,-1]
dy = [-1, 0, 1, 0]

while True:
    i = random.randrange(4)         #Kies een random richting
    richting = 'urdl'[i]            #u=up, d=down, l=left, r=right
    positie[0] += dx[i]             #Verander de huidige positie
    positie[1] += dy[i]
                                    #Let op periodieke randvoorwaarden!
    positie[0] = (positie[0] + level_breedte)% level_breedte
    positie[1] = (positie[1] + level_hoogte) % level_hoogte

    print('move')                   #Geef door dat we gaan bewegen
    print(richting)                 #Geef de richting door

    line = input()                  #Lees nieuwe informatie

    if line == "quit":              #We krijgen dit door als het spel is afgelopen
        print("bye")                #Geef door dat we dit begrepen hebben
        break

    speler_bewegingen = line        #String met bewegingen van alle spelers
                                    #Nu is speler_bewegingen[i] de richting waarin speler i beweegd

    aantal_voedsel = int(input())   #Lees aantal nieuw voedsel en posities
    voedsel_posities = []
    for i in range(aantal_voedsel):
        voedsel_positie = [int(s) for s in input().split()]
        # Sla de voedsel positie op in een lijst en in het level
        voedsel_posities.append(voedsel_positie)
        level[voedsel_positie[1]][voedsel_positie[0]] = "x"

