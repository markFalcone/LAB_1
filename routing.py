import matplotlib.pyplot as plt
import numpy as np
from warnings import warn
import heapq

from scipy.spatial import Voronoi, voronoi_plot_2d
import picar_4wd as fc
import math, time, sys, tty
import collections

# Credit for this: Nicholas Swift
# as found at https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2

class Node:
    """
    A node class for A* Pathfinding
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
    
    def __repr__(self):
        return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

    # defining less than for purposes of heap queue
    def __lt__(self, other):
        return self.f < other.f
    
    # defining greater than for purposes of heap queue
    def __gt__(self, other):
        return self.f > other.f

def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Return reversed path


def astar(maze, start, end, allow_diagonal_movement = False):
    """
    Returns a list of tuples as a path from the given start to the given end in the given maze
    :param maze:
    :param start:
    :param end:
    :return:
    """

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Heapify the open_list and Add the start node
    heapq.heapify(open_list) 
    heapq.heappush(open_list, start_node)

    # Adding a stop condition
    outer_iterations = 0
    max_iterations = (len(maze[0]) * len(maze) // 2)

    # what squares do we search
    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0))
    if allow_diagonal_movement:
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1),)

    # Loop until you find the end
    while len(open_list) > 0:
        outer_iterations += 1

        if outer_iterations > max_iterations:
          # if we hit this point return the path such as it is
          # it will not contain the destination
            warn("giving up on pathfinding too many iterations")
            return return_path(current_node)       
        
        # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            return return_path(current_node)

        # Generate children
        children = []
        
        for new_position in adjacent_squares: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            # Child is on the closed list
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            if len([open_node for open_node in open_list if child.position == open_node.position and child.g > open_node.g]) > 0:
                continue

            # Add the child to the open list
            heapq.heappush(open_list, child)

    warn("Couldn't get a path to destination")
    return None
	
	# Use kernel to thicken the obstacle
def obstacle_clearance(routeMap, kernel_size = 5):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    maze = cv2.dilate(routeMap, kernel)
    return maze
	
	# draw the path found by A* algo
def draw_path(maze, path):
    maze = np.array(maze)
    for ind in path:
        maze[ind[0], ind[1]] = 4
    plt.matshow(maze)
    
def angle_distance():
    x = np.array([0])
    y = np.array([0])
    for deg in range(-90,90,5):
        print('the degree is',(deg), 'and the distence is:', fc.get_distance_at(deg))
        dist =fc.get_distance_at(deg)
        if dist == -2:
            #dist = 100
            continue
        rad = math.radians(deg)
        y_CORD = math.floor(dist*math.sin(rad))
        
        x_CORD = math.floor(dist*math.cos(rad))
        x= np.append(x,x_CORD)
        y = np.append(y,y_CORD)
        time.sleep(0.1)
    #print(x)
    #print(y)
    #plt.scatter(x,y)
    #plt.show()
    return x,y                                                    
    
def plot(mat, x_cord, y_cord):
    for i in range(x_cord.size):
        if -100 < x_cord[i] <0 or -100 < y_cord[i] <0:
            xArr = 100 - abs(x_cord[i])
            yArr = 100 - abs(y_cord[i])
        if 0 < x_cord[i] <= 100 and 0< y_cord[i] <= 100: 
            xArr = x_cord[i]+100
            yArr = y_cord[i]+100
        #placing a 1 where the x and y cordanates are 
            mat[xArr][yArr] =1
        ##**checking number of 1 and zeros**##
#     print(mat)
#     ua,uind=np.unique(mat,return_inverse=True)
#     count=np.bincount(uind)
#     print(ua)
#     print(count)
    return mat
    
    
def build_mat(N):
#     mat = np.zeros(N*N)
#     mat.reshape((N,N))
#     print(mat.shape)
    mat = np.zeros((N, N))
    # need to add 50 to all x points to align them and eith add or subtract 50 for y
    #mat[1][1] =8
    return mat

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

def move_forward():
    fc.forward(5)
    for i in range(5):
        time.sleep(0.1)
        
    fc.stop()
def move_left():
    fc.stop()
    fc.turn_left(10)
    
    for i in range(10):
        time.sleep(0.1)
    fc.stop()
def move_right():
    fc.stop()
    fc.turn_right(10)
   
    for i in range(10):
        time.sleep(0.1)
    fc.stop()
# In[7]:


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
            move_right()
            break
        
        elif list(location - car_pos) == [-1,0]:
            move_left()
            print("turn left")
            break
        
    maze = update_maze(maze) #flip and transpose maze
    path_arr = update_path(path_arr) #update the locations in the path accoring to the maze update
    #car_pos = path_arr[count] #update the car_pos in the refreshed maze 
    path_arr = path_arr[count:] #remove the passed locations in the path
    return car_pos, path_arr, maze




maze = build_mat(250)
    ## ** Getting distances **##
x,y = angle_distance()

    ## ** Send x and y to be plotted  **#
H = plot(maze, x,y)
    #plt.scatter(H)

kernal = np.array([[0,1,0],[1,1,1],[0,1,0]]) #can change the kernal size and definition 

start = (2, 2)
end = (2, 10)
path_arr = astar(H, start, end)
print(path_arr)
    #draw_path(maze, path, intensity = 2)
car_pos = (2,2)
#while path_arr.shape[0] > 1:
plt.matshow(maze)
move_instruction(path_arr,maze)
#car_pos, path, maze = move_instruction(path_arr, maze)
#print(car_pos)
	
