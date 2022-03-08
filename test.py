from code import Drone, GhostServer
from pattern import Shape
import matplotlib.pyplot as plt
import matplotlib.path as mpPath
import numpy as np

d1 = Drone(-1,-1,0,"")
d2 = Drone(-1,1,1,"")
d3 = Drone(1,1,2,"")
d4 = Drone(1,-1,3,"")

fleet = [d1,d2,d3,d4]

pattern = Shape(np.array([[-1,-1,1,1],[-1,1,1,-1]]).transpose())

GS = GhostServer(fleet,[],max_dist=2.5)

GS.update_pattern(pattern)
GS.update_neighbors()

for k in range(50):
    print("Iteration %d"%k)
    for i in range(len(fleet)):
        print("Agent %d. ID = %s. State = %s"%(i,GS.fleet[i].identifier,GS.fleet[i].state))
        #print("Agent %d. State = %s. Cons = %.3f"%(i,GS.fleet[i].state,GS.fleet[i].cons_var))
    GS.update_neighbors()
    GS.update_positions()
    print()
