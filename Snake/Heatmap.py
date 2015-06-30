from snake import Snake
from copy import deepcopy
from BFS import mapFood
from BFS import givePath
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

       #We kennen een waarde toe aan alle muren
       #Deze moet overgezet worden in het bestand waarin het gebruikt wordt.
wall_value = 1000

       #Lijst maken van alle buurvakjes
def neighbours(coordinate):
       neighbourList = []
       for i in range(4):
              neighbourList.append(((coordinate[0] + dx[i]) % level_breedte, (coordinate[1] + dy[i]) % level_hoogte))
       return neighbourList

def mapHeat():
       #Zorgen dat level aanpasbaar is (alles wordt 0)
       heatmap = [[0 for x in range(level_breedte)] for y in range(level_hoogte)]
       #Level wordt gekopieerd (stond in str, nu in array)
       for y in range(level_hoogte):
              for x in range(level_breedte):
                     heatmap[y][x] = level[y][x]
                     
       #for i in heatmap:
              #print(i)
       #print('\n')
       
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
       #print(mapFood())
                            
       #for i in heatmap:
              #print(i)
       
       #We geven de warmte van de heatmap mee
       #We laten de warmte uitvloeien
       counter = 0
       max_counter = 4
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

              #for i in heatmap:
                     #print(i)
              #print('\n')
              counter += 1
       return(heatmap)
       
def calculateLimit(heatmap):
       totalSum = 0 
       for y in range(level_hoogte):
              for x in range(level_breedte):
                     totalSum += heatmap[y][x]
       average = totalSum / (level_breedte * level_hoogte)
       return((3*wall_value + average)/4)
       
#for i in mapHeat():
#       print(i)

heatmap = mapHeat()
foodmap = mapFood()
print(calculateLimit(heatmap))
for i in heatmap:
       print(i)
print('\n')
print(foodmap)
foodheat = {}
paths = {}
for (food, distance) in foodmap:
       paths[food] = givePath(snakes[speler_nummer].head, food)
       foodheat[food] = heatmap[food[1]][food[0]]
print(foodheat)
print(paths)
