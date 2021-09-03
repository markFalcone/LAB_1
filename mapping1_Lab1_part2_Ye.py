import picar_4wd as fc
import numpy as np
import time

angleList = np.arange(-60,60,30)

def get_coord_at(angle):
    dist = fc.get_distance_at(angle)
    x = int(dist * np.sin(dist))
    y = int(dist * np.cos(dist))
    print(dist)
    return x, y

def mapping(angleList):
    x_coords = []
    y_coords = []
    for angle in angleList:
        x, y = get_coord_at(angle)
        x_coords.append(x)
        y_coords.append(y)
    x_coords = np.array(x_coords)
    y_coords = np.array(y_coords)
    #print(x_coords)
    #print(y_coords)

    x_min = np.min(x)
    x_max = np.max(x)
    y_min = np.min(y)
    y_max = np.max(y)
    #print(x_min, x_max, y_min, y_max)
    car_x = 0
    car_y = 0
    if x_min < 0:
        shift = -x_min
        car_x += shift
        x_coords += shift
        x_min = np.min(x_coords)
        x_max = np.max(x_coords)
    #print(shift)
    if y_min <0 or y_max < 0:
        print("error!")
    #print(x_min, x_max, y_min, y_max, car_x, car_y)
	
	    if car_x > x_max:
        car_map = np.zeros(car_x - x_min + 1, y_max + 1)
    else:
        car_map = np.zeros(x_max - x_min + 1, y_max + 1)


    for i in x_coords:
        for j in y_coords:
            car_map[i,j] = 1

    print(car_map)
    return car_map


if __name__ == "__main__":
    mapping(angleList)


