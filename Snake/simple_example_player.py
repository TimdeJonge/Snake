#!/bin/python
import random
from copy import copy
from snake import Snake
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
###De tijdstap
snakes = [Snake([begin_posities[i]]) for i in range(aantal_spelers)]

# We beginnen op de volgende positie:
positie = begin_posities[speler_nummer]

# u=up, d=down, l=left, r=right
# dx en dy geven aan in welke richting 'u', 'r', 'd' en 'l' zijn:
dx = [ 0, 1, 0,-1, 0]
dy = [-1, 0, 1, 0, 0]

while True:
    moves_empty = []
    moves_candy = []
    for i in range(4):
        x_new = (snakes[speler_nummer].segments[-1][0] + dx[i]) % level_breedte
        y_new = (snakes[speler_nummer].segments[-1][1] + dy[i]) % level_hoogte
        print("Nu onderzoeken we in vorm (x,y) het coordinaat (" + str(x_new) + ", " + str(y_new) + ")")
        print("We vinden " + level[y_new][x_new])
        if level[y_new][x_new] == '.':
            moves_empty.append('urdl'[i])
            print(moves_empty)
        elif level[y_new][x_new] == 'x':
            moves_candy.append('urdl'[i])
    if len(moves_candy) != 0: 
        direction = random.choice(moves_candy)
    elif len(moves_empty) != 0: 
        direction = random.choice(moves_empty)
    else: 
        direction = 'r'
        print("Goodbye, cruel world")

    print('move')                   #Geef door dat we gaan bewegen
    print(direction)                 #Geef de richting door

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
        coordinate = ((snakes[j].segments[-1][0] + dx[i]) % level_breedte, (snakes[j].segments[-1][1] + dy[i]) % level_hoogte)
        snakes[j].move(coordinate, level[coordinate[1]][coordinate[0]])
    
    #TO DO: volgorde bepalen.
        
    for i in range(len(snakes)):
       coordinate = snakes[i].segments[-1]
       if level[coordinate[1]][coordinate[0]] == '.':
           coordinate2 = snakes[i].last_segment
           level[coordinate2[1]][coordinate2[0]] = '.'
       
       level[coordinate[1]][coordinate[0]] = str(i)



    aantal_voedsel = int(input())   #Lees aantal nieuw voedsel en posities
    if aantal_voedsel == 0:
        input()
    voedsel_posities = []
    for i in range(aantal_voedsel):
        voedsel_positie = [int(s) for s in input().split()]
        # Sla de voedsel positie op in een lijst en in het level
        voedsel_posities.append(voedsel_positie)
        level[voedsel_positie[1]][voedsel_positie[0]] = "x"

