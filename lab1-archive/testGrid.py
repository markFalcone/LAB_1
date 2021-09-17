import numpy as np

N = 10

def build_mat(N):
 

    mat = np.zeros(N*N)
   

    return mat.reshape((N,N))

mat = build_mat(N)
print(mat)
