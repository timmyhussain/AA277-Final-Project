
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

def create_blob(rad_fun,N,c=np.array([0,0])):

    theta = np.array(np.linspace(0,2*np.pi,N))
    x = rad_fun(theta) * np.cos(theta) + c[0]
    y = rad_fun(theta) * np.sin(theta) + c[1]
    
    verts = np.array([x,y]).T
    return verts

if __name__ == "__main__":
    #%% Initialization

    start_time = time.time()

    # parameters
    t = 0.01
    num_steps = 2000
    num_agents = 20
    reduce = 10
    axlim = 10
    init_bounds = 5

    # create patterns
    N = int(num_steps / reduce) # num frames
    R = 3

    objs = []
    patterns = []
    c10 = np.array([-8,8])
    c1f = np.array([8,-8])
    c20 = np.array([7.5,6])
    c2f = np.array([5,6])
    c30 = np.array([-5,-8])
    c3f = np.array([-6,8])
    for i in range(N):

        c1 = c10 + (c1f - c10) / N * i
        c2 = c20 + (c2f - c20) / N * i
        c3 = c30 + (c3f - c30) / N * i

        rad_fun1 = lambda t: (R-i/N) + 0.25*np.sin(6*t+4*np.pi*i/N)*np.cos(3*t+4*np.pi*i/N)
        blob1 = create_blob(rad_fun1,100,c1)
        rad_fun2 = lambda t: R - 0.1*t * (t-2*np.pi) / (2*np.pi) + 0.2*np.sin(3*t)*np.cos(5*t)
        blob2 = create_blob(rad_fun2,100,c2)
        rad_fun3 = lambda t: 1.5*R  + 0.5*np.sin(1.5*t)*np.cos(1.5*t)
        blob3 = create_blob(rad_fun3,100,c3)
        objs.append([blob1,blob2,blob3])
        patterns.append(Pattern([blob1,blob2,blob3]))

    fleet = []
    GS = GhostServer(fleet,[],patterns[0],max_dist=10)
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
            GS.set_pattern(patterns[int(i/reduce)])

    trajectories = GS.return_trajectories()
    states = GS.return_states()
    trajectories = trajectories[:,range(0,num_steps,reduce),:]
    states = states[:,range(0,num_steps,reduce)]

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

        # plot pattern
        patterns[j].visualize(ax)

        ax.set_xlim(-axlim, axlim)
        ax.set_ylim(-axlim, axlim)
        plt.xlabel("$x$ position")
        plt.ylabel("$y$ position")

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=N, repeat = True)

    print("Saving animation")
    #%% save animation
    f = r"trajectories2.mp4"
    writervideo = animation.FFMpegWriter(fps=1/(reduce*t))
    anim.save(f, writer=writervideo)

    print("--- %s seconds ---" % (time.time() - start_time))
