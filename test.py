from code import Drone, GhostServer
import matplotlib.pyplot as plt
import numpy as np

d1 = Drone(-1,-1,0,"")
d2 = Drone(-1,1,1,"")
d3 = Drone(1,1,2,"")
d4 = Drone(1,-1,3,"")

fleet = [d1,d2,d3,d4]
targets = {0:(1,1),1:(1,-1),2:(-1,-1),3:(-1,1)}
GS = GhostServer(fleet,targets,max_dist=2.5)

GS.update_neighbors()
GS.update_targets()

for k in range(50):
    print("Iteration %d"%k)
    for i in range(len(fleet)):
        print("Agent %d. ID = %s. State = %s"%(i,GS.fleet[i].identifier,GS.fleet[i].state))
        #print("Agent %d. State = %s. Cons = %.3f"%(i,GS.fleet[i].state,GS.fleet[i].cons_var))
    GS.update_neighbors()
    GS.update_positions()
    print()
