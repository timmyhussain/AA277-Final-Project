
from code import Drone, GhostServer, Shape, State
from enum import Enum
import matplotlib.pyplot as plt
import matplotlib.path as mpPath
import numpy as np
from matplotlib import animation
import matplotlib
args = {"size": 20}
matplotlib.rc("font", **args)

if __name__ == "__main__":
    #%% Initialization

    t = 0.01
    num_steps = 600
    num_agents = 20

    pattern = Shape(np.array([[-1,-1,1,1],[-1,1,1,-1]]).transpose())

    fleet = []
    np.random.seed(1)
    for i in range(num_agents):
        x = 2*np.random.random()
        y = 2*np.random.random()
        fleet.append(Drone(x,y,i))

    GS = GhostServer(fleet,[],max_dist=2.5)

    GS.update_pattern(pattern)
    GS.update_neighbors()

    #%% Simulation loop
    for i in range(num_steps):
        if i%25 == 0:
            print("Iteration %d"%i)
            for k in range(len(fleet)):
                target = "None"
                if i > 1 and GS.fleet[k].state != State.CONSENSUS:
                    target = "(%.3f,%.3f)"%(GS.fleet[k].target_x,GS.fleet[k].target_y)
                position = "(%.3f,%.3f)"%(GS.fleet[k].x,GS.fleet[k].y)
                print("Agent %d. ID = %s. State = %s. Target = %s. Position = %s"%(k,GS.fleet[k].identifier,GS.fleet[k].state,target,position))
        GS.update_neighbors()
        GS.update_positions()

    trajectories = GS.return_trajectories()
    states = GS.return_states()
    reduce = 10
    trajectories = trajectories[:,range(0,num_steps,reduce),:]
    states = states[:,range(0,num_steps,reduce)]
    #%% Plotting

    fig, ax = plt.subplots(figsize=[10, 10])
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)

    cmap = {State.IDLE:"green",State.DRIVING:"orange",State.CONSENSUS:"red"}

    def init():
        ax.clear()

    def animate(j):
        ax.clear()

        # plot drones
        for i in range(len(fleet)):
            ax.plot(trajectories[i, j, 0], trajectories[i, j, 1],marker="o",label="Drone: "+str(i), color = cmap[i])

        # plot pattern
        pattern.visualize(ax)

        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        plt.xlabel("$x$ position")
        plt.ylabel("$y$ position")

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(trajectories[0]), repeat = True)

    print("Saving animation")
    #%% save animation
    f = r"trajectories2.mp4"
    writervideo = animation.FFMpegWriter(fps=1/(reduce*t))
    anim.save(f, writer=writervideo)
