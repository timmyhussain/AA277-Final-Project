
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mpPath
from matplotlib import animation
import matplotlib.patches as patches

from code import Shape

class Pattern:
    '''
    Pattern defined by a collection of shapes (each defined by boundary points)
    '''
    def __init__(self, vert_array):
        self.num_shapes = len(vert_array)
        paths = [None] * self.num_shapes

        for i in range(self.num_shapes):
            paths[i] = mpPath.Path(vert_array[i])
        
        self.path = mpPath.Path.make_compound_path(*paths)

    # Pattern dynamics
    def update(self):
        # randomly oscillate point(s) sinusoidally
        # (for now just do the first point)
        #self.x += 

        # simple translation
        self.x += 0.1
        self.y += 0.1



class ShadowPattern:
    '''
    Pattern set induced by point light source casting shadows
    '''
    def __init__(self):
        pass

        
# Test out some shapes and patterns
if __name__ == "__main__":
    # Circle
    R = 5; t = np.linspace(0,2*np.pi,10)
    V = np.array([R * np.cos(t), R* np.sin(t)])
    P = Shape(V.T, 'EXPAND')

    # Non-convex (star shape)
    V = [(5,0), 
         (1,1),
         (0,5),
         (1,-1),
         (0,-5),
         (-1,-1),
         (-5,0),
         (-1,1)]

    # visualize
    num_iters = 20
    fig, ax = plt.subplots()
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)

    def init():
        ax.clear()

    def animate(j):
        ax.clear()
        P.update()
        P.visualize(ax)
        ax.set_xlim(-6, 6)
        ax.set_ylim(-6, 6)
        plt.xlabel("$x$ position")
        plt.ylabel("$y$ position")

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=num_iters, repeat = True)

    plt.show()