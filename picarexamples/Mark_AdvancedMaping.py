import picar_4wd as fc
import numpy as np
import math, time, sys, tty
from matplotlib import pyplot as plt
import collections
# arr = np.arange(-90,90)

def angle_distance():
    x = np.array([0])
    y = np.array([0])
    for deg in range(-90,90,2):
        print('the degree is',(deg), 'and the distence is:', fc.get_distance_at(deg))
        dist =fc.get_distance_at(deg)
        if dist == -2:
            #dist = 100
            continue
        y_CORD = math.floor(dist*math.sin(deg))
        
        x_CORD = math.floor(dist*math.cos(deg))
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
    


## ** Build Grid **##
mat =build_mat(210)



## ** Getting distances **##
x,y = angle_distance()

## ** Send x and y to be plotted  **#
H = plot(mat, x,y)
#plt.scatter(H)
plt.matshow(H, cmap='Blues')
plt.show()
# plt.imshow(H)
# plt.show()


# x = np.arange(1,11) 
# y = 2 * x + 5 
# plt.title("Matplotlib demo") 
# plt.xlabel("x axis caption") 
# plt.ylabel("y axis caption") 
# plt.plot(x,y) 
# plt.show()