from ortools.sat.python import cp_model

def solve_bus_routing(n, k, c):
    # Khởi tạo model
    model = cp_model.CpModel()

    # Tạo biến quyết định
    x = {}
    for i in range(2 * n + 1):
        for j in range(2 * n + 1):
            if i != j:
                x[i, j] = model.NewBoolVar(f'x[{i},{j}]')

    U = [model.NewIntVar(0, 2 * n, f'U[{i}]') for i in range(2 * n + 1)]
    q = [model.NewIntVar(0, k, f'q[{i}]') for i in range(2 * n + 1)]
    
    # Thêm các ràng buộc
    for i in range(2 * n + 1):
        model.Add(sum(x[i, j] for j in range(2 * n + 1) if i != j) == 1)
        model.Add(sum(x[j, i] for j in range(2 * n + 1) if i != j) == 1)

    model.Add(U[0] == 0)
    model.Add(q[0] == 0)

    for i in range(1, n + 1):
        model.Add(U[i] < U[i + n])

    for i in range(2 * n + 1):
        model.Add(q[i] <= k)

    for i in range(2 * n + 1):
        for j in range(1, 2 * n + 1):
            if i != j:
                model.Add(U[i] - U[j] + (2 * n + 1) * x[i, j] <= 2 * n)
    
    for i in range(1, 2 * n + 1):
        for j in range(1, 2 * n + 1):
            if i != j:
                model.Add(x[i, j] + x[j, i] <= 1)
    
    for i in range(1, 2 * n + 1):
        for j in range(1, n + 1):
            if i != j:
                model.Add((q[i] + 1 - q[j]) == 0).OnlyEnforceIf(x[i, j])
        for j in range(n + 1, 2 * n + 1):
            if i != j:
                model.Add((q[i] - 1 - q[j]) == 0).OnlyEnforceIf(x[i, j])
    
    # Tạo đối tượng tối ưu
    total = sum(c[i][j] * x[i, j] for i in range(2 * n + 1) for j in range(2 * n + 1) if i != j)
    model.Minimize(total)

    # Giải bài toán
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        print(n)
        route = []
        current = 0
        while len(route) < 2 * n:
            for j in range(2 * n + 1):
                if current != j and solver.Value(x[current, j]) == 1:
                    route.append(j)
                    current = j
                    break
        print(" ".join(map(str, route)))
    else:
        print("No solution found")

if __name__ == "__main__":
    n, k = map(int, input().split())

    c = [[0] * (2 * n + 1) for _ in range(2 * n + 1)]
    for i in range(2 * n + 1):
        c[i] = list(map(int, input().split()))

    solve_bus_routing(n, k, c)
