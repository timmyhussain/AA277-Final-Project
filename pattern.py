
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mpPath
from matplotlib import animation
import matplotlib.patches as patches

class Shape:
    def __init__(self, vertices, update_rule='STATIC'):
    
        self.update_rule = update_rule # possible options = 'STATIC','TRANSLATE','EXPAND'
        self.path = mpPath.Path(vertices)
        self.vertices = self.path.vertices # np array
        m,d = vertices.shape
        if d != 2:
            raise Exception("Expected vertices to have shape (m,2)")

        # Parameters
        self.dx = 1e-3; self.dy = 1e-3 # for translation
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
        patch = patches.PathPatch(self.path, facecolor='orange', alpha = 0.2, lw=0)
        ax.add_patch(patch)


class Pattern:
    """
    Pattern defined by a collection of shapes (each defined by boundary points)
    """
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
    """
    Pattern set induced by point light source casting shadows
    """
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