import picar_4wd as fc
import numpy as np
import math
import time
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')

angleList = np.arange(-60,60,10)
routeMap = np.zeros((200,100))
carPos = [100, 0]

def get_coord_at(angle):
    dist = fc.get_distance_at(angle)
    x = int(dist * np.sin(math.radians(angle))) + carPos[0]
    y = int(dist * np.cos(math.radians(angle))) + carPos[1]
   # print(dist)
    return x, y

def mapping(angleList):
    x_coords = []
    y_coords = []
    for angle in angleList:
        x, y = get_coord_at(angle)
        x_coords.append(x)
        y_coords.append(y)
   # x_coords = np.array(x_coords)
   # y_coords = np.array(y_coords)
   # print(x_coords)
   # print(y_coords)


    for i in x_coords:
        for j in y_coords:
            routeMap[i,j] = 1
    print(routeMap)
    return routeMap

def plot_map(routeMap):
    plt.matshow(routeMap)
    plt.show()

if __name__ == "__main__":
    mapping(angleList)
