import numpy as np
import matplotlib.pyplot as plt
import time

import os
import pickle

import cProfile
import pstats

import threading


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


directory = "pickled_X_y"
if not os.path.exists(directory):
    os.makedirs(directory)




def main(seed,n_samples=200):
    np.random.seed(seed)

    start_time = time.time()
    for i in range(n_samples):
        rint = np.random.randint(46000)
        component_matrix = gen_RCL_matrix(rint)
        # print(f"component_matrix")
        # print(component_matrix)
        # print()

        try:
            sig_response = simulateCircuitMatrix(componentMatrix=component_matrix,
                                        t_stop=1.023E-3,
                                        dt=1E-6)
        except:
            continue

        complex_matrix = genComplexMatrix(component_matrix, 300)

        # component_matrix_reverse = genComponentMatrix(complex_matrix, 300)

        # check = component_matrix_reverse == component_matrix
        # print(f"diff: {np.abs(component_matrix_reverse - component_matrix)}")
        # print(f"Check:\n {check}")
        # print(f"comp_reverse: {component_matrix_reverse}")
        # print(f"comp: {component_matrix}")

        file_path = os.path.join(directory, f"{i+seed}X.pkl")  # Specify the file path
        with open(file_path, "wb") as file:
            pickle.dump(sig_response, file)

        file_path = os.path.join(directory, f"{i+seed}y.pkl")  # Specify the file path
        with open(file_path, "wb") as file:
            pickle.dump(complex_matrix, file)
        print(i)
    

    end_time = time.time()

    execution_time = end_time - start_time

    print(f"execution time: {execution_time}")

    #plt.plot(sig_response, label="sig")
    #plt.show()

# ---------------------------------------------------------------------------

num_threads = 4
start_seed = 0

# Start worker threads
threads = []
for i in range(num_threads):
    seed_offset = 100
    seed = start_seed + (seed_offset * i)
    thread = threading.Thread(target=main, args=(seed,))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()






def print_contents(path):
    with open(path, "rb") as file:
        loaded_data = np.array(pickle.load(file))
    print("Loaded array:", loaded_data)
    print(loaded_data.size)
    print(loaded_data.shape)

# print_contents("pickled_samples/0.pkl")
# print()
# print_contents("pickled_samples/00.pkl")




# profiler = cProfile.Profile()
# profiler.enable()
# main()
# profiler.disable()

# stats = pstats.Stats(profiler).sort_stats('time')
# stats.print_stats() 