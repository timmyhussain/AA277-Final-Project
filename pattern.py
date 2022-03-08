
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mpPath

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
    def __init__(self, )

        
# Test out some patterns
if __name__ == "__main__":
    # Circle
    R = 5
    t = np.linspace(0,2*np.pi,10)
    pts = [R * np.cos(t), R* np.sin(t)]

    P = Pattern(pts)

    # visualize
    plt.scatter(P.x, P.y)
    plt.plot(P.x, P.y)
    plt.show()