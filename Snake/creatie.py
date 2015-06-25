#!/bin/python
import random
from snake import Snake
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

# We beginnen op de volgende positie:
positie = begin_posities[speler_nummer]

# u=up, d=down, l=left, r=right
# dx en dy geven aan in welke richting 'u', 'r', 'd' en 'l' zijn:
dx = [ 0, 1, 0,-1]
dy = [-1, 0, 1, 0]

richting = 'urdl'

def run_ai():
    snake = [positie]

    log = open('logs/test' + str(speler_nummer) + '.txt', 'w')

    while True:
        for y in range(level_hoogte):
            print("".join(level[y]))
        moves = possible_moves(positie[0],positie[1])
        log.write("test")
        log.write(str(moves) + '\n')
    
        if len(moves) == 0:
            i = 1                           #Waarde tussen 0 en 3
        else:
            i = moves[random.randrange(len(moves))]
        
        log.write(str(i) + "\n")
        log.write(richting[i] + "\n")
        
        positie[0] = (positie[0] + dx[i]) % level_breedte             #Verander de huidige positie
        positie[1] = (positie[1] + dy[i]) % level_hoogte
    
        snake.append(positie)                               #Nieuwe positie toevoegen aan snake
        if level[positie[1]][positie[0]] != 'x':            #Als nieuwe positie is niet 'x'
            staart = snake.pop(0)                           #Dan staart verwijderen
            level[staart[1]][staart[0]] = '.'
       
        for pos_x, pos_y in snake:
            level[pos_y][pos_x] = str(speler_nummer)
    
        print('move')                   #Geef door dat we gaan bewegen
        print(richting[i])                 #Geef de richting door
    
        line = input()                  #Lees nieuwe informatie
    
        if line == "quit":              #We krijgen dit door als het spel is afgelopen
            print("bye")                #Geef door dat we dit begrepen hebben
            break
    
        speler_bewegingen = line        #String met bewegingen van alle spelers
                                        #Nu is speler_bewegingen[i] de richting waarin speler i beweegt
    
        aantal_voedsel = int(input())   #Lees aantal nieuw voedsel en posities
        voedsel_posities = []
        for i in range(aantal_voedsel):
            voedsel_positie = [int(s) for s in input().split()]
            # Sla de voedsel positie op in een lijst en in het level
            voedsel_posities.append(voedsel_positie)
            level[voedsel_positie[1]][voedsel_positie[0]] = "x"
    
    log.close()


def possible_moves(x, y):
    # u=up, d=down, l=left, r=right
    # dx en dy geven aan in welke richting 'u', 'r', 'd' en 'l' zijn:
    #dx = [ 0, 1, 0,-1]
    #dy = [-1, 0, 1, 0]
    
    #richting = 'urdl'
    valide_richting_leeg = []
    valide_richting_snoep = []
    
    for i in range(0,4):
        x_new = (x + dx[i]) % level_breedte             #Verander de huidige positie
        y_new = (y + dy[i]) % level_hoogte
        if level[y_new][x_new] == '.':
            valide_richting_leeg.append(i)
        elif level[y_new][x_new] == 'x':
            valide_richting_snoep.append(i)
    if len(valide_richting_snoep) == 0:
        return(valide_richting_leeg)
    else:
        return(valide_richting_snoep)

if __name__ == "__main__":
    run_ai()