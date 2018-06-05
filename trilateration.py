#!/usr/bin/env
# -*- coding:utf-8 -*-
 
import random
import math
import json
from json import encoder
import numpy as np
encoder.FLOAT_REPR = lambda o: format(o, '.2f')


def get_coords(pi):
    return [{"x": 10*random.random(), "y": 10*random.random(), "r": 10*random.random()}
            for x in pi for y in pi for r in pi]
    

xyr = get_coords(range(2))

d = {'x': [i['x'] for i in xyr], 'y': [j['y'] for j in xyr], 'r': [k['x'] for k in xyr]}


np.seterr(divide='ignore', invalid='ignore')

class point:    
    def __init__(self, x, y):
        self.x = x
        self.y = y
   
    
    def __sub__(self, other):
        return self.x - other.x, self.y -other.y
        
            
    def __itruediv__(self, scalar=int):
        if scalar == 0:
            return None
        return self/scalar       
 
    def __next__(self):
        if not self.x or self.y:
            raise StopIteration
        return self.x.pop(), self.y.pop()      

    def __iter__(self):
        return iter(self)
    
        
class circle:    
    def __init__(self, point, radius):
        self.center = point
        self.radius = radius
    
    def __sub__(self, other):
        return self.center - other.center, self.radius - other.radius
   
    def __add__(self,other):
        return self.center + other.center, self.radius + other.radius
                
    def __itruediv__(self, scalar=int):   
        if scalar == 0:
            return None
        return self.center / scalar


    def __next__(self):
        if not self.center or self.radius:
            raise StopIteration
        return self.center.pop(), self.radius.pop()
    
    def __iter__(self):
        return iter(self)
    

class json_data:
    def __init__(self, circles, inner_points, center):
        self.circles = circles
        self.inner_points = inner_points
        self.center = center
                    
def jdefault(o):
    if isinstance(o, np.ndarray):
        return list(o)
    return o.__dict__

def get_two_points_distance(p1 = [], p2 = []):
    return math.sqrt(pow((p1.x - p2.x), 2) + pow((p1.y - p2.y), 2))


def get_two_circles_intersecting_points(c1 = [], c2 = []):
    d = get_two_points_distance(c1.center,c2.center)
    if d >= (c1.radius + c2.radius) or d <= math.fabs(c1.radius -c2.radius):
        return None
    
    a = (pow(c1.radius, 2) - pow(c2.radius, 2) + pow(d, 2)) / (2*d)
    h  = math.sqrt(pow(c1.radius, 2) - pow(a, 2))
    x0 = c1.center.x + a*(c2.center.x - c1.center.x)/d 
    y0 = c1.center.y + a*(c2.center.y - c1.center.y)/d
    rx = -(c2.center.y - c1.center.y) * (h/d)
    ry = -(c2.center.x - c1.center.x) * (h / d)
    
    return [point(x0+rx, y0-ry), point(x0-rx, y0+ry)]


def get_all_intersecting_points(circles):
    points = []
    num = len(circles)
    for i in range(num):
        j = i + 1
        for k in range(j, num):
            res = get_two_circles_intersecting_points(circles[i], circles[k])
            if res:
                points.extend(res)
    return points


def is_contained_in_circles(point, circles):
    for i, _ in enumerate(circles):
        if get_two_points_distance(point, circles[i].center) > circles[i].radius:
            return False
        return True


def get_polygon_center(points):
    center = point(0, 0)
    num = len(points)
    for i in range(num):
        center.x += points[i].x
        center.y += points[i].y
    try:
        center.x /= np.array(num)
        center.y /= np.array(num)   
    except ZeroDivisionError:
        return 0.0    
    return center


if __name__ == '__main__' :
    
    
    p1 = point(d['x'][0],d['y'][0])
    p2 = point(d['x'][1] ,d['y'][1])
    p3 = point(d['x'][2] ,d['y'][2])

    p4 = point(d['x'][3],d['y'][3])
    p5 = point(d['x'][4],d['y'][4])
    p6 = point(d['x'][5],d['y'][5])

    c1 = circle(p1, d['r'][0])
    c2 = circle(p2, d['r'][1])
    c3 = circle(p3, d['r'][2])
    
    c4 = circle(p4, d['r'][3])
    c5 = circle(p5, d['r'][4])
    c6 = circle(p6, d['r'][5])
    
    circle_list = [c1,c2,c3,c4,c5,c6]


    inner_points = []
    for p in get_all_intersecting_points(circle_list):
        if is_contained_in_circles(p, circle_list):
            inner_points.append(p) 
    
    center = get_polygon_center(inner_points)
    
    in_json = json_data([c1,c2,c3,c4,c5,c6], [p1,p2,p3,p4,p5,p6], center)
    
    out_json = json.dumps(in_json, sort_keys=True,
                          indent=4, default=jdefault)
    
    with open("data.json", 'w') as fw:
        fw.write(out_json)