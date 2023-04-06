import random
import time

start = time.time()
'''
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
        D = []
        q=[]
        for i in range (1, 1+N):
            type = f.readline().split()
            Q.append(list(int(ele) for ele in type))
        # print(Q)
        for j in range (2+N, 3+N+M):
            dis = f.readline().split()
            D.append(list(int(ele) for ele in dis))
        last_line = f.readline().split()
        for ele in last_line:
            q.append(int(ele))
    return N, M, Q, D,q'''
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
class Individual:
    def __init__(self):
        self.path = []
        self.fitness = 0
        self.length = 0
    def __lt__(self, other):
        return self.fitness < other.fitness
    def __gt__(self, other):
        return self.fitness > other.fitness

# Generate a random from start to end
def rand_num(start, end):
    return random.randint(start, end-1)

# Check if a shelf is already traversed in a path
def is_traversed(shelf, path):
    return shelf in path

def cal_fitness(ind, D):
    path = ind.path # 0 1 5 2 4 ... path[ind.length] (not containing 0 at the end)
    fitness = 0
    for i in range(1, ind.length): # From the second element to the last element
#       print("fitness += D[%d][%d] (%d)" % (path[i-1], path[i], D[path[i-1]][path[i]]))
        fitness += D[path[i-1]][path[i]] # fitness += D[previous_shelf][current_shelf]
#   print("fitness += D[%d][0] (%d)" % (path[i], D[path[i]][0]))
    fitness += D[path[i]][0] # fitness += D[current_shelf][0] (return to the beginning position)
    return fitness

def end(q):
    for p_num in q:
        if p_num != 0:
            return False
    return True

# Calculate matrix q for given path
def cal_q(path, N, Q, q):
    for shelf in path[1:]:
        for i in range(N):
            if q[i] != 0:
                taken = Q[i][shelf-1] if Q[i][shelf-1] < q[i] else q[i]
                q[i] -= taken
    return q

def cal_real_path(path, N, Q, q):
    real_path = [0]
    q_temp = q.copy()
    for shelf in path[1:]:
        real_path.append(shelf)
        for i in range(N):
            if q_temp[i] != 0: # Visit this shelf
                taken = Q[i][shelf-1] if Q[i][shelf-1] < q_temp[i] else q_temp[i]
                q_temp[i] -= taken
        if end(q_temp):
            real_path.append(0)
            return real_path

# s: starting position
# Create a path randomly
def create_individual(s, Q, D, q, M, N):
    ind = Individual()
    path = []
    path.append(s) # Append starting position
    q_temp = q.copy()
    # Generate the real part
    while not end(q_temp):
        shelf = rand_num(1, M+1) # Generate random shelf from 1 -> M+1
        if not is_traversed(shelf, path):
            path.append(shelf)
            for i in range(N):
                if q_temp[i] != 0:
                    # products taken from the shelf shelf-1 (because shelf starts from 1)
                    taken = Q[i][shelf-1] if Q[i][shelf-1] < q_temp[i] else q_temp[i]
                    q_temp[i] -= taken

    # Individual's length
    ind.length = len(path)

    # Generate the virtual part
    for i in range(1, M+1):
        if i not in path:
            path.append(i)
    
    # Individual's path
    ind.path = path

    # Individual's fitness
    ind.fitness = cal_fitness(ind, D)

    return ind

# Fill a child knowing parent, crossover gene and crossover position
def fill_child(p, g, r, r1, M):
    c = [-1 for i in range(M+1)]  # New child
    c[0] = p.path[0]
    c_pos = r
    # Fill in crossover part
    for i in g:
        c[c_pos] = i
        c_pos = 1 if c_pos == M else c_pos + 1

    p_pos = r1
    while c_pos != r:
        if p.path[p_pos] not in g:
            c[c_pos] = p.path[p_pos]
            c_pos = 1 if c_pos == M else c_pos + 1
        p_pos = 1 if p_pos == M else p_pos + 1
    return c


def crossover_ox(p1, p2, M, N, Q, D, q):
    c1 = Individual()
    c2 = Individual()
    c1.path = [-1 for i in range(M+1)]
    c2.path = [-1 for i in range(M+1)]
    r = r1 = None

    # Generate positions to crossover
    r = rand_num(1, M+1)
    r1 = rand_num(r, M+1) if r != M+1 else r
    
    # Crossover part
    if r != r1:
        g1 = p1.path[r:r1]
        g2 = p2.path[r:r1]
    else:
        g1 = [p1.path[r]]
        g2 = [p2.path[r]]

#    print("\n CROSSOVER FROM %d TO %d" % (r, r1))
#    print(g1)
#    print(g2)
    c1.path = fill_child(p1, g2, r, r1, M)
    c1.length = len(cal_real_path(c1.path, N, Q, q)) - 1
    c1.fitness = cal_fitness(c1, D)
    c2.path = fill_child(p2, g1, r, r1, M)
    c2.length = len(cal_real_path(c2.path, N, Q, q)) - 1
    c2.fitness = cal_fitness(c2, D)
    return c1, c2

def mutation_swap(ind, D):
    new_ind = Individual()
    new_ind.path = ind.path.copy()
    new_ind.length = ind.length # Length will not be changed
    while True:
        # Generate two random positions (not including the first position and the virtual part)
        r = rand_num(1, new_ind.length)
        r1 = rand_num(1, new_ind.length)
        if r != r1: # Two positions must be different
            # Swap
            temp = new_ind.path[r]
            new_ind.path[r] = new_ind.path[r1]
            new_ind.path[r1] = temp
            break
    new_ind.fitness = cal_fitness(new_ind, D) # Recalculate the fitness value
    return new_ind 

def mutation_cut(ind, M, N, D, Q, q):
    new_ind = Individual()
    new_ind.path = ind.path.copy()

    r = rand_num(ind.length//2, ind.length) # Generate a random position from length//2 -> length
    new_ind.path = new_ind.path[:r] # Cut from position r to the end
    q_temp = q.copy()
    q_temp = cal_q(new_ind.path, N, Q, q_temp) # Recalculate q matrix based on current path

    # Generate new path
    while not end(q_temp):
        shelf = rand_num(1, M+1)
        if not is_traversed(shelf, new_ind.path):
            new_ind.path.append(shelf)
            for i in range(N):
                if q_temp[i] != 0:
                    taken = Q[i][shelf-1] if Q[i][shelf-1] < q_temp[i] else q_temp[i]
                    q_temp[i] -= taken
    
    # Length
    new_ind.length = len(ind.path)

    # Generate virtual part
    for i in range(1, M+1):
        if i not in new_ind.path:
            new_ind.path.append(i)
    new_ind.fitness = cal_fitness(new_ind, D)
    return new_ind

# Select the first `size` individuals that have highest fitness value
def select(pop, size):
    pop.sort()
    return pop[:size]

# Print information about every members in the population
def print_pop(pop, N, Q, q):
    #print("@@@ POPULATION INFORMATION @@@")
    for i in range(len(pop)):
        print("=> INDIVIDUAL %d" % (i+1))
        print_ind(pop[i])

def print_ind(ind, N, Q, q):
    print(cal_real_path(ind.path, N, Q, q))
    print("\nDistance of the route:", ind.fitness)
    print("Number of nodes:", ind.length+1)

def traverse_until(time_limit: int = 600):
    N, M, Q, D, q = data()

    # Constants
    POP_SIZE = 10 # Size of the population
    MUTATION_SWAP_PERCENT = 0.2
    MUTATION_ADD_PERCENT = 0.1
    
    # Vars
    pop = [] # Population array
    gen = 1 # Current generation
    gen_thres = 100 # Number of generations
    s = 0 # Starting position

    # Generate POP_SIZE individuals and append to population
    for i in range(POP_SIZE):
        ind = create_individual(s, Q, D, q, M, N)
        pop.append(ind) 

#   print_pop(pop, N, Q, q)

    # Loop for generations
    while gen <= gen_thres:
#       print("###### GENERATION %d ######" % gen)

        random.shuffle(pop)

        # Crossover
        i = 0
        while i < POP_SIZE:
            c1, c2 = crossover_ox(pop[i], pop[i-1], M, N, Q, D, q)

            # Mutation
            mutation_c1 = random.random()
            mutation_c2 = random.random()
            # mutation_c1 <= 0.1 then call mutation_cut()
            if mutation_c1 <= MUTATION_ADD_PERCENT:
                c1 = mutation_cut(c1, M, N, D, Q, q)
            # else if 0.1 < mutation_c1 <= 0.2 then call mutation_swap()
            elif mutation_c1 <= MUTATION_SWAP_PERCENT:
                c1 = mutation_swap(c1, D)
            # mutation_c2 <= 0.1 then call mutation_cut()
            if mutation_c2 <= MUTATION_ADD_PERCENT:
                c1 = mutation_cut(c2, M, N, D, Q, q)
            # else if 0.1 < mutation_c2 <= 0.2 then call mutation_swap()
            elif mutation_c2 <= MUTATION_SWAP_PERCENT:
                c2 = mutation_swap(c2, D)  

            pop.append(c1)
            pop.append(c2)

            i+=2
        pop = select(pop, POP_SIZE)

#       print_pop(pop, N, Q, q)

        gen += 1

    #print("\n#### RESULT ####\n")
    print_ind(pop[0], N, Q, q)

traverse_until()

#elapsed = time.time() - start
#print("\nTime taken:", elapsed)
