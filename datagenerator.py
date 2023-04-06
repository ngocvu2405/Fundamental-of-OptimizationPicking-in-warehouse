import random as rd

def genData(filename, M, N, MAX_COORDINATE, MAX_Q):
    f = open(filename, 'w')
    f.write(str(N) + ' ' + str(M) + '\n')
    Q = [[0 for i in range(M)] for j in range(N)]
    for i in range(N):
        for j in range(M):
            Q[i][j] = rd.randint(1, MAX_Q)

    for i in range(N):
        line = ''
        for j in range(M):
            line = line + str(Q[i][j]) + ' '
        line = line + '\n'
        f.write(line)

    x = [0 for i in range(M+1)]
    y = [0 for i in range(M+1)]
    for i in range(M+1):
        x[i] = rd.randint(1, MAX_COORDINATE)
        y[i] = rd.randint(1, MAX_COORDINATE)

    d = [[0 for i in range(M+1)] for j in range(M+1)]
    for i in range(M+1):
        for j in range(M+1):
            d[i][j] = abs(x[i] - x[j]) + abs(y[i] - y[j])
    
    for i in range(M+1):
        line = ''
        for j in range(M+1):
            line = line +str(d[i][j]) + ' '
        f.write(line + '\n')

    q = [0 for i in range(N)]
    for i in range(N):
        q[i] = rd.randint(1, sum(Q[i][j] for j in range(M)))
        f.write(str(q[i]) + ' ')

genData('25_50.txt', 20, 40, 10, 100)
