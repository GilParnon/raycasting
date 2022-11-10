import numpy as np

class Beam:
    def __init__(self, x1 = 0, y1 = 0, x2 = 1, y2 = 1):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def intersection(self, p3, p4):
        #https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_line_segment
        x3 = p3[0]
        x4 = p4[0]
        y3 = p3[1]
        y4 = p4[1]
        u = (self.x1-x3)*(self.y1-self.y2)-(self.y1-y3)*(self.x1-self.x2)
        t = (self.x1-x3)*(y3-y4)-(self.y1-y3)*(x3-x4)
        denom = (self.x1-self.x2)*(y3-y4)-(self.y1-self.y2)*(x3-x4)
        if denom!=0: 
            u /= denom
            t /= denom
            if u <= 1 and u >= 0 and t >= 0:
                x = (x3+u*(x4-x3))
                y = (y3+u*(y4-y3))
                return (x,y)    
            else:
                return False