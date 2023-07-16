import numpy as np
import matplotlib.pyplot as plt
import time

import cProfile
import pstats


from data_functions.simulateLinearCircuit import genComplexMatrix
from data_functions.simulateLinearCircuit import genComponentMatrix
from data_functions.simulateLinearCircuit import simulateCircuitMatrix

from data_functions.generate_RCL_matrix import gen_RCL_matrix


# rint = np.random.randint(10)
# print(rint)
# component_matrix = gen_RCL_matrix(rint)
# # print(component_matrix.shape)
# print(component_matrix)
# 
# sig_response = simulateCircuitMatrix(componentMatrix=component_matrix,
#                                      t_stop=1.023E-3,
#                                      dt=1E-6)
# print(len(sig_response))

def main(n_samples):

    samples = np.array(n_samples,4,4,3)

    start_time = time.time()

    for i in range(n_samples):
        rint = np.random.randint(46000)
        component_matrix = gen_RCL_matrix(rint)
        try:
            sig_response = simulateCircuitMatrix(componentMatrix=component_matrix,
                                        t_stop=1.023E-3,
                                        dt=1E-6)
        except:
            continue
    

    end_time = time.time()

    execution_time = end_time - start_time

    print(f"execution time: {execution_time}")

    #plt.plot(sig_response, label="sig")
    #plt.show()

    execution_time = end_time - start_time


main()


# profiler = cProfile.Profile()
# profiler.enable()
# main()
# profiler.disable()

# stats = pstats.Stats(profiler).sort_stats('time')
# stats.print_stats() 