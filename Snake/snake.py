class Snake(object):
    def __init__(self, segments=[]):
        self.segments = segments
    
    def __str__(self):
        return(str(self.segments))
        
    def move(self, coordinate, value):
        if value == '.':
            self.segments.pop(0)
        self.segments.append(coordinate)
        
    
#snake = Snake([[0,0],[0,1]])
#snake.move([1,1],'.')
#snake.move([1,2], 'x')

#print(snake)
