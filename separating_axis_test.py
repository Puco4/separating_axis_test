import random as rd
import numpy as np
import math 
import time
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def rotation(x, y, theta_R):
    return np.array([ x*math.cos(theta_R) - y*math.sin(theta_R),
             x*math.sin(theta_R) + y*math.cos(theta_R)])

def calculateVerticesRectangle(Center, theta, l, w):
    theta_R = theta/180*math.pi
    Vertices = np.array([
          Center + rotation(w, l, theta_R), 
          Center + rotation(w, -l, theta_R), 
          Center + rotation(-w, -l, theta_R), 
          Center + rotation(-w, l, theta_R) ] )
    return Vertices

def isRectangleACollidingWithRectangleB(Center_A, Vertices_A, Center_B, Vertices_B, R_BoundingCircle, l, w):       
    #1) Bounding circle check
    dAB = math.sqrt( (Center_A[0] - Center_B[0])**2 + (Center_A[1] - Center_B[1])**2 )
    if dAB > 2*R_BoundingCircle:
        return False
    
    #2) Separating axis test
    #Rectangle A
    si_Minus = Vertices_A[3] - Vertices_A[0] 
    for i in range(len(Vertices_A)):
        si_Plus = Vertices_A[(i+1) % 4] - Vertices_A[i]
        ni = [- si_Plus[1], si_Plus[0]]
        sgni = np.sign( np.dot(si_Minus, ni) )

        for j in range(len(Vertices_B)):
            sij = Vertices_B[j] - Vertices_A[i]
            sgnj = np.sign( np.dot(sij, ni) )
            if sgni * sgnj > 0:
                break #Vertex i does not define separating axis
            else:
                if j == 3:
                    return False #Vertex i defines separating axis: no collision
        
        si_Minus = - si_Plus
    
    #Rectangle B
    si_Minus = Vertices_B[3] - Vertices_B[0] 
    for i in range(len(Vertices_B)):
        si_Plus = Vertices_B[(i+1) % 4] - Vertices_B[i]
        ni = [- si_Plus[1], si_Plus[0]]
        sgni = np.sign( np.dot(si_Minus, ni) )

        for j in range(len(Vertices_A)):
            sij = Vertices_A[j] - Vertices_B[i]
            sgnj = np.sign( np.dot(sij, ni) )
            if sgni * sgnj > 0:
                break #Vertex i does not define separating axis
            else:
                if j == 3:
                    return False #Vertex i defines separating axis: no collision
        
        si_Minus = - si_Plus

    return True #There is no separating axis

#MAIN
#Parameters
rd.seed(1)
w = 5
l = 10

#---
R_BoundingCircle = math.sqrt(w**2 + l**2)
start_time = time.time()

for k in range(5):

    Center_A = np.array([rd.uniform(-15, 15), rd.uniform(-15, 15)])
    theta_A = 360*rd.random()
    Vertices_A = calculateVerticesRectangle(Center_A, theta_A, l, w)
    
    Center_B = np.array([rd.uniform(-15, 15), rd.uniform(-15, 15)])  
    theta_B = 360*rd.random()
    Vertices_B = calculateVerticesRectangle(Center_B, theta_B, l, w)
    
    isColliding = isRectangleACollidingWithRectangleB(Center_A, Vertices_A, Center_B, Vertices_B, R_BoundingCircle, l, w)    

    #Figures
    plt.figure(figsize=(5, 5))
    plt.xlim(-50, 50)
    plt.ylim(-50, 50)
    ax = plt.gca()

    plt.plot(Vertices_A[0][0], Vertices_A[0][1], 'bo')
    draw_rect = Rectangle( Vertices_A[2], 2*w, 2*l, theta_A, linewidth=1,edgecolor='b',facecolor='none')
    ax.add_patch(draw_rect)

    plt.plot(Vertices_B[0][0], Vertices_B[0][1], 'ro')
    draw_rect = Rectangle( Vertices_B[2], 2*w, 2*l, theta_B, linewidth=1,edgecolor='r',facecolor='none')
    ax.add_patch(draw_rect)   
    plt.title("Colliding:%r" %isColliding)

print("Time: %s s" % (time.time() - start_time))
