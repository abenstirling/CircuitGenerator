import numpy as np
from itertools import product

def gen_RCL_matrix(j, n=4, r_min=1, r_max=1000, l_min=1, l_max=1000, c_min=1, c_max=1000):
    '''
    compont matrix [n x n x 3]
    permute all combinations of n elements in the graph
      for all rlc
          all >= 0
          l and c can be both non negative on the same edge

    if no r
        r = inf
    if no c
        c = 0
    if no l
        l= inf
    

    (0, [''])
    (1, ['r'])
    (2, ['c'])
    (3, ['l'])
    (4, ['r', 'c'])
    (5, ['r', 'l'])
    '''
    if n == 3: r = 3
    elif n ==4: r = 6
    products = list(map(list,product(range(6),repeat=r)))
    # print(len(products))
    # print(f"products: ")
    # for i,p in enumerate(products):
    #     print(i,p)

    dim = int(n*(n-1)/2)  # Number of elements in the array
    RCL_arr = np.zeros((dim, 3))

    open_circuit = np.array([np.inf,0,np.inf])
    r_open = np.inf
    c_open = 0.0
    l_open = np.inf
    
    #print(products[j])
    for i,components in enumerate(products[j]):
        # print(f"components: {components}")
        if components == 0:
            RCL_arr[i,:] = open_circuit
            # print("open circuit")
        elif components == 1:
            vals = np.array([np.random.uniform(r_min,r_max), c_open, l_open])
            # print(1,vals)
            RCL_arr[i,:] = vals
        elif components == 2:
            vals = np.array([r_open, np.random.uniform(c_min,c_max), l_open])
            # print(2,vals)
            RCL_arr[i,:] = vals
        elif components == 3:
            vals = np.array([r_open, c_open, np.random.uniform(l_min,l_max)])
            # print(3,vals)
            RCL_arr[i,:] = vals
        elif components == 4:
            vals = np.array([np.random.uniform(r_min,r_max), np.random.uniform(c_min,c_max), l_open])
            # print(4,vals)
            RCL_arr[i,:] = vals
        elif components == 5:
            vals = np.array([np.random.uniform(r_min,r_max), c_open, np.random.uniform(l_min,l_max)])
            # print(5,vals)
            RCL_arr[i,:] = vals

    # print(f"RCL_arr: {RCL_arr}")
    out_matrix = np.zeros((n,n,3))
    j=0
    for i in range(n-1):
        # print(f"len vec: {len(RCL_arr[j:n-1-i])}")
        # print(f"len mat: {len(out_matrix[i,i+1:,:])}")
        # print(f"shape vec: {RCL_arr[j:n-1-i].shape}")
        # print(f"shape mat: {out_matrix[i,i+1:,:].shape}")
        # print()
        out_matrix[i,i+1:,:] = RCL_arr[j:n-1-i+j]
        j += n-1-i
    
    return out_matrix

