class Snake(object):
    def __init__(self, segments=[], score = 0, level_breedte = 10, level_hoogte = 10):
        self.segments = segments
        self.score = score
    
    def __str__(self):
        return(str(self.segments))
    
    def getScore(self):
        return(self.score)
    
    def setDimensions(self, breedte, hoogte):
        self.level_breedte = breedte
        self.level_hoogte = hoogte 
        
    def move(self, direction, value):
        dx = [0,  1, 0, -1]
        dy = [-1, 0, 1,  0] 
        legend ='urdl'
        if value == 'x':
            self.score += 100
        else:
            self.segments.pop(0)
        i = legend.index(direction)
        coordinate = ((self.segments[-1][0] + dy[i]) % self.level_hoogte, (self.segments[-1][1] + dx[i]) % self.level_breedte)
        self.segments.append(coordinate)
        self.score += 1
        

snake = Snake([(0,0),(0,1)])
snake.setDimensions(10,10)
snake.move('r','.')
snake.move('u', 'x')
snake.move('u', 'x')
snake.move('u', 'x')
snake.move('u', 'x')
snake.move('u', 'x')
