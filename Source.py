import numpy as np
from matplotlib import path
from Beam import Beam
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Source:
    def __init__(self, x_center, y_center, objects, box):
        self.x = x_center
        self.y = y_center
        self.objects = objects
        self.box = box
        self.rays = self._create_rays()


    def _create_rays(self):
        blocks = self.objects
        box = self.box
        #Append all points in all objects into a single list
        points = [[tuple(vertices) for vertices in block.vertices] for block in blocks]

        #To handle corners, add a small ray above and below each ray
        offset = []
        for point in points:
            for pnt in point:
                offset.append((pnt[0]+.001,pnt[1]+.001))
                offset.append((pnt[0]-.001,pnt[1]-.001))
        points.append(offset)
        points.append(box)

        #Remove duplicate points
        points = list(set([vertices for point in points for vertices in point]))

        #Create a ray to each point from the source, then check which sides of each block it intersects, and take the closest point
        ray_intersections = []
        for point in points:
            ray = Beam(x1 = self.x, y1 = self.y, x2 = point[0], y2 = point[1])
            nearest_intersections = [] #for each ray
            
            for block in blocks: #Iterate across all polygons
                for k in range(len(block.vertices)-1): #Iterate across each face of the polygon
                    #Calculate intersections with each face of the polygon
                    p3 = block.vertices[k]
                    p4 = block.vertices[k+1]
                    intersection = ray.intersection(p3, p4)
                    #Ignore intersections that hit the corners of polygons, since we want them to extend further
                    if intersection:
                        nearest_intersections.append(intersection)

            #Add in intersections of the ray with the sides of the box            
            for i in range(4):
                pnt = ray.intersection(box[i],box[i+1])
                if pnt:
                    nearest_intersections.append(pnt)

            #Check the distance from the center along the ray and just take the closest one
            min_dist = np.inf
            for pnt in nearest_intersections:
                x = pnt[0]
                y = pnt[1]
                distance = np.sqrt((self.x-x)**2 + (self.y-y)**2)
                if distance < min_dist:
                    min_dist = distance
                    nearest_point = pnt
            ray_intersections.append(nearest_point)

        #Order the list clockwise
        angles = []
        for point in ray_intersections:
            x_len = self.x - point[0]
            y_len = self.y - point[1]
            if x_len == 0:
                theta = np.pi/2
            else:
                theta = np.arctan(y_len/x_len)
            if x_len < 0:
                theta = theta + np.pi
            if theta < 0:
                theta = theta + 2*np.pi
            angles.append(theta)
        ray_intersections = [y for x,y in sorted(zip(angles,ray_intersections))]
        ray_intersections.append(ray_intersections[0])
        return ray_intersections

#This draws all the rays on a canvas with filled in color
    def mouse_move(self,event):
        
        self.x, self.y = event.xdata, event.ydata
        try:
            self.rays = self._create_rays()
            for i in range(len(self.ax.patches)):
                self.ax.patches.pop()
            for i in range(len(self.rays)-1):
                pts = np.array([(self.x,self.y), self.rays[i], self.rays[i+1],(self.x,self.y)])
                patch = patches.Polygon(pts, facecolor = 'white', lw = 0)
                self.ax.add_patch(patch)
            for object in self.objects:
                patch = patches.PathPatch(object, facecolor='none', lw=0)
                self.ax.add_patch(patch)
            self.fig.canvas.draw_idle()
        except:
            return False
        
    def draw_rays(self):
        plt.style.use('dark_background')
        # img = plt.imread('gabby.png')
        xlims = [min([pnt[0] for pnt in self.box]), max([pnt[0] for pnt in self.box])]
        ylims = [min([pnt[1] for pnt in self.box]), max([pnt[1] for pnt in self.box])]
        self.fig, self.ax = plt.subplots()
        # self.ax.imshow(img, extent=[xlims[0], xlims[1], ylims[0], ylims[1]])
        self.ax.set_xlim(xlims[0], xlims[1])
        self.ax.set_ylim(ylims[0], ylims[1])
        for i in range(len(self.rays)-1):
            pts = np.array([(self.x,self.y), self.rays[i], self.rays[i+1],(self.x,self.y)])
            patch = patches.Polygon(pts, facecolor = 'white', lw = 0)
            self.ax.add_patch(patch)
        # for point in self.rays:
        #     plt.plot([point[0],self.x],[point[1],self.y], 'bo', linestyle="-")
        for object in self.objects:
            patch = patches.PathPatch(object, facecolor='none', lw=0)
            self.ax.add_patch(patch)

        plt.connect('motion_notify_event', self.mouse_move)
        plt.axis('off')
        plt.show()