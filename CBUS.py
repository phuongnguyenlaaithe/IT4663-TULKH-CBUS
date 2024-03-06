import sys

MAX_N = 100

N = 0  # number of passengers
Q = 0  # number of seats on the bus
X = [0] * (2 * MAX_N + 1)  # represent the route X[1], X[2], . . . X[2N]
appear = [False] * (2 * MAX_N + 1)
c = [[0] * (2 * MAX_N + 1) for _ in range(2 * MAX_N + 1)]  # distance matrix

bestRoute = [0] * (2 * MAX_N + 1)  # store the best route found so far
minDistance = sys.maxsize  # store the minimum distance found so far

q = 0  # number of passengers currently on the bus


# Function to check if passenger v can be picked up or dropped off
def check(v, k):
    global q
    if appear[v]:
        return False
    if v <= N:  # v is a pickup
        if q >= Q:
            return False
    else:  # v > N means drop-off
        if not appear[v - N]:
            return False
    return True


# Function to calculate the total distance of the route
def calculateDistance():
    distance = 0
    for i in range(1, 2 * N + 1):
        distance += c[X[i - 1]][X[i]]
    distance += c[X[2 * N]][0]  # return to point 0
    return distance


# Function to print the solution
def solution():
    global minDistance
    distance = calculateDistance()
    if distance < minDistance:
        minDistance = distance
        for i in range(1, 2 * N + 1):
            bestRoute[i] = X[i]


# Backtracking function to find the shortest route
def TRY(k):
    global q
    for v in range(1, 2 * N + 1):
        if check(v, k):
            X[k] = v
            appear[v] = True
            if v <= N:
                q += 1
            else:
                q -= 1  # update q incrementally
            if k == 2 * N:
                solution()
            else:
                TRY(k + 1)
            appear[v] = False
            if v <= N:
                q -= 1
            else:
                q += 1  # recover status q


if __name__ == "__main__":
    N, Q = map(int, input().split())

    # Read distance matrix
    for i in range(2 * N + 1):
        c[i] = list(map(int, input().split()))

    q = 0
    appear = [False] * (2 * N + 1)

    TRY(1)

    # Output the best route
    print(N)
    for i in range(1, 2 * N + 1):
        print(bestRoute[i], end=" ")
    print()
