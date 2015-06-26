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
#for i in range(len(snakes)):
#    print("Snake nummer " + str(i) + " is op positie" + str(snakes[i]) + " VOOR DE GAME") 
# We beginnen op de volgende positie:
positie = copy(begin_posities[speler_nummer])

# u=up, d=down, l=left, r=right
# dx en dy geven aan in welke richting 'u', 'r', 'd' en 'l' zijn:
dx = [ 0, 1, 0,-1, 0]
dy = [-1, 0, 1, 0, 0]

#i = 'urdl'.index(coordinate)
#coordinate = ((self.segments[-1][0] + dy[i]) % level_hoogte, (self.segments[-1][1] + dx[i]) % level_breedte)



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
    
                                    #Bekijkt richting die ingegeven wordt
                                    #Bepaalt nieuwe coördinaat in volgorde (x,y)
                                    #Beweegt naar nieuwe punt
    for j in range(len(snakes)):
        i = 'urdlx'.index(speler_bewegingen[j])
        #print("Slang nummer " + str(j) + " bevindt zich nu op " + str(snakes[j]) + " VOOR DE ZET")
        coordinate = ((snakes[j].segments[-1][0] + dx[i]) % level_breedte, (snakes[j].segments[-1][1] + dy[i]) % level_hoogte)
        snakes[j].move(coordinate, level[coordinate[1]][coordinate[0]])
        
   
    
    #for j in range(len(snakes)):
        #print("Slang nummer " + str(j) + " bevindt zich nu op " + str(snakes[j]) + " NA DE ZET")
    aantal_voedsel = int(input())   #Lees aantal nieuw voedsel en posities
    if aantal_voedsel == 0:
        input()
    voedsel_posities = []
    for i in range(aantal_voedsel):
        voedsel_positie = [int(s) for s in input().split()]
        # Sla de voedsel positie op in een lijst en in het level
        voedsel_posities.append(voedsel_positie)
        level[voedsel_positie[1]][voedsel_positie[0]] = "x"

