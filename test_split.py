from code import *
from pattern import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mpPath
import matplotlib.patches as patches

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

fig,ax = plt.subplots(figsize=[7,4])
def animate(j):
    ax.clear()
    path = patterns[j].path
    ax.add_patch(patches.PathPatch(path,facecolor='blue',alpha=0.2,lw=0))
    ax.set_xlim(-2,12)
    ax.set_ylim(-4,4)

anim = animation.FuncAnimation(fig,animate,frames=len(patterns),repeat=True)
plt.show()
'''
print("Saving animation...")
f = r"test_split.mp4"
writervideo = animation.FFMpegWriter(fps = 50)
anim.save(f,writer=writervideo)
'''

