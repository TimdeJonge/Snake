from snake import Snake
from random import shuffle

dx = [ 0, 1, 0,-1, 0]
dy = [-1, 0, 1, 0, 0]
class Map(object):
    def __init__(self, level = [], level_hoogte = 0, level_breedte = 0, snakes =[], speler_nummer = 0, aantal_spelers = 1, aantal_voedsel = 0, voedsel_posities = []):
        output = []
        for row in level:
            output.append([])
            for element in row:
                output[-1].append(element)
        self.level = output
        self.level_hoogte = level_hoogte
        self.level_breedte = level_breedte
        self.snakes = snakes
        self.speler_nummer = speler_nummer
        self.aantal_spelers = aantal_spelers
        self.aantal_voedsel = aantal_voedsel
        self.voedsel_posities = voedsel_posities
        wall_value = 1000
    
    def __str__(self):
        output = ''
        for y in self.level:
            temp = ''
            for x in y: 
                temp += str(x) + '\t'
            output += temp + '\n' 
        return str(output)
        
    def isWall(self, node):
        if self.level[node[1]][node[0]] in ['0', '1', '2', '3', '4', '5' ,'6', '7', '#']:
            return True
        return False
        
           #Lijst maken van alle buurvakjes
    def neighbours(self, coordinate):
        neighbourList = []
        indexList = [0,1,2,3]
        shuffle(indexList)
        for i in indexList:
            neighbourList.append(((coordinate[0] + dx[i]) % self.level_breedte, (coordinate[1] + dy[i]) % self.level_hoogte))
        return neighbourList
    
    def giveDirection(self, start, goal):
       if start[0] == goal[0]:
              if start[1] == (goal[1] + 1) % self.level_hoogte:
                     direction = 'u'
              else:
                     direction = 'd'
       elif start[0] == (goal[0] + 1) % self.level_breedte:
              direction = 'l'
       else:
              direction = 'r'
       return(direction)
       

       
#level = Map(['0###.',
#       '####x',                                                                     
#       '#.2..',
#       '.#1x#',
#       '.#..#',
#       'x#..#'], 6, 5, [Snake([(0,0)]), Snake([(2,3)]), Snake([(2,2)])], 0, 3, 3, [(4,1), (3,3), (0,5)]) 
