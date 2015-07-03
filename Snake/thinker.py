from mapper import mapFood
from mapper import mapHeat
from queue import PriorityQueue
from mapper import calculateLimit
from mapper import givePath
from level import Map
from snake import Snake

wall_value = 1000
level = Map(['..............................',
    '.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#', 
    '.............................x',
    '.#.#.#.#.#.#.#x#.#.#.#.#.#.#.#',
    '..#..................x........',   
    '.#.#.#.#.#.#.#.#.#x#.#.#.#.#.#',
    '#...#.......x.................',
    '.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#', 
    '.#0#........................1.',
    '.###.#.#.#.#.#.#x#.#.#.#.#.#.#'], 10, 30, [Snake([(2,8)]), Snake([(28,8)])], 
    0, 2, 6, 
    [(29,2), (14,3), (21,4), (18,5), (12,6), (16,9)])


def giveConclusion(level):       
    foodmap = mapFood(level)
    heatmap = mapHeat(level)
    foodheat = {}
    foods = PriorityQueue()
    good_food = 0
    for (distance, food) in foodmap:
            foodheat[food] = heatmap.level[food[1]][food[0]]
            limit = max(950,calculateLimit(heatmap))
            if foodheat[food] < limit:
                foods.put((distance, food))
    if not foods.empty():
        good_food = foods.get()[1]
        head = level.snakes[level.speler_nummer].head
        path = givePath(level, head, good_food)
        direction = level.giveDirection(path[0], path[1])
    else:
        minimum = wall_value
        direction = -1
        head = level.snakes[level.speler_nummer].head
        backuplist = []
        for coordinate in level.neighbours(head):
            if heatmap.level[coordinate[1]][coordinate[0]] < minimum:
                direction = level.giveDirection(head, coordinate)
                minimum = heatmap.level[coordinate[1]][coordinate[0]]
            elif level.level[coordinate[1]][coordinate[0]] in ['.','x']:
                backuplist.append(coordinate)
        if direction == -1:
                if len(backuplist)!= 0:
                    direction = level.giveDirection(head,backuplist[0])
                else:
                    print("Goodbye, cruel world!")
                    direction = 'r'
    #TESTCODE
    
    #print("foodmap =" ,foodmap)
    #print("HEATMAP:")
    #print(heatmap)
    #print(level)
    #print("foodheat =", foodheat)
    #if(foodmap != []):
    #    print("limit =", limit)
    #if good_food!= 0:
    #    print("Going to", good_food)
    #else:
    #    print("Going nowhere")
    
    return direction