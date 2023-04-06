
from ortools.sat.python import cp_model
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import time

def _input(file):
    with open(file,'r') as f:
        first_line = f.readline().split()
        N, M = int(first_line[0]),int(first_line[1])
        Q = []
        for i in range(N):
            line = f.readline().split()
            Q.append([int(num) for num in line])
        d = []
        for i in range(M+1):
            line = f.readline().split()
            d.append([int(num) for num in line])
        q = [int(num) for num in f.readline().split()]
    return [N,M,Q,d,q]

'''def _input():
    # N: The number of type of product
    # M: The number of shelf
    N, M = [int(i) for i in input().split()]

    # Matrix Q(NxM)
    Q = []
    for i in range(1,N+1): # Input N lines (equivalent to N types of product)
        Q.append([int(i) for i in input().split()])

    # Distance matrix
    D = []
    for i in range(M+1): # Input M+1 lines (equivalent to distances between shelf 0,1,2,...,M)
        D.append([int(i) for i in input().split()])

    # Products that need to take
    q = [int(i) for i in input().split()]

    return [N, M, Q, D, q]'''
def warehouse_picking_routing(d,Q,q):
    
    """
    Solve the ware_house_picking_routing
    d: matrix containing the distance between the depot and the shelves
    Q: matrix containing the number of products of each type available at each shelf
    q: list containing the demand of each product type
    max_distance: the maximum distance picker can travel
    return the optimal path, the total distance traveled and the total demand met
    """
        
    N = len(Q)
    M = len(Q[0])
    
    #Create the solver
    model = cp_model.CpModel()

    #Define the variable
    x = [[0 for col in range(M+1)] for row in range(M+1)]
    
    #Create the variable
    #X[shelfi][shelfj] = 1 if picker travel from shelf i to shelf j
    for shelfi in range(M+1):
        for shelfj in range(M+1):
            x[shelfi][shelfj] = model.NewIntVar(0,1,'x[{}][{}]'.format(shelfi,shelfj))       
    p = [0 for j in range(M+1)] #Picker travel shelf j or not
    
    u = [0 for i in range(M+1)]
    for i in range(M+1):
        u[i] = model.NewIntVar(0,M+1,'u[{}]'.format(i))
    #init p[i]
    for j in range(M+1): #M -> M+1
        p[j] = model.NewIntVar(0, 1, 'p[{}]'.format(j))
    #print(p)
    #Define the constraint
    model.Add(p[0] == 1) #Add visit 0 -> p[0] = 1      

    #2.A shelf is only traveled one time
    c1 = 0
    c2 = 0 #Need a constraint if go to shelf i => must go out from self i
    for shelfi in range(M+1): 
        for shelfj in range(M+1): 
            if shelfi!= shelfj:
                c1 += x[shelfi][shelfj]
                c2 += x[shelfj][shelfi]
        model.Add(c1 <= 1) #model.Add move in the loop and replace c==1 => c<=1 'cause if not visit that shelf
        #Add more constraint
        model.Add(c2 <= 1)
        #if c1 == 0 -> the shelf i is not visited -> p[shelfi] == 0
        model.Add(c1 == p[shelfi])
        #if c1 == 1 -> if go to then must go out from it -> c2 == 1 
        model.Add(c1 == c2)
        c1 = 0
        c2 = 0
    #Order of the next point in path is order of previous point + 1, this also eliminates sub-tours
    #u[0] = 0
    model.Add(u[0] == 0)
    for i in range(M+1):
        for j in range(1,M+1):
            if i!= j:
                b = model.NewBoolVar('b')
                model.Add(x[i][j] == 1).OnlyEnforceIf(b)
                #model.Add(x[i][j] == 1).OnlyEnforceIf(b)
                model.Add(x[i][j] != 1).OnlyEnforceIf(b.Not())
                model.Add(u[j] == u[i] + 1).OnlyEnforceIf(b)
    #Add a picked list
    picked = [0 for i in range(N)]
    for i in range(N):
        for j in range(1, M+1):
            picked[i] += p[j] * Q[i][j-1]
        model.Add(picked[i] >= q[i])

    
    # When he picks up goods he needs, then comeback to the gate of warehouse:
    # model.Add(sum(x[i][0] for i in range(M + 1)) == 1)
    # model.Add(sum(picked[i] >= q[i]) for i in range)

    # Feasible solution: The total distance is the sum of all journey to pick up all goods 
    total_distance = 0
    for shelfi in range(M+1):
        for shelfj in range(M+1):
            if shelfi != shelfj:
                total_distance += d[shelfi][shelfj] * x[shelfi][shelfj] 

    model.Minimize(total_distance)
    
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    #print(status)
    #print(solver.ObjectiveValue())
    #Print the solution
    # print(cp_model.OPTIMAL)
    # print(solver.StatusName(status))
    # print(cp_model.FEASIBLE)
    # print(cp_model.INFEASIBLE)
    # print(solver.ObjectiveValue())
    if status == cp_model.OPTIMAL:
        #Extract the solution
        print("Minimum total distance: ",solver.ObjectiveValue())
        total_shelf = sum(solver.Value(p[i]) for i in range(1, M+1))
        print(total_shelf)
        i = total_shelf
        start = 0
        while(i != 0):
            for j in range(0, M+1):
                if(solver.Value(x[start][j]) == 1):
                    print(j, end= ' ')
                    start = j
                    break
            i -= 1
        print()
        #for i in range(M+1):
            # print(solver.Value(p[i]), end = ' ')
        #print()
        #for i in range(N):
          #  print(solver.Value(picked[i]), end = ' ')
        #print()

        for i in range(M+1):
            print(solver.Value(p[i]))
            for j in range(M+1):
                print(solver.Value(x[i][j]), end = ' ')
            print()

        #for i, j in x:
             #if solver.Value(x[i, j])  == 1:
                 #print("Picker travel from shelf",i,"to shelf",j)
    else:
        print("No optimal solution")
    
if __name__ == "__main__":
    start = time.time()
    F = _input('5_6.txt')
    warehouse_picking_routing(F[3],F[2],F[4])
    print('The time taken is: ',time.time() - start)
