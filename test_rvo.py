
from code import Drone, GhostServer, Shape
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

    d1 = Drone(-5,-1,0,"")
    d2 = Drone(-6,1,1,"")
    d3 = Drone(-7,1,2,"")
    d4 = Drone(-8,-1,3,"")

    fleet = [d1,d2,d3,d4]

    pattern = Shape(np.array([[-1,-1,1,1],[-1,1,1,-1]]).transpose())

    GS = GhostServer(fleet,[],max_dist=2.5)

    GS.update_pattern(pattern)
    GS.update_neighbors()
    cmap = {0:"blue", 1: "red", 2: "green", 3: "black"} #for plotting

    #%% Simulation loop
    for i in range(200):
        print("Iteration %d"%i)
        for k in range(len(fleet)):
            print("Agent %d. ID = %s. State = %s. ConsVar = %.3f"%(k,GS.fleet[k].identifier,GS.fleet[k].state,GS.fleet[k].cons_var))
        GS.update_neighbors()
        GS.update_positions()

    trajectories = GS.return_trajectories()
    quit()
    #%% Plotting

    # for i in range(len(fleet)):
    #     plt.plot(trajectories[i, :, 0], trajectories[i, :, 1], label="Drone: "+str(i))

    fig, ax = plt.subplots(figsize=[10, 10])
    ax.set_xlim(-10, 2)
    ax.set_ylim(0, 2)
    # data = np.array([o.reshape(o.shape[1], -1) for o in outputs])
    # sns.heatmap(data[0], vmax=1, square=True)
    # plt.scatter(0, 1, s=100)
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
