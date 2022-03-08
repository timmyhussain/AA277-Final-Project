
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
    num_steps = 500
    num_agents = 8

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
    reduce = 10
    trajectories = trajectories[:,range(0,num_steps,reduce),:]
    print(trajectories.shape)
    #%% Plotting

    # for i in range(len(fleet)):
    #     plt.plot(trajectories[i, :, 0], trajectories[i, :, 1], label="Drone: "+str(i))

    fig, ax = plt.subplots(figsize=[10, 10])
    ax.set_xlim(-8, 2)
    ax.set_ylim(-8, 2)
    # data = np.array([o.reshape(o.shape[1], -1) for o in outputs])
    # sns.heatmap(data[0], vmax=1, square=True)
    # plt.scatter(0, 1, s=100)
    cmap = {}
    for i in range(len(fleet)):
        p = plt.plot(trajectories[i, 0, 0], trajectories[i, 0, 1], label="Drone: "+str(i))
        cmap[i] = p[0].get_color()
        plt.xlabel("$x$ position")
        plt.ylabel("$y$ position")

    def init():
          # sns.heatmap(data[0], vmax=1, square=True, cbar=False)
        for i in range(len(fleet)):
            plt.plot(trajectories[i, 0, 0], trajectories[i, 0, 1], marker="o",label="Drone: "+str(i), color = cmap[i])
        plt.xlabel("$x$ position")
        plt.ylabel("$y$ position")

    def animate(j):
        # sns.heatmap(data[i], vmax=1, square=True, cbar=False)
        for i in range(len(fleet)):
            plt.plot(trajectories[i, j, 0], trajectories[i, j, 1],marker="o",label="Drone: "+str(i), color = cmap[i])
        plt.xlabel("$x$ position")
        plt.ylabel("$y$ position")

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(trajectories[0]), repeat = True)

    print("Saving animation")
    #%% save animation
    f = r"trajectories2.mp4"
    writervideo = animation.FFMpegWriter(fps=1/(reduce*t))
    anim.save(f, writer=writervideo)
