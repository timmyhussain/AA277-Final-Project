
from code import Drone, GhostServer, State
from pattern import Shape, Pattern
from enum import Enum
import matplotlib.pyplot as plt
import matplotlib.path as mpPath
import numpy as np
from matplotlib import animation
import matplotlib
import time

args = {"size": 20}
matplotlib.rc("font", **args)


if __name__ == "__main__":
    #%% Initialization

    start_time = time.time()

    # parameters
    t = 0.01
    num_steps = 1500
    num_agents = 20
    reduce = 10
    axlim = 15
    init_bounds = 1

    #pattern = Shape(1.5*np.array([[-1,-1,1,1],[-1,1,1,-1]]).transpose(), 'TRANSLATE')
    #pattern = Shape(np.array([[-1,-1,1,1],[-1,1,1,-1]]).transpose(), 'EXPAND')
    # V = np.array([[0,5], 
    #               [1,1],
    #               [5,0],
    #               [1,-1],
    #               [0,-5],
    #               [-1,-1],
    #               [-5,0],
    #               [-1,1]])
    # pattern = Shape(V)

    R = 5; th = np.linspace(0,2*np.pi,10)
    V1 = np.array([R * np.cos(th), R* np.sin(th)])
    V1 += 6
    V1 = V1.T
    V2 = np.array([[0,5], 
                [1,1],
                [5,0],
                [1,-1],
                [0,-5],
                [-1,-1],
                [-5,0],
                [-1,1]])
    V_arr = [V1,V2]
    pattern = Pattern(V_arr)

    fleet = []
    # np.random.seed(1)
    # for i in range(num_agents):
    #     x = 2*np.random.random()
    #     y = 2*np.random.random()
    #     fleet.append(Drone(x,y,i))

    GS = GhostServer(fleet,[],pattern,max_dist=2.5)
    GS.init_fleet(num_agents, init_bounds)

    GS.update_neighbors()

    #%% Simulation loop
    for i in range(num_steps):
        if i%25 == 0:
            print("Iteration %d of %d" %(i, num_steps))
            #print(GS.pattern.vertices)
            for k in range(len(fleet)):
                target = "None"
                if i > 1 and GS.fleet[k].state != State.CONSENSUS:
                    target = "(%.3f,%.3f)"%(GS.fleet[k].target_x,GS.fleet[k].target_y)
                position = "(%.3f,%.3f)"%(GS.fleet[k].x,GS.fleet[k].y)
                print("Agent %d. ID = %s. State = %s. Target = %s. Position = %s"%(k,GS.fleet[k].identifier,GS.fleet[k].state,target,position))
        GS.update_neighbors()
        GS.update_positions()

        if i % reduce == 0:
            GS.update_pattern()

    trajectories = GS.return_trajectories()
    states = GS.return_states()
    trajectories = trajectories[:,range(0,num_steps,reduce),:]
    states = states[:,range(0,num_steps,reduce)]
    #patterns = GS.pattern_log[0:num_steps:reduce]
    patterns = GS.pattern_log

    #%% Plotting

    fig, ax = plt.subplots(figsize=[10, 10])
    ax.set_xlim(-axlim, axlim)
    ax.set_ylim(-axlim, axlim)

    cmap = {State.IDLE:"green",State.DRIVING:"orange",State.CONSENSUS:"red"}

    def init():
        ax.clear()

    def animate(j):
        ax.clear()

        # plot drones
        for i in range(len(fleet)):
            ax.plot(trajectories[i, j, 0], trajectories[i, j, 1],marker="o",label="Drone: "+str(i), color = cmap[states[i,j]])
            #ax.plot(GS.fleet[i].x, GS.fleet[i].y, marker="o", label="Drone: "+str(i), color = cmap[GS.fleet[i].state])

        # plot pattern
        patterns[j].visualize(ax)

        ax.set_xlim(-axlim, axlim)
        ax.set_ylim(-axlim, axlim)
        plt.xlabel("$x$ position")
        plt.ylabel("$y$ position")

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(trajectories[0]), repeat = True)

    print("Saving animation")
    #%% save animation
    f = r"trajectories2.mp4"
    writervideo = animation.FFMpegWriter(fps=1/(reduce*t))
    anim.save(f, writer=writervideo)

    print("--- %s seconds ---" % (time.time() - start_time))
