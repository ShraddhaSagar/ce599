class car(object):
    "Attributes:color, location(x,y) and direction"
    def __init__(auto, color,location,direction):
        if len(location) < 2 or len(location) > 2:
            print('location is the x,y coordinates of the car')
        else:    
            auto.color = color
            auto.location = location
            auto.x = location[0] 
            auto.y = location[1]
            auto.direction = direction
   
    def go(auto,l):#to move forward
        if auto.direction == 'N':
            auto.location.y = auto.location.y+l
            return print_car(auto)
        elif auto.direction == 'S':
            auto.location.x = auto.location.x+l
            return print_car(auto)
        elif auto.direction == 'E':
            auto.location.y = auto.location.y-l
            return print_car(auto)
        elif auto.direction == 'W':
            auto.location.x = auto.location.x-l
            return print_car(auto)
        else:
            return
        
    def turn_right(auto):#to turn right
        if auto.direction == 'N':
            auto.direction = 'E'
        elif auto.direction == 'S':
            auto.direction = 'W'
        elif auto.direction == 'E':
            auto.direction = 'S'
        elif auto.direction == 'W':
            auto.direction = 'N'
        else:
            print('INVALID')
            
    def turn_left(auto):#to turn left
        if auto.direction == 'N':
            auto.direction = 'W'
        elif auto.direction == 'S':
            auto.direction = 'E'
        elif auto.direction == 'E':
            auto.direction = 'N'
        elif auto.direction == 'W':
            auto.direction = 'S'
        else:
            print('INVALID')

    def printcar(auto):
    print(str(auto.color), 'car is at', str(auto.location), 'in the', str(auto.direction),'direction')
    