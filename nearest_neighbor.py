import time 

INT_MAX = 2147483647

start = time.time()

'''def data(file):
    with open(file, 'r') as f:
        first_line = f.readline().split()
        N, M = int(first_line[0]), int(first_line[1])
        Q = []
        D = []
        q = []
        for i in range(1, 1+N):
            type = f.readline().split()
            Q.append(list(int(ele) for ele in type))
        # print(Q)
        for j in range(2+N, 3+N+M):
            dis = f.readline().split()
            D.append(list(int(ele) for ele in dis))
        last_line = f.readline().split()
        for ele in last_line:
            q.append(int(ele))
    return N, M, Q, D, q
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

# Check to see if we have enough products
def end(q):
    for p_num in q:
        if(p_num != 0): return False
    return True

def cal_nearest_shelf(c, D, M, r):
    min_d = INT_MAX
    nearest = -1
    for i in range(M + 1):
        if i not in r and D[c][i] != 0 and min_d > D[c][i]: # condition for nearest shelf
            nearest = i
            min_d = D[c][i]
    return nearest, D[c][nearest]

def nearest_neighbor():
    N, M, Q, D, q = data('10_20.txt')
    print("N = %d, M = %d" % (N, M))
    print("len(Q) = %d, len(D) = %d, len(q) = %d" % (len(Q), len(D), len(q)))
    print("MATRIX q:", q)
    s = 0 # Starting location
    c = s # Current location
    r = [] # Result array
    total = 0 # Total distance moved

    r.append(s) # Append starting location
    print("Start from shelf %d" % s)
    print("Matrix q:", q)

    while end(q) == False:
        c, distance = cal_nearest_shelf(c, D, M, r) # Find next shelf to go
        r.append(c)
        print(">>> Go to shelf %d" % c)
        total += distance # Increase distance moved 
        for i in range(N):
            if(q[i] != 0):
                taken = Q[i][c-1] if Q[i][c-1] < q[i] else q[i] # The number of products of type i we will take from the shelf c
                q[i] -= taken
        print("Matrix q:", q)

    r.append(s) # Append ending location
    print(">>> Return to shelf %d" % s)
    total += D[c][s]

    print("\n#### RESULT ####")
    print("\nPath traversed:\n")
    for shelf in r[:-1]:
        print("%d" % shelf, end="->")
    print(r[-1])
    print("\nNumber of nodes:", len(r))
    print("\nDistance of the route:", total)


nearest_neighbor()

elapsed = time.time() - start # Time taken for the program
print("\nTime taken:", elapsed)
