class Snake(object):
    def __init__(self, segments=[], score = 0, last_segment = (), head = ()):
        self.segments = segments
        self.head = segments[-1]
        self.score = score
    
    def __str__(self):
        return(str(self.segments))
    
    def getScore(self):
        return(self.score)
        
        
    def move(self, coordinate, value):
        if coordinate == self.segments[-1]:
            pass
        else:
            if value == 'x':
                self.score += 99
            else:
                self.last_segment = self.segments.pop(0)
                #print(self.segments)
            self.segments.append(coordinate)
            self.head = coordinate
            self.score += 1
            #print(self.segments)


#snake = Snake([(0,0),(0,1)])
#snake.move((1,1),'.')
#print(snake.last_segment)
#snake.move((1,2), '.')
#print(snake.last_segment)
#snake.move((1,3), 'x')
#snake.move((1,3), 'x')
#snake.move((1,3), 'x')


#print(snake)
