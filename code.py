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
import matplotlib.patches as patches
import matplotlib
args = {"size": 20}
matplotlib.rc("font", **args)

t = 0.01
class State(Enum):
    IDLE = 0
    DRIVING = 1
    CONSENSUS = 2


class Shape:
    def __init__(self, vertices, update_rule='STATIC'):

        self.update_rule = update_rule # possible options = 'STATIC','TRANSLATE','EXPAND'
        self.path = mpPath.Path(vertices)
        self.vertices = self.path.vertices # np array
        m,d = vertices.shape
        if d != 2:
            raise Exception("Expected vertices to have shape (m,2)")

        # Parameters
        self.dx = 0.1; self.dy = 0.1 # for translation
        self.center = np.mean(vertices, axis=0) # for expansion
        self.expand_rate = 0.1

    def update(self):
        if self.update_rule == 'STATIC':
            pass
        elif self.update_rule == 'TRANSLATE':
            # Simple translation
            self.vertices += [self.dx, self.dy]
        elif self.update_rule == 'EXPAND':
            # Expand points out from center
            dx = self.expand_rate * (self.vertices - self.center)
            self.vertices += dx

        self.path = mpPath.Path(self.vertices)

    def visualize(self, ax):
        patch = patches.PathPatch(self.path, facecolor='blue', alpha = 0.2, lw=0)
        ax.add_patch(patch)


class Drone:
    def __init__(self, x_init, y_init, ix, identifier=""):
        self.x = x_init
        self.y = y_init
        self.cons_var = x_init
        self.log = []
        self.state_log = []
        self.neighbors = set()
        self.name = ix
        self.identifier = identifier
        self.state = State.IDLE
        self.converged = False
        self.cons_neighbors = set()
        self.vx = 0
        self.vy = 0

        self.speed_max = 1.5
        self.speed_pref = 1
        self.speed_min = 0.5

        speeds = np.linspace(self.speed_min, self.speed_max, 10)
        dirs = np.linspace(0., 2*np.pi, 36)
        self.vels = []
        for i in range(10):
            for j in range(36):
                self.vels.append(np.array([[speeds[i]*np.cos(dirs[j])], [speeds[i]*np.sin(dirs[j])]]))

        self.log_now()

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
                if not self.converged and self.state != State.CONSENSUS:
                    self.identifier = max_id
                return True
        return False

    def set_vel(self):
        if self.neighbor_check():
            self.consensus_step()
            self.vx = 0
            self.vy = 0
        elif np.sqrt((self.x-self.target_x)**2 + (self.y-self.target_y)**2) < 0.05:
            self.vx = 0
            self.vy = 0
        else:
            self.set_vel_collision_avoidance();

    def get_vel(self):
        return self.vx, self.vy

    def update_position(self):
        self.set_vel()
        self.x = self.x + self.vx*t
        self.y = self.y + self.vy*t
        self.log_now()

    def log_now(self):
        self.log.append((self.x, self.y))
        if self.state == State.DRIVING and np.linalg.norm(np.array([self.target_x,self.target_y])-np.array([self.x,self.y])) < 0.05:
            self.state_log.append(State.IDLE)
        else:
            self.state_log.append(self.state)

    def get_position(self):
        return np.array([self.x, self.y])

    def __repr__(self):
        return "Drone: " + str(self.name) + ", " + str(self.state)

    def add_neighbor(self, drone2):
        self.neighbors.add(drone2)
        pass

    def remove_neighbor(self, drone2):
        if drone2 in self.neighbors:
            self.neighbors.remove(drone2)
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
        self.cons_var += 0.01*deriv
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

    def set_vel_collision_avoidance(self):

        # define some constants defining robot geometries and check_constraints
        R = 0.1 # radius of circular robots

        vA = np.array([[self.vx], [self.vy]])
        pos_A_target = np.array([[self.target_x-self.x], [self.target_y-self.y]])
        v_pref = self.speed_pref * pos_A_target / np.linalg.norm(pos_A_target) # preferred speed in the direction of target

        vels = self.vels.copy()

        # Loop through all drones, remove the velocities that are in the velocity obstacles

        for drone in self.neighbors:

            vB = np.array([[drone.vx], [drone.vy]])
            pos_AB = np.array([[drone.x-self.x], [drone.y-self.y]])
            dist_AB = np.linalg.norm(pos_AB)
            theta = np.arcsin(2.2*R / dist_AB)

            a_right = np.array([[np.cos(np.pi/2-theta), np.sin(np.pi/2-theta)], [-np.sin(np.pi/2-theta), np.cos(np.pi/2-theta)]]) @ pos_AB/dist_AB
            a_left = np.array([[np.cos(theta-np.pi/2), np.sin(theta-np.pi/2)], [-np.sin(theta-np.pi/2), np.cos(theta-np.pi/2)]]) @ pos_AB/dist_AB

            counter = 0
            while counter < len(vels):
                if a_right.T @ (2*vels[counter] - vA - vB) > 0 and a_left.T @ (2*vels[counter] - vA - vB) > 0:
                    vels.pop(counter)
                else:
                    counter = counter + 1

        # Optimize over the velocities that are left

        if len(vels) == 0:
            self.vx = 0
            self.vy = 0
        else:
            vels_possible = np.array(vels).reshape((len(vels), 2)).T
            cost = np.linalg.norm(vels_possible-v_pref, axis=0)
            best_index = np.argmin(cost)

            self.vx = vels_possible[0,best_index]
            self.vy = vels_possible[1,best_index]


class GhostServer:
    def __init__(self, drones, targets, pattern, max_dist = 5):
        self.fleet = drones
        self.max_dist = max_dist
        self.targets = targets
        self.pattern = pattern
        for d in self.fleet:
            d.set_pattern(self.pattern)

    def update_pattern(self):
        self.pattern.update()
        for d in self.fleet:
            d.set_pattern(self.pattern)

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

    def return_states(self):
        return np.array([d.state_log for d in self.fleet])


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
