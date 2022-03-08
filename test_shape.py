from code import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mpPath
import matplotlib.patches as patches

def create_blob(rad_fun,N,c=np.array([0,0])):

    theta = np.array(np.linspace(0,2*np.pi,N))
    x = rad_fun(theta) * np.cos(theta) + c[0]
    y = rad_fun(theta) * np.sin(theta) + c[1]
    
    verts = np.array([x,y]).T
    return verts

N = 100
R = 3

objs = []
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


fig,ax = plt.subplots(figsize=[6,6])
def init():
    ax.clear()
def animate(j):
    ax.clear()
    for i in range(len(objs[0])):
        ax.add_patch(patches.PathPatch(mpPath.Path(objs[j][i]),facecolor='blue',alpha=0.2,lw=0))
    ax.set_xlim(-10,10)
    ax.set_ylim(-10,10)

anim = animation.FuncAnimation(fig,animate,init_func=init,frames=len(objs),repeat=True)
plt.show()
