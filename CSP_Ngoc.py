from ortools.sat.python import cp_model
import time

def data(file):
    #M: shelf
    #N: types of goods
    #Q: matrix of quantity of each type in all shelf
    #q: quantity of each type we need to pick up
    #d: matrix of distance between 2 shelves

    with open(file, 'r') as f:
        first_line = f.readline().split()
        N, M = int(first_line[0]), int(first_line[1])
        Q = []
        d = []
        q=[]
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

info = data('200_400.txt')
# print(i)
N = info[0]
M = info[1]
Q = info[2]
d = info[3]
q = info[4]
# print(N, M, Q, d,q)


DISTANCE_MATRIX = d
def main():
    """Entry point of the program."""
    num_nodes = len(DISTANCE_MATRIX)
    all_nodes = range(num_nodes)

    # Model.
    model = cp_model.CpModel()

    obj_vars = []
    obj_coeffs = []
 

    # Create the circuit constraint.
    arcs = []
    arc_literals = {}
    for i in all_nodes:
        for j in all_nodes:
            if i == j:
                continue

            lit = model.NewBoolVar('%i follows %i' % (j, i))
            arcs.append([i, j, lit])
            arc_literals[i, j] = lit

            obj_vars.append(lit)
            obj_coeffs.append(DISTANCE_MATRIX[i][j])

    model.AddCircuit(arcs)

    # Solve and print out the solution.
    solver = cp_model.CpSolver()
    # To benefit from the linearization of the circuit constraint.
    solver.parameters.linearization_level = 2
    #Minimize the total distance
    model.Minimize(sum(obj_vars[i] * obj_coeffs[i] for i in range(len(obj_vars))))
    solver.Solve(model)

    current_node = 0
    str_route = '0 \nRemain Load({0})\n'.format(q)
    route_is_finished = False
    route_distance = 0
    path = []
    while not route_is_finished:
        for i in all_nodes:
            if i == current_node:
                continue
            if solver.BooleanValue(arc_literals[current_node, i]):
                if all(ele==0 for ele in q):
                        route_distance +=d[current_node][0]
                        current_node = 0
                        route_is_finished = True
                        break
    
                else:
                        route_distance +=d[current_node][i]
                        current_node  = i
                for i in range(N): 
                    if q[i] > Q[i][current_node-1]:
                            q[i]= q[i] - Q[i][current_node-1]
                    else:
                            q[i] = 0
                str_route += '\n-> {0}\nRemain Load({1})\n'.format(current_node, q)
                path.append(current_node)
            
    path = [0] + path
    str_route += '\n-> {0}\nRemain Load({1})\n'.format(0, q)
    path.append(0)
    print('Route:', str_route)
    print('Travelled distance:', route_distance)
    path_update = " ".join([str(i) for i in path]).replace(" ","->")
    print("Path traversal: ",path_update)
    print("Number of nodes: ",len(path))

if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time execution: ",time.time() - start)
