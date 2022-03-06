# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 12:57:12 2022

@author: user
"""
from enum import Enum
import matplotlib.pyplot as plt
import matplotlib.path as mpPath
import numpy as np
from matplotlib import animation
import matplotlib
args = {"size": 20}
matplotlib.rc("font", **args)

t = 0.1
class State(Enum):
    IDLE = 0
    DRIVING = 1
    CONSENSUS = 2
    
    
class Shape:
    def __init__(self,vertices):
        m,d = vertices.shape
        if d != 2:
            raise Exception("Expected vertices to have shape (m,2)")
        self.vertices = vertices

class Drone:
    def __init__(self, x_init, y_init, ix, identifier):
        self.x = x_init
        self.y = y_init
        self.cons_var = x_init
        self.log = []
        self.log_now()
        self.neighbors = set()
        self.name = ix
        self.identifier = identifier
        self.state = State.IDLE
        self.converged = False
        self.cons_neighbors = set()
        
    def set_target(self, x, y):
        self.target_x = x
        self.target_y = y

    def set_pattern(self,pattern):
        self.pattern = pattern
    
    def neighbor_check(self):
        if len(self.identifier) == 0:
            return True
        for d2 in self.neighbors:
            if len(d2.identifier) == 0:
                continue
            min_id = min(self.identifier, d2.identifier)
            max_id = max(self.identifier, d2.identifier)
            if len(max_id.split(min_id)[0]) == 0:
                if not self.converged:
                    self.identifier = max_id
                return True
        return False
        
    def get_control(self):
        if self.neighbor_check():
            self.consensus_step()
            return 0, 0
        else:
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
        return "Drone: " + str(self.name) + ", " + str(self.state)
    
    def add_neighbor(self, drone2):
        self.neighbors.add(drone2)
        pass
    
    def remove_neighbor(self, drone2):
        if drone2 in self.neighbors:
            self.neighbors.remove(d2)    
        pass
    
    def consensus_step(self):
        # Check for neighbors with the same ID
        for d in self.neighbors:
            if d.identifier == self.identifier:
                self.cons_neighbors.add(d)

        # Initialize consensus variable if first consensus step
        if self.state != State.CONSENSUS:
            self.converged = False
            self.state = State.CONSENSUS
            self.cons_var = self.x if len(self.identifier)%2 == 0 else self.y

        # If we have neighbors with the same ID, perform a step of LCP
        # If we've reached convergence assign a new ID and move to driving state
        deriv = sum([d.cons_var - self.cons_var for d in self.cons_neighbors])
        #print("Agent %s. ID = %s. State = %s. Cons = %.3f. Deriv = %.3f"%(self.name,self.identifier,self.state,self.cons_var,deriv))
        self.cons_var += 1.5*deriv*t
        if abs(deriv) < 0.05:
            self.converged = True

        # If we've converged, assign a new ID and move to driving state
        if self.converged and all([d.converged for d in self.cons_neighbors]):
            if len(self.identifier) %2 == 0:
                self.identifier += "L" if self.x < self.cons_var else "R"
            else:
                self.identifier += "D" if self.y < self.cons_var else "U"
            self.state = State.DRIVING
            self.cons_neighbors.clear()
            self.set_pattern_target()

    def set_pattern_target(self):

        # Get dense points within pattern
        path = mpPath.Path(self.pattern.vertices)
        minx = self.pattern.vertices[:,0].min()
        maxx = self.pattern.vertices[:,0].max()
        miny = self.pattern.vertices[:,1].min()
        maxy = self.pattern.vertices[:,1].max()
        x,y = np.meshgrid(np.linspace(minx,maxx,100),np.linspace(miny,maxy,100))
        x = x.flatten()
        y = y.flatten()
        pts = np.array([x,y]).transpose()
        isin = path.contains_points(pts)
        inpts = pts[isin]

        # Partition points and get target
        for i in range(len(self.identifier)):
            if self.identifier[i] == 'L':
                inpts = inpts[inpts[:,0] < np.mean(inpts[:,0])]
            elif self.identifier[i] == 'R':
                inpts = inpts[inpts[:,0]>= np.mean(inpts[:,0])]
            elif self.identifier[i] == 'U':
                inpts = inpts[inpts[:,1] >= np.mean(inpts[:,1])]
            else:
                inpts = inpts[inpts[:,1] < np.mean(inpts[:,1])]

        self.set_target(np.mean(inpts[:,0]),np.mean(inpts[:,1]))


class GhostServer:
    def __init__(self, drones, targets, max_dist = 5):
        self.fleet = drones
        self.max_dist = max_dist
        self.targets = targets
        pass
    
    def update_pattern(self,pattern):
        for d in self.fleet:
            d.set_pattern(pattern)
    
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
        
    
    
if __name__ == "__main__":
    #%% Initialization 
    d1 = Drone(-1, 0, 0, "LU") #identifier likely initialized as empty string ""   
    d2 = Drone(1, 0, 1, "LRU")
    d3 = Drone(1, 1, 2, "LUD")
    d4 = Drone(-1, 1, 3, "LRD")
    
    fleet = [d1, d2, d3, d4] 
    targets = {0: (0, 1), 1: (0, 1), 2: (0, 1), 3: (0, 1)} #ideally targets shouldn't come from here
    cmap = {0:"blue", 1: "red", 2: "green", 3: "black"} #for plotting
    
    GS = GhostServer(fleet, targets, max_dist=1.0) #comm. range = max_dist
    
    #some stuff to establish the neighborset and give some dummy targets
    GS.update_neighbors()
    GS.update_targets()
    
    
    #%% Simulation loop       
    for i in range(20):
        GS.update_neighbors()
        GS.update_positions()
    
    trajectories = GS.return_trajectories()
    #%% Plotting     
    
    # for i in range(len(fleet)):
    #     plt.plot(trajectories[i, :, 0], trajectories[i, :, 1], label="Drone: "+str(i))
    
    fig, ax = plt.subplots(figsize=[10, 10])
    ax.set_xlim(-2, 2)
    ax.set_ylim(0, 2)
    # data = np.array([o.reshape(o.shape[1], -1) for o in outputs])
    # sns.heatmap(data[0], vmax=1, square=True)
    plt.scatter(0, 1, s=100)
    for i in range(len(fleet)):
        plt.plot(trajectories[i, 0, 0], trajectories[i, 0, 1], label="Drone: "+str(i), color = cmap[i])
        plt.xlabel("$x$ position")
        plt.ylabel("$y$ position")
        
    def init():
          # sns.heatmap(data[0], vmax=1, square=True, cbar=False)
        for i in range(len(fleet)):
            plt.plot(trajectories[i, 0, 0], trajectories[i, 0, 1], label="Drone: "+str(i), color = cmap[i])
        plt.xlabel("$x$ position")
        plt.ylabel("$y$ position")
    
    def animate(j):
        # sns.heatmap(data[i], vmax=1, square=True, cbar=False)
        for i in range(len(fleet)):
            plt.plot(trajectories[i, :j, 0], trajectories[i, :j, 1], label="Drone: "+str(i), color = cmap[i])
        plt.xlabel("$x$ position")
        plt.ylabel("$y$ position")
    
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(trajectories[0]), repeat = True)
    
    #%% save animation
    f = r"trajectories2.mp4" 
    writervideo = animation.FFMpegWriter(fps=1/t) 
    anim.save(f, writer=writervideo)
    
