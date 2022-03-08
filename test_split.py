from code import *
from pattern import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mpPath
import matplotlib.patches as patches

from code import Drone, GhostServer, State

# parameters
t = 0.01
num_steps = 2000
num_agents = 20
reduce = 10
init_bounds = 2

N = 100

c0 = np.array([0,0])
cf = np.array([5,0])
w0 = np.array([1,1])
wf = np.array([1.5,1.75])
patterns = []
for i in range(N):
    c = c0 + (cf-c0)*i/N
    w = w0 + (wf-w0)*i/N
    verts = np.array([[c[0]-w[0],c[0]-w[0],c[0]+w[0],c[0]+w[0]],[c[1]-w[1],c[1]+w[1],c[1]+w[1],c[1]-w[1]]]).T
    patterns.append(Pattern([verts]))

c0 = cf
w0 = wf
c1f = np.array([7,0])
c2f = np.array([10,2])
c3f = np.array([10,-2])
for i in range(N):
    c = c0 + (c1f-c0)*i/N
    c1 = c0 + (c2f-c0)*i/N
    c2 = c0 + (c3f-c0)*i/N
    w = w0
    w1 = w
    w2 = w
    v1 = np.array([[c[0]-w[0],c[0]-w[0],c[0],c[0]],[c[1]-w[1],c[1]+w[1],c[1]+w[1],c[1]-w[1]]]).T
    v2 = np.array([[c1[0],c1[0],c1[0]+w1[0],c1[0]+w1[0]],[c1[1],c1[1]+w1[1],c1[1]+w1[1],c1[1]]]).T
    v3 = np.array([[c2[0],c2[0]+w2[0],c2[0]+w2[0],c2[0]],[c2[1],c2[1],c2[1]-w2[1],c2[1]-w2[1]]]).T
    patterns.append(Pattern([v1,v2,v3]))


fleet = []
GS = GhostServer(fleet,[],patterns[0],max_dist=10)
GS.init_fleet(num_agents, init_bounds)

GS.update_neighbors()

# Simulation loop
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

# Plotting
fig,ax = plt.subplots(figsize=[7,4])
cmap = {State.IDLE:"green",State.DRIVING:"orange",State.CONSENSUS:"red"}
def animate(j):
    ax.clear()
    # plot drones
    for i in range(len(fleet)):
        ax.plot(trajectories[i, j, 0], trajectories[i, j, 1],marker="o",label="Drone: "+str(i), color = cmap[states[i,j]])
    # path = patterns[j].path
    # ax.add_patch(patches.PathPatch(path,facecolor='blue',alpha=0.2,lw=0))
    patterns[j].visualize(ax)
    ax.set_xlim(-2,12)
    ax.set_ylim(-4,4)

anim = animation.FuncAnimation(fig,animate,frames=len(patterns),repeat=True)
#plt.show()

print("Saving animation...")
f = r"test_split.mp4"
writervideo = animation.FFMpegWriter(fps = 50)
anim.save(f,writer=writervideo)


