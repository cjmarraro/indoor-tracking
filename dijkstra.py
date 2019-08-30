#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import heapq

class Vertex:
    def __init__(self, u):
        self.value = u
        self.adj = {} #Adj[u]
        self.estD = sys.maxsize
        self.searched = False  
        self.parent = None
        
    def __lt__(self, other):
        return self.estD < other.estD

    def add_neighbor(self, neighbor, weight=0):
        self.adj[neighbor] = weight

    def get_link(self):
        return self.adj.keys()  

    def get_value(self):
        return self.value

    def get_weight(self, neighbor):
        return self.adj[neighbor]

    def set_estD(self, dist):
        self.estD = dist

    def get_estD(self):
        return self.estD

    def set_parent(self, prev):
        self.parent = prev

    def set_searched(self):
        self.searched = True

    def __str__(self):
        return str(self.value) + ' adj: ' + str([x.value for x in self.adj])

class Graph:
    def __init__(self):
        self.vertices = {}
        self.value_vertices = 0

    def __iter__(self):
        return iter(self.vertices.values())

    def add_vertex(self, u):
        self.value_vertices = self.value_vertices + 1
        new_v = Vertex(u)
        self.vertices[u] = new_v
        return new_v

    def get_vertex(self, k):
        if k in self.vertices:
            return self.vertices[k]
        else:
            return None

    def add_edge(self, v_i, v_j, wt=0):
        if v_i not in self.vertices:
            self.add_vertex(v_i)
        
        if v_j not in self.vertices:
            self.add_vertex(v_j)
       
        self.vertices[v_i].add_neighbor(self.vertices[v_j], wt)
        self.vertices[v_j].add_neighbor(self.vertices[v_i], wt)

    def get_vertices(self):
        return self.vertices.keys()

    def set_parent(self, current):
        self.parent = current

    def get_parent(self):
        return self.parent

def delta_SP(v, path):
    ''' get shortest path to parent node, v'''
    if v.parent:
        path.append(v.parent.get_value())
        delta_SP(v.parent, path)
    return

def dijkstra(graph, init):
    print ('''Dijkstra's shortest path''')
    #Initialize single source node s := 0 for G(V, s) 
    init.set_estD(0)    
    #Insert (estD(v),v) into min priority queue,Q, for each v in the set V - {s}
    Q = [(v.get_estD(),v) for v in graph] 
    heapq.heapify(Q)     
    
    #Extracts vertex with smallest estD in Q, adds to S
    while len(Q): 
        s_to_v = heapq.heappop(Q)
        current = s_to_v[1]
        current.set_searched()        

        #Relax
        for node in current.adj:  
            if node.searched:
                continue
            update_estD = current.get_estD() + current.get_weight(node)            
            if update_estD < node.get_estD():
                node.set_estD(update_estD)
                node.set_parent(current)
                print ('updated : current = %s next = %s update_estD = %s' \
                        %(current.get_value(), node.get_value(), node.get_estD()))
            else:
                print ('not updated : current = %s next = %s update_estD = %s' \
                        %(current.get_value(), node.get_value(), node.get_estD()))        
        #Rebuild heap
        while len(Q): 
            heapq.heappop(Q)
        #Assign vertices not searched to Q    
        Q = [(v.get_estD(),v) for v in graph if not v.searched] 
        heapq.heapify(Q)


if __name__ == '__main__':

    g = Graph()

    g.add_vertex('a1')
    g.add_vertex('a2')
    g.add_vertex('a3')
    g.add_vertex('b1')
    g.add_vertex('b2')
    g.add_vertex('b3')

    g.add_edge('a1', 'a2', 7)  
    g.add_edge('a1', 'a3', 9)
    g.add_edge('a1', 'b3', 14)
    g.add_edge('a2', 'a3', 10)
    g.add_edge('a2', 'b1', 15)
    g.add_edge('a3', 'b1', 11)
    g.add_edge('a3', 'b3', 2)
    g.add_edge('b1', 'b2', 6)
    g.add_edge('b2', 'b3', 9)

    print ('Graph data:')
    for v in g:
        for w in v.get_link():
            v_val = v.get_value()
            w_val = w.get_value()
            print ('( %s , %s, %3d)'  % ( v_val, w_val, v.get_weight(w)))        
    
    dijkstra(g, g.get_vertex('a1')) 
    target = g.get_vertex('b2')
    path = [target.get_value()]
    delta_SP(target, path)
    
    print ('The shortest path : %s' %(path[::-1]))
 