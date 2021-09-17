import picar_4wd as fc
import numpy as np
import math
import time
import matplotlib
import matplotlib.pyplot as plt

#matplotlib.use('Agg')

angles = np.arange(-60,60,2)
routeMap = np.zeros((200,200))
carPos = [50, 0]

def get_coord_at(angles, carPos):
    x_coords = []
    y_coords = []
    for a in angles:
        dist = fc.get_distance_at(a)
        if dist == -2:
            continue
        else:
            x = int(dist * np.sin(math.radians(a))) + carPos[0]
            y = int(dist * np.cos(math.radians(a))) + carPos[1]
        x_coords.append(x)
        y_coords.append(y)
        time.sleep(0.01)
   # print(dist)
    return x_coords, y_coords

def mapping(angles, carPos):
    x_coords, y_coords = get_coord_at(angles, carPos)
    for x,y in zip(x_coords, y_coords):
            routeMap[x,y] = 1
    routeMap[carPos[0], carPos[1]] = 1
    print(routeMap)
    np.save('routeMap.npy', routeMap)


    plt.matshow(routeMap)
	plt.show()
   #mat.pyplot.savefig("routemap.png")
    return routeMap

if __name__ == "__main__":
    mapping(angles, carPos)


