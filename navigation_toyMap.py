#import matplotlib.pyplot as plt
import numpy as np
import picar_4wd as fc
import time

# This is the script using the toy routing map for navigation
# After the ultrosonic scanning and the A_star route finding, you should have a map similar to this toy map that highlights the 
# path in 1 and the rest in 0 in a squared matrix (numpy array)


# Scheme of navigation 
# 1. Give move instruction to the car, move_forward, turn_left or turn_right 
#    based on the location in the path and the current position of the car
# 2. Once the car reaches the "turning" position, the map and path will be updated 
#    by fliping horizontally followed by transpose. 
#    In this way, the relative moving direction of the car will be always horizontal 
#    and the same condition used for deciding moving forwar, turning left or right won't change 
#    by the change of the car orientation. 
# 3. The visted location on the path is removed from the path list as car move along

# Functions that update maze and path
def update_maze(maze):
    return np.transpose(np.flip(maze,1))
def update_location(loc):
    loc_f = np.array([loc[0], maze.shape[1]-loc[1]])
    loc_f_t = np.flip(loc_f)
    return loc_f_t
def update_path(path):
    path_new = []
    for loc in path:
        loc_new = update_location(loc)
        path_new.append(loc_new)
    return np.array(path_new)

# Functions that move the picat forward, left and right
def move_forward(speed = 10):
    fc.forward(speed)
    x = 0
    for i in range(1):
        time.sleep(0.1)
        x += speed * 0.1
    print("%smm"%x)
    fc.stop()

def turn_left(speed = 10):
    fc.turn_left(speed)
    for i in range(15):
        time.sleep(0.1)
    fc.stop()

def turn_right(speed = 10):
    fc.turn_right(speed)
    for i in range(15):
        time.sleep(0.1)
    fc.stop()

def move_instruction(path_arr, maze):
    car_pos = path_arr[0]
    count = 0
    for location in path_arr[1:]:
        if (list(location - car_pos) == [0,1]) or (list(location - car_pos) == [0,-1]):
            print("forward")
            move_forward()
            car_pos = location
            count += 1
        
        elif list(location - car_pos) == [1,0]:
            print("turn right")
            turn_right()
            break
        
        elif list(location - car_pos) == [-1,0]:
            print("turn left")
            turn_left()
            break
        
    maze = update_maze(maze) #flip and transpose maze
    path_arr = update_path(path_arr) #update the locations in the path accoring to the maze update
    #car_pos = path_arr[count] #update the car_pos in the refreshed maze 
    path_arr = path_arr[count:] #remove the passed locations in the path
    return car_pos, path_arr, maze

def main():
    # Build a toy map
    maze = np.zeros([100,100])
    maze[50,:30]=1
    maze[50:70, 30]=1
    maze[70,30:80]=1
    #plt.matshow(maze)

    # Find out the path in the toy map
    path_arr = np.stack((np.where(maze==1)[0], np.where(maze==1)[1]), axis = 1)
    print(path_arr)
    while path_arr.shape[0] > 1:
        #plt.matshow(maze)
        car_pos, path_arr, maze = move_instruction(path_arr, maze)
        print(car_pos)

if __name__ == "main":
    main()
