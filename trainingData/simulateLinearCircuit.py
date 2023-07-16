import lcapy as lc
import matplotlib.pyplot as plt
import numpy as npy



def simulateCircuitMatrix(componentMatrix, tStop, time_step):
    # component matrix is n x n x 3 of [R, C, L]
    # tStop is stop time in seconds
    # sample rate is dt in seconds
    # returns n x 1 array of voltage vs time in response to step function

    netlist = generateNetlistFromCompMatrix(componentMatrix)
    response = simulateStepResponse(netlist, tStop, time_step)

def genComplexMatrix(componentMatrix,a):
    inSize = npy.shape(componentMatrix)
    complexMatrix = npy.zeros([inSize[0], inSize[1], 2])
    for row in range(inSize[0]):
        for col in range(inSize[1]):
            complexMatrix[row,col,:] = get2MatrixFromComponent(componentMatrix[row,col,:],a)
    return complexMatrix

def genComponentMatrix(complexMatrix, a):
    inSize = npy.shape(complexMatrix)
    componentMatrix = npy.zeros([inSize[0], inSize[1], 3])
    for row in range(inSize[0]):
        for col in range(inSize[1]):
            componentMatrix[row,col,:] = getComponentFrom2Matrix(complexMatrix[row,col,:],a)
    return componentMatrix

def getComponentFrom2Matrix(x,a):
    # scaling factor
    if(x[0] == 1):
        R = npy.inf
    else:
        temp1 = a*npy.log((1+x[0])/(1-x[0]))
        R = temp1
    if(x[1] == 0.5):
        L = 0
        C = 0
    elif(x[1] == 0):
        L = npy.inf
        C = 0
    elif(x[1] == 1):
        L = npy.inf
        C = 0
    else:
        temp2 = a*npy.log(x[1]/(1-x[1]))
        C = L = 0;
        if(temp2 > 0):
            L = temp2
            C = 0;
        elif(temp2 < 0):
            C = -1/temp2
            L = npy.inf
    return [R, C, L]

def get2MatrixFromComponent(component,a):
    # component is (R,C,L) in units of kOhm, uF, uH
    R = component[0]
    C = component[1]
    L = component[2]
    if(C != 0 and L != npy.inf):
        # can't have both L and  C between nodes
        print("Can't have both L and C on the same node!!!")
    if(R == npy.inf):
        x1 = 1
    else:
        temp1 = npy.exp(R/a)
        x1 = (temp1-1)/(temp1+1)
    temp2 = 0
    if(C == 0 and L == npy.inf):
        x2 = 1;
    else:
        if(C == 0 and L != npy.inf):
            temp2 = L
        elif(C != 0 and L == npy.inf):
            temp2 = -1/C
        x2 = 1/(1+npy.exp(-temp2/a))
    return [x1, x2]

def generateNetlistFromCompMatrix(X):
    matrixSize = X.shape
    num_nets = matrixSize[1]
    netlist = ''
    for i in range(num_nets):
        for j in range(i+1,num_nets):
            R = npy.real(X[i, j, 0])
            C = npy.real(X[i, j, 1])
            L = npy.real(X[i, j, 2])
            node1 = f'N{i+1}'
            if(j == num_nets-1):
                node2 = '0'
            else:
                node2 = f'N{j+1}'
            if(C != 0 and L != npy.inf):
                print("L and C cannot both be present!")
            if(R != npy.inf):
                component_name = f'R{i+1}{j+1}'
                netlist += f"{component_name} {node1} {node2} {R}\n"
            if(C != 0):
                component_name = f'C{i+1}{j+1}'
                netlist += f"{component_name} {node1} {node2} {C*1e-6} 0 \n"
            if(L != npy.inf):
                component_name = f'L{i+1}{j+1}'
                netlist += f"{component_name} {node1} {node2} {L*1e-6} 0 \n"

    # add step voltage source
    netlist += f"V1 N1 0 step 1\n"
    #netlist += f"R0 N3 0 0"

    print(netlist)
    return netlist

def simulateStepResponse(netlist, duration=1, time_step = 0.001):
    # Create the circuit from the netlist
    circuit = lc.Circuit(netlist)
    #print(circuit)
    # circuit.draw();
    # Define the step input
    #Vstep = lc.StepVoltageSource('Vstep', initial_value=0, final_value=1, pulse_width=duration)

    # Add the step input to the circuit
    #circuit.add_source(Vstep)

    # Set the end time and number of points for simulation
    # circuit.draw()
    #circuit.set_end_time(duration)
    num_points = duration/time_step + 1;
    #circuit.set_num_samples(num_points)
    timeEval = npy.linspace(0, duration, round(num_points))

    # Perform the simulation
    response = circuit.sim(timeEval)  # 'N' refers to the node name

    # Extract the time and output voltage arrays
    #t = response
    #Vout = response['N']

    # Plot the step response
    #print(response.N2.v)
    #plt.plot(timeEval, response.N2.v)
    #plt.xlabel('Time')
    #plt.ylabel('Output Voltage')
    #plt.title('Step Response')
    #plt.grid(True)
    #plt.show()
    return response.N2.v

testMatrix = npy.zeros((3,3,3))
testMatrix[:,:,0] = npy.inf
testMatrix[:,:,1] = 0
testMatrix[:,:,2] = npy.inf
testMatrix[0,1,:] = [10, 1, npy.inf]
testMatrix[1,2,:] = [npy.inf, 0, 50]

testMatrix2 = genComplexMatrix(testMatrix,100)
testMatrix3 = genComponentMatrix(testMatrix2,100)
print(testMatrix)
print(testMatrix2)
print(testMatrix3)
#print(testMatrix)
#simulateCircuitMatrix(testMatrix3, 1e-3, 1e-6);
