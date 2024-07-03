from ortools.linear_solver import pywraplp
import time


def create_variables(solver, n):
    X = {t: {i: {j: solver.IntVar(0, 1, name=f'X[{t}][{i}][{j}]')for j in range(2 * n + 1)
            } for i in range(2 * n + 1)
        } for t in range(2 * n + 1)
    }
    return X


def add_constraints(solver, X, a_value, n, k):
    # Xe buýt bắt đầu từ điểm 0
    solver.Add(sum(X[0][0][i] for i in range(2 * n + 1)) == 1)
    # Xe buýt không thể quay về điểm 0 ở các thời điểm trung gian
    for t in range(1, 2 * n):
        solver.Add(sum(X[t][i][0] for i in range(2 * n + 1)) == 0)
    # Xe buýt kết thúc tại điểm 0
    solver.Add(sum(X[2 * n][i][0] for i in range(2 * n + 1)) == 1)

    # Đảm bảo mỗi điểm chỉ được ghé một lần
    for j in range(1, 2 * n + 1):
        solver.Add(sum(X[t][i][j] for t in range(2 * n + 1) for i in range(2 * n + 1)) == 1)
        solver.Add(sum(X[t][j][i] for t in range(2 * n + 1) for i in range(2 * n + 1)) == 1)

    # Ràng buộc tổng số lần ghé mỗi điểm tại mỗi thời điểm là 1
    for t in range(2 * n + 1):
        solver.Add(sum(X[t][i][j] for i in range(2 * n + 1) for j in range(2 * n + 1)) == 1)

    # Ràng buộc số lượng khách trên xe buýt tại mọi thời điểm
    for t_now in range(2 * n + 1):
        solver.Add(0 <= sum(
            X[t][i][j] * a_value[j] for i in range(2 * n + 1) for j in range(2 * n + 1) for t in range(t_now + 1)))
        solver.Add(sum(
            X[t][i][j] * a_value[j] for i in range(2 * n + 1) for j in range(2 * n + 1) for t in range(t_now + 1)) <= k)

    # Ràng buộc bảo toàn luồng
    for t in range(2 * n):
        for p in range(2 * n + 1):
            solver.Add(sum(X[t][i][p] for i in range(2 * n + 1)) == sum(X[t + 1][p][j] for j in range(2 * n + 1)))

    # Ràng buộc điểm đón và trả
    for p in range(n + 1, 2 * n + 1):
        for t_now in range(2 * n + 1):
            solver.Add(sum(X[t_now][i][p] for i in range(2 * n + 1)) <= sum(
                X[t][i][p - n] for i in range(2 * n + 1) for t in range(t_now)))


def cbus(c, n, k):
    solver = pywraplp.Solver.CreateSolver('CBC')

    # Giá trị trợ giúp để tính số khách trên xe
    a_value = [0] + [1] * n + [-1] * n

    # Khởi tạo biến
    X = create_variables(solver, n)

    # Thêm các ràng buộc
    add_constraints(solver, X, a_value, n, k)

    # Hàm mục tiêu: Tối thiểu hóa tổng chi phí di chuyển
    solver.Minimize(
        sum(c[i][j] * X[t][i][j] for t in range(2 * n + 1) for i in range(2 * n + 1) for j in range(2 * n + 1)))
    solver.set_time_limit(120000)  # Đơn vị là milliseconds
    # Giải bài toán
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        route = []
        for t in range(2 * n + 1):
            for i in range(2 * n + 1):
                for j in range(2 * n + 1):
                    if X[t][i][j].solution_value() == 1:
                        route.append(i)
        optimal_cost = solver.Objective().Value()
        return route
    else:
        print('Không tìm thấy giải pháp tối ưu.')
        return []


if __name__ == "__main__":
    N, k = map(int, input().split())
    c = [list(map(int, input().split())) for _ in range(2 * N + 1)]

    start = time.time()
    print(N)
    bestRoute = cbus(c, N, k)
    for i in range(1, len(bestRoute)):
        print(bestRoute[i], end=" ")

