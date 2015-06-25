#!/bin/python
from queue import PriorityQueue
import random
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

    head = (positie[0],positie[1])
    
    
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
            neighbours = [((current[0] + dx[i])%level_breedte, (current[1] + dy[i])%level_hoogte) for i in range(4)]
            for node in neighbours:
                
                new_cost = cost[current] + 1
                testBool = (node not in came_from or new_cost < cost[node]) and not isWall(node) 
                if testBool:
                    if isFood(node):
                        foodlist[node] = new_cost
                    came_from[node] = current
                    cost[node] = new_cost
                    frontier.put(node, new_cost)
        #print(foodlist)
        minimum = 10**6
        close_food = (start[0],start[1]+1)
        for node in foodlist:
            if foodlist[node] < minimum:
                close_food = node
                minimum = foodlist[node]
        return [came_from, cost, close_food]
    
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
    
    #print(givePath(closest_food))    

    #log = open('logs/test' + str(speler_nummer) + '.txt', 'w')

    while True:
        #for y in range(level_hoogte):
            #print("".join(level[y]))
        moves = givePath(closest_food)[1]
        #log.write("test")
        #log.write(str(moves) + '\n')
        
        direction = ""
        
        if head[0] == moves[0]:
            if head[1] == (moves[1] - 1):
                direction = "r"
            else:
                direction = "l"
        elif head[0] == (moves[0] - 1):
            direction = "u"
        else:
            direction = "d"
    
        if moves == "ERROR":
            direction = 'r'                           #Waarde tussen 0 en 3
        
        #print(direction)
        
        #log.write(str(i) + "\n")
        #log.write(richting[i] + "\n")
        
        i = 0
        positie[0] = (positie[0] + dx[i]) % level_breedte             #Verander de huidige positie
        positie[1] = (positie[1] + dy[i]) % level_hoogte
    
        snake.append(positie)                               #Nieuwe positie toevoegen aan snake
        if level[positie[1]][positie[0]] != 'x':            #Als nieuwe positie is niet 'x'
            staart = snake.pop(0)                           #Dan staart verwijderen
            level[staart[1]][staart[0]] = '.'
       
        for pos_x, pos_y in snake:
            level[pos_y][pos_x] = str(speler_nummer)
    
        print('move')                   #Geef door dat we gaan bewegen
        print(direction)                 #Geef de richting door
    
        line = input()                  #Lees nieuwe informatie
    
        if line == "quit":              #We krijgen dit door als het spel is afgelopen
            print("bye")                #Geef door dat we dit begrepen hebben
            break
    
        speler_bewegingen = line        #String met bewegingen van alle spelers
                                        #Nu is speler_bewegingen[i] de richting waarin speler i beweegt
        regel = input()
        while len(regel) == 0:
            regel = input()
        aantal_voedsel = int(regel)   #Lees aantal nieuw voedsel en posities
        voedsel_posities = []
        for i in range(aantal_voedsel):
            voedsel_positie = [int(s) for s in input().split()]
            # Sla de voedsel positie op in een lijst en in het level
            voedsel_posities.append(voedsel_positie)
            level[voedsel_positie[1]][voedsel_positie[0]] = "x"
    
    #log.close()


if __name__ == "__main__":
    run_ai()