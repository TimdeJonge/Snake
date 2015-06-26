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
        
    def move(self, coordinate, value):
        if coordinate == self.segments[-1]:
            pass
        else:
            if value == 'x':
                self.score += 99
            else:
                self.segments.pop(0)
            self.segments.append(coordinate)
            self.score += 1
            

#snake = Snake([(0,0),(0,1)])
#snake.setDimensions(10,10)
#snake.move((1,1),'.')
#snake.move((1,2), 'x')
#snake.move((1,3), 'x')
#snake.move((1,3), 'x')
#snake.move((1,3), 'x')

#print(snake)
