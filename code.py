# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 12:57:12 2022

@author: user
"""
import matplotlib.pyplot as plt
import numpy as np


t = 0.1

class Drone:
    def __init__(self, x_init, y_init, ix):
        self.x = x_init
        self.y = y_init
        self.log = []
        self.log_now()
        self.neighbors = set()
        self.name = ix
        
    def set_target(self, x, y):
        self.target_x = x
        self.target_y = y
    
    def get_control(self):
        u_x = self.target_x - self.x
        u_y = self.target_y - self.y
        return u_x, u_y
    
    def update_position(self):
        u_x, u_y = self.get_control()
        self.x = self.x + u_x*t
        self.y = self.y + u_y*t
        self.log_now()
    
    def log_now(self):
        self.log.append((self.x, self.y))
        
    def get_position(self):
        return np.array([self.x, self.y])
    
    def __repr__(self):
        return "Drone: " + str(self.name)
    
    def add_neighbor(self, drone2):
        self.neighbors.add(drone2)
        pass
    
    def remove_neighbor(self, drone2):
        if drone2 in self.neighbors:
            self.neighbors.remove(d2)
        
        pass
    


class GhostServer:
    def __init__(self, drones, targets, max_dist = 5):
        self.fleet = drones
        self.max_dist = max_dist
        self.targets = targets
        pass
    
    def update_targets(self, targets=None):
        for d1 in self.fleet:
            d1.set_target(*self.targets[d1.name])
    
    def neighbors(self, pos_1, pos_2):
        if np.linalg.norm(pos_1 - pos_2) < self.max_dist:
            return True
    
    def update_neighbors(self):
        for d1 in self.fleet:
            fleet_copy = self.fleet.copy()
            fleet_copy.remove(d1)
            for d2 in fleet_copy:
                if self.neighbors(d1.get_position(), d2.get_position()):
                    d1.add_neighbor(d2)
                else:
                    d1.remove_neighbor(d2)
                    
    def update_positions(self):
        for d1 in self.fleet:
            d1.update_position()
    
    def return_trajectories(self):        
        return np.array([d.log for d in self.fleet])
    
        
d1 = Drone(-1, 0, 0)    
d2 = Drone(1, 0, 1)
fleet = [d1, d2]
targets = {0: (0, 1), 1: (0, 1)}

GS = GhostServer(fleet, targets)
GS.update_neighbors()
GS.update_targets()

print(d1.neighbors)
print(d2.neighbors)
        
        
for i in range(20):
    GS.update_neighbors()
    GS.update_positions()
    
trajectories = GS.return_trajectories()

for i in range(len(fleet)):
    plt.plot(trajectories[i, :, 0], trajectories[i, :, 1], label="Drone: "+str(i))
    
    
# trajectory = np.array(d.log)
# plt.plot(trajectory[:, 0], trajectory[:, 1])