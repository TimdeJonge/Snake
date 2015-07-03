from copy import deepcopy
from snake import Snake

dx = [ 0, 1, 0,-1, 0]
dy = [-1, 0, 1, 0, 0]


level = ['..................................................',
'.#################################################',  
'.............................xxxxx................',
'###########################.#####################.',
'....................#x..x........................x',
'###########################.#####################.', 
'............x.....................................',
'###########################.#####################.', 
'.................................#.##.............',
'.##########################.######################',
'..0...............................................',
'#################################################.']
level_hoogte = 12
level_breedte = 50
snakes = [Snake([(2,10)])]
speler_nummer = 0 
aantal_spelers = 1
aantal_voedsel = 5
voedsel_posities = [(29,2), (32,2), (21,4), (49,4), (12,6)]


clustermap = [[] for i in range(level_hoogte)]

       #Lijst maken van alle buurvakjes
def neighbours(coordinate):
       neighbourList = []
       for i in range(4):
              neighbourList.append(((coordinate[0] + dx[i]) % level_breedte, (coordinate[1] + dy[i]) % level_hoogte))
       return neighbourList

def mapAllFood():
    
    for y in range(level_hoogte):
        for x in level[y]:
            if x in ['0', '1', '2', '3', '4', '5', '6' '7', '#']:
                clustermap[y].append(0)
            elif x == 'x':
                clustermap[y].append(1000)
            else:
                clustermap[y].append(100)
    counter = 0 
    while counter <= 5:
        clusterdata = deepcopy(clustermap)
        for y in range(level_hoogte):
            for x in range(level_breedte):
                if clustermap[y][x] == 0:
                    continue
                total = clusterdata[y][x]
                freeSquares = 1
                for (a,b) in neighbours((x,y)):
                    if clusterdata[b][a] == 0:
                        pass
                    else:
                        total += clusterdata[b][a]
                        freeSquares += 1
                if freeSquares == 1:
                    clustermap[y][x] = 0
                else:
                    clustermap[y][x] = total / freeSquares
        counter += 1
mapAllFood()  

for i in clustermap:
    print(i)
