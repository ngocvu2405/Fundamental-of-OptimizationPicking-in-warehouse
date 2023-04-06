# from ortools.sat.python import cp_model
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import time
'''
def data(file):
    #M: shelf
    #N: types of goods
    #Q: matrix of quantity of each type in all shelf
    #q: quantity of each type we need to pick up
    #d: matrix of distance between 2 shelves

    with open(r'{0}'.format(file), 'r') as f:
        first_line = f.readline().split()
        N, M = int(first_line[0]), int(first_line[1])
        Q = []
        d = []
        q = []
        for i in range (1, 1+N):
            type = f.readline().split()
            Q.append(list(int(ele) for ele in type))
        # print(Q)
        for j in range (2+N, 3+N+M):
            dis = f.readline().split()
            d.append(list(int(ele) for ele in dis))
        last_line = f.readline().split()
        for ele in last_line:
            q.append(int(ele))
    return [N, M, Q, d,q]
'''
def data():
   #N: The number of type of product
   #M: The number of shelf
   N, M = [int(i) for i in input().split()]

    # Matrix Q(NxM)
   Q = []
   for i in range(N): # Input N lines (equivalent to N types of product)
       Q.append([int(i) for i in input().split()])

    # Distance matrix
   D = []
   for i in range(M+1): # Input M+1 lines (equivalent to distances between shelf 0,1,2,...,M)
       D.append([int(i) for i in input().split()])

    # Products that need to take
   q = [int(i) for i in input().split()]

   return N, M, Q, D, q

info = data()
# print(i)
N = info[0]
M = info[1]
Q = info[2]
d = info[3]
q = info[4]
# print(N, M, Q, d,q)

def print_solution(info, manager, routing, solution):
    """Prints solution on console."""
    # print(f'Objective: {solution.ObjectiveValue()}')
    total_distance = 0
    # total_load = 0
    index = routing.Start(0)   
    plan_output = 'Route for vehicle 0:\n'
    route_distance = 0
    remain_route_load = info[4] #=q
    path = []

    while not routing.IsEnd(index):
                node_index = manager.IndexToNode(index)
                plan_output += '\n-> {0}\nRemain Load({1})'.format(node_index, remain_route_load)
                path.append(node_index)
                
                if all(ele==0 for ele in remain_route_load):
                    previous_index = index
                    index = 0
                    route_distance +=info[3][previous_index][0]
                    break
                else:
                    previous_index = index
                    index = solution.Value(routing.NextVar(index))
                    route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
                for i in range(info[0]): #contraint 4
                    if remain_route_load[i] > info[2][i][index-1]:
                        remain_route_load[i]= remain_route_load[i] - info[2][i][index-1]
                    else:
                        remain_route_load[i] = 0
    plan_output += '\n-> {0}\nRemain Load({1})\n'.format(manager.IndexToNode(index),
                                                 remain_route_load)
    path.append(manager.IndexToNode(index))
    plan_output += '\nDistance of the route: {}\n'.format(route_distance)
    print(plan_output)
    #total_distance += route_distance
    #path_update = " ".join([str(i) for i in path]).replace(" ","->")
    #print("Path traversed:", path_update)
    #print("Number of nodes: ",len(path))

def CSP():
    global N, M, Q, q, d
    num_vehicles = 1
    depot = 0 #to define start and end point (constraint 1)
    # model = cp_model.CpModel()

    # #initialize variables
    # p = [0 for j in range (M+1)] #picker travel shelf j or not
    # D = 0 #total distance
    # x = [[0 for j in range (M+1)] for i in range (M+1)] #picker travel from shelf i to j or not
    # S = [ele for ele in q] #number of goods of each type needs to pick in journey
    # #init x[i][j]
    
    # for i in range (1, M+1):
    #     for j in range (1, M+1):
    #         if i != j:
    #             x[i][j] = model.NewIntVar(0, 1, 'x[' + str(i) + '][' + str(j) + ']')
    
    # #init p[i]
    # for j in range (1, M+1):
    #     p[j] = model.NewIntVar(0, 1, 'p[' + str(j) + ']')

    # #init S[i]
    # for i in range (N):
    #     S[i] = model.NewIntVar(0, q[i-1], 'S[' + str(i) +']')

    #init D
    # D = model.NewIntVar(0, sum(max(ele) for ele in d[j] for j in range(M+1)), 'D')
    '''Add constraint:
        # 1. The picker must start and end at the gate of warehouse.
        # 2. A shelf is traveled no more than once time.
        # 3. Feasible solution: The total distance is the sum of all journey to pick up all goods he needs
        # 4. When he comes to shelf m, all goods of any types he need at this shelf is picked up.
        # 5. When he pick up all goods he needs, come back to the gate of warehouse
        # 6. Optimal solution: The last result is the minimize of all feasible solution.
    '''
    #Mô hình định tuyến
    manager = pywrapcp.RoutingIndexManager(len(d), num_vehicles, depot)
    routing = pywrapcp.RoutingModel(manager)
    #khoảng cách

    def distance_callback(from_index, to_index): #routing of the picker
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return info[3][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    
    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.FromSeconds(60)
    
    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(info, manager, routing, solution)
    else:
        print("No solution")

if __name__ == '__main__':
    #t = time.time()
    CSP()
    #print('\nThe time taken is: ',end = ' ')
    #print(time.time() - t)
