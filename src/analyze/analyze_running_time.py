import matplotlib.pyplot as plt
import numpy as np
result_path = ["D:\\Github\\optimization_picking_in_warehouse\\src\\csv\\CSP_(actually_TSP_CPSAT_reference).csv","D:\\Github\\optimization_picking_in_warehouse\\src\\csv\\GA_10_100.csv","D:\\Github\\optimization_picking_in_warehouse\\src\\csv\\Heuristic_10_100_inkali.csv","D:\\Github\\optimization_picking_in_warehouse\\src\\csv\\Nearest_neighbor_10_100.csv"]
#result_path = ["D:\\Github\\optimization_picking_in_warehouse\\src\\csv\\Heuristic_10_100_inkali.csv"]
n_types_of_goods = []
m_shelves = []
success_tests = []
fail_tests = []
run_time = []
minimum_distance = []
N_M = ["N=20,M=10","N=100,M=50","N=200,M=100","N=400,M=200","N=1000,M=500","N=2000,M=1000","N=4000,M=2000"]
#get data
for path in result_path:
    with open(path,"r") as f:
        _n_types_of_goods = []
        _m_shelves = []
        _run_time = []
        _minimum_distance = []
        _number_of_nodes = []
        remove_fails = []
        data = f.readlines()
        data.pop(0)
        for line in data:
            values = line.strip().split(",")
            #print(values)
            _n_types_of_goods.append(int(values[0]))
            _m_shelves.append(int(values[1]))
            if "CAN'T" not in line:
                _run_time.append(float(values[5]))
                _minimum_distance.append(int(values[4]))
                _number_of_nodes.append(int(values[6]))
            else:
                _run_time.append(None)
                _minimum_distance.append(None)
                _number_of_nodes.append(None)
        n_types_of_goods.append(_n_types_of_goods)
        m_shelves.append(_m_shelves)
        run_time.append(_run_time)
        success_tests.append(len(remove_fails))
        fail_tests.append(len(data) - len(remove_fails))
        minimum_distance.append(_minimum_distance)
#run_time[2].append(None)
print(run_time)
#print(n_types_of_goods)
#print(m_shelves)
#N_M_20_10,N_M_100_50,N_M_200_100,N_M_400_200,N_M_1000_500,N_M_2000_1000,N_M_4000_2000 = [],[],[],[],[],[],[]
#for i in range(len(minimum_distance)):
#    N_M_20_10.append(minimum_distance[i][0])
#    N_M_100_50.append(minimum_distance[i][1])
#    N_M_200_100.append(minimum_distance[i][2])
#   N_M_1000_500.append(minimum_distance[i][4])
#    N_M_2000_1000.append(minimum_distance[i][5])
#   N_M_4000_2000.append(minimum_distance[i][6])
CSP,GA,Heuristic,Nea_Neig = run_time[0],run_time[1],run_time[2],run_time[3]
'''
for i in range(CSP.count(None)):
    CSP.remove(None)
    CSP.append(0)
#print(CSP)
for i in range(GA.count(None)):
    GA.remove(None)
    GA.append(0)
for i in range(Nea_Neig.count(None)):
    Nea_Neig.remove(None)
    Nea_Neig.append(0)
for i in range(Heuristic.count(None)):
    Heuristic.remove(None)
    Heuristic.append(0)'''
#Compare
fig, ax = plt.subplots(figsize = (16,9))
#ax.plot(minimum_distance[0],'-',label = "CSP")
#ax.plot(minimum_distance[1],'-',label = 'GA')
#ax.plot(minimum_distance[2],'-',label = 'Heuristic')
#ax.plot(minimum_distance[3],'-',label = 'Nearest Neighbors')
x = np.arange(len(N_M))
width = 0.2 #The with of the bar
line1 = ax.plot(x - width/2 ,CSP,label = "CSP")
line2 = ax.plot(x - width/2 ,GA,label = "GA")
line3 = ax.plot(x - width/2 ,Heuristic,label = "Heuristic")
line4 = ax.plot(x - width/2 ,Nea_Neig,label = "Nearest Neighbors")

ax.set_xticks(x + width/2, N_M)
ax.set_xticklabels(N_M)
ax.set_ylabel("Running time")

ax = plt.gca()
ax.set_ylim([0,60])
#ax.set_xlabel("Run Time")
plt.title("Comparing running time between 4 methods")


plt.legend(loc = "upper left")  
fig.tight_layout()
#plt.show()
plt.savefig("D:/Github/optimization_picking_in_warehouse/src/figures/Comparing_running_time_4_methods.png")  

    
