from Source import Source
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

class Rectangle:
   def __init__(self, corner, width = 1, height = 1):
      x = corner[0]
      y = corner[1]
      self.points = Path([(x,y),
                     (x,y+height),
                     (x+width,y+height),
                     (x+width,y),
                     (x,y)])

#Bounding box
xmin = 0
xmax = 10
ymin = 0
ymax = 15

box = [(xmin,ymin),
(xmin,ymax),
(xmax,ymax),
(xmax,ymin),
(xmin,ymin)]

w1 = Rectangle((1,0),height=10)
w2 = Rectangle((1,11),width=3)
w3 = Rectangle((3,13),height=2)
w4 = Rectangle((5,3),width=3, height=6)
w5 = Rectangle((6,11), height=4)
w6 = Rectangle((7,5), width = 2, height=4)
w7 = Rectangle((8,9),height=6)
w8 = Rectangle((3,0),width=7, height=2)
w9 = Rectangle((8,3),width=1)
w10 = Rectangle((2.5,3),width=2,height=4)

objects = [w1.points,w2.points,w3.points,w4.points,w5.points,w6.points,w7.points,w8.points,w9.points,w10.points]

source = Source(4,6,objects,box)
source.draw_rays()

