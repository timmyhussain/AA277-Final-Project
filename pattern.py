
import numpy as np
import matplotlib.pyplot as plt

class Pattern:
    '''
    Pattern defined by a set of boundary points
    '''
    def __init__(self, points):
        self.p = points
        self.center = np.mean(points, axis=1)
        self.x = points[0][:]
        self.y = points[1][:]

    # Pattern dynamics
    def update(self):
        # randomly oscillate point(s) sinusoidally
        # (for now just do the first point)
        #self.x += 

        # simple translation
        self.x += 0.1
        self.y += 0.1
        
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