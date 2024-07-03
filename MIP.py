from ortools.linear_solver import pywraplp


def create_variables(solver, n):
    X = {
        k: {
            i: {
                j: solver.IntVar(0, 1, name=f'X[{k}][{i}][{j}]')
                for j in range(2 * n + 1)
            } for i in range(2 * n + 1)
        } for k in range(2 * n + 1)
    }
    return X

def add_constraints(solver, X, a_value, n, cap):
    # Xe buýt bắt đầu từ điểm 0
    fc1 = solver.Constraint(1, 1)
    for i in range(2 * n + 1):
        if i != 0:
            fc1.SetCoefficient(X[0][0][i], 1)

    # Xe buýt không thể quay về điểm 0 ở các thời điểm trung gian
    for k in range(1, 2 * n):
        fc2 = solver.Constraint(0, 0)
        for i in range(2 * n + 1):
            if i != 0:
                fc2.SetCoefficient(X[k][i][0], 1)

    # Xe buýt kết thúc tại điểm 0
    fc3 = solver.Constraint(1, 1)
    for i in range(2 * n + 1):
        if i != 0:
            fc3.SetCoefficient(X[2 * n][i][0], 1)

    # Đảm bảo mỗi điểm chỉ được ghé một lần
    for j in range(1, 2 * n + 1):
        fc4 = solver.Constraint(1, 1)
        for k in range(2 * n + 1):
            for i in range(2 * n + 1):
                fc4.SetCoefficient(X[k][i][j], 1)

        fc5 = solver.Constraint(1, 1)
        for k in range(2 * n + 1):
            for i in range(2 * n + 1):
                fc5.SetCoefficient(X[k][j][i], 1)

    # Ràng buộc tổng số lần ghé mỗi điểm tại mỗi thời điểm là 1
    for k in range(2 * n + 1):
        fc6 = solver.Constraint(1, 1)
        for i in range(2 * n + 1):
            for j in range(2 * n + 1):
                fc6.SetCoefficient(X[k][i][j], 1)

    # Ràng buộc số lượng khách trên xe buýt tại mọi thời điểm
    for k_now in range(2 * n + 1):
        fc7 = solver.Constraint(0, cap)
        for k in range(k_now + 1):
            for i in range(2 * n + 1):
                for j in range(2 * n + 1):
                    fc7.SetCoefficient(X[k][i][j], a_value[j])

    # Ràng buộc bảo toàn luồng
    for k in range(2 * n):
        for p in range(2 * n + 1):
            fc8 = solver.Constraint(0, 0)
            for i in range(2 * n + 1):
                fc8.SetCoefficient(X[k][i][p], 1)
            for j in range(2 * n + 1):
                fc8.SetCoefficient(X[k + 1][p][j], -1)

    # Ràng buộc điểm đón và trả
    for p in range(n + 1, 2 * n + 1):
        for k_now in range(2 * n + 1):
            fc9 = solver.Constraint(-1, 0)
            for i in range(2 * n + 1):
                fc9.SetCoefficient(X[k_now][i][p], 1)
            for k in range(k_now):
                for i in range(2 * n + 1):
                    fc9.SetCoefficient(X[k][i][p - n], -1)

def cbus(c, n, cap):
    solver = pywraplp.Solver.CreateSolver('CBC')

    # Giá trị trợ giúp để tính số khách trên xe
    a_value = [0] + [1] * n + [-1] * n

    # Khởi tạo biến
    X = create_variables(solver, n)

    # Thêm các ràng buộc
    add_constraints(solver, X, a_value, n, cap)

    # Hàm mục tiêu: Tối thiểu hóa tổng chi phí di chuyển
    solver.Minimize(
        sum(c[i][j] * X[k][i][j] for k in range(2 * n + 1) for i in range(2 * n + 1) for j in range(2 * n + 1)))

    # Giải bài toán
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        route = []
        for k in range(2 * n + 1):
            for i in range(2 * n + 1):
                for j in range(2 * n + 1):
                    if X[k][i][j].solution_value() == 1:
                        route.append(i)
        optimal_cost = solver.Objective().Value()
        return route, optimal_cost
    else:
        print('Không tìm thấy giải pháp tối ưu.')
        return []

if __name__ == "__main__":
    N, cap = map(int, input().split())
    c = [list(map(int, input().split())) for _ in range(2 * N + 1)]


    print(N)
    bestRoute, cost = cbus(c, N, cap)
    for i in range(1, len(bestRoute)):
        print(bestRoute[i], end=" ")

