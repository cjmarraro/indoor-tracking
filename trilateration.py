#!/usr/bin/env python3
# -*- coding:utf-8 -*-
 
import random
import math
import numpy as np
import types
import json
from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.2f')
np.seterr(divide='ignore', invalid='ignore')

class Point(object):    
    def __init__(self, x, y):
        self.x = x
        self.y = y
       
    def __isub__(self, other):
        return self.x - other.x, self.y - other.y
                    
    def __itruediv__(self, scalar=int):
        if scalar == 0:
            return 
        return self/scalar       
 
    def __next__(self):
        if not self.x or not self.y:
            raise StopIteration
        return self.x.pop(), self.y.pop()      

    def __iter__(self):
        return self

    @classmethod
    def get_two_points_distance(cls, q, p):
        return math.sqrt(pow((q.x - p.x), 2) + pow((q.y - p.y), 2))
        
class Circle(object):    
    def __init__(self, Point, radius):
        self.center = Point
        self.radius = radius
    
    def __isub__(self, other):
        return self.center - other.center, self.radius - other.radius
   
    def __iadd__(self,other):
        return self.center + other.center, self.radius + other.radius
                
    def __itruediv__(self, scalar=int):   
        if scalar == 0:
            return 
        return self.center/scalar

    def __next__(self):
        if not self.center or not self.radius:
            raise StopIteration
        return self.center.pop(), self.radius.pop()
    
    def __iter__(self):
        return self

    @classmethod
    def get_two_circles_intersecting_points(cls, cj, ck):
        d = Point.get_two_points_distance(cj.center, ck.center)       
        if d >= (cj.radius + ck.radius) or d <= math.fabs(cj.radius - ck.radius):
            return None   
        a = (pow(cj.radius, 2) - pow(ck.radius, 2) + pow(d, 2)) / (2*d)
        h  = math.sqrt(pow(cj.radius, 2) - pow(a, 2))
        x0 = cj.center.x + a*(ck.center.x - cj.center.x)/d 
        y0 = cj.center.y + a*(ck.center.y - cj.center.y)/d
        rx = -(ck.center.x - cj.center.x) * (h/d)
        ry = -(ck.center.y - cj.center.y) * (h / d)   
        return [Point(x0+rx, y0-ry), Point(x0-rx, y0+ry)]
    

class json_data(object):
    def __init__(self, circles, inner_points, center):
        self.circles = circles
        self.inner_points = inner_points
        self.center = center
    @staticmethod                    
    def jdefault(o):
        if isinstance(o, types.GeneratorType):
            return list(o)
        return o.__dict__

def get_all_intersecting_points(circles):
    points = []
    num = len(circles)
    for i in range(num):
        j = i + 1
        for k in range(j, num):
            res = Circle.get_two_circles_intersecting_points(circles[i], circles[k])
            if res:
                points.extend(res)
    return points

def is_contained_in_circles(point, circles):
    for i, _ in enumerate(circles):
        if Point.get_two_points_distance(point, circles[i].center) > circles[i].radius:
            return False
        return True

def get_polygon_center(points):
    center = Point(0, 0)
    num = len(points)
    for i in range(num):
        center.x += points[i].x
        center.y += points[i].y
    try:
        center.x /= num
        center.y /= num   
    except ZeroDivisionError:
        return    
    return center


if __name__ == '__main__':

    def get_x(x0):
            yield from x0
            
    def get_y(y0):
            yield from y0
            
    def get_r(r0):                    
            yield from r0
            
    xx= [10*random.random() for x in range(10)]
    
    yy= [10*random.random() for y in range(10)]
   
    rr= [10*random.random() for r in range(10)]
    
    xcoord = get_x(xx)
    ycoord = get_y(yy)
    rad = get_r(rr)
    
    
    p1 = Point(next(xcoord), next(ycoord))
    p2 = Point(next(xcoord), next(ycoord))
    p3 = Point(next(xcoord), next(ycoord))
    
   
    c1 = Circle(p1, next(rad))
    c2 = Circle(p2, next(rad))
    c3 = Circle(p3, next(rad))
    
    
    circle_list = [c1, c2, c3]
    

    inner_points = []
    for p in get_all_intersecting_points(circle_list):
        if is_contained_in_circles(p, circle_list):
            inner_points.append(p) 
    
    center = get_polygon_center(inner_points)
    
    in_json = json_data([c1,c2,c3], [p1,p2,p3], center)
    
    out_json = json.dumps(in_json, sort_keys=True,
                          indent=4, default= json_data.jdefault)
    
    with open("data.json", 'a') as fw:
        while center is None:
            continue
        fw.write(out_json)