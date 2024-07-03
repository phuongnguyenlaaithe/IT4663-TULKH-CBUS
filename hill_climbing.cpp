#include <iostream>
#include <vector>
#include <algorithm>
#include <unordered_set>
#include <cstdlib>
#include <ctime>
#include <chrono>

using namespace std;

int N; 
int cap;
const int MAX_ITER = 10000; 

vector<vector<int>> c;

int randInt(int a, int b) {
    return a + rand() % (b - a + 1);
}

bool isValid(const vector<int>& x) {
    unordered_set<int> visited;
    int load = 0;

    for (int i = 1; i < x.size() - 1; ++i) {
        if (x[i] <= N) {
            load++;
            if (load > cap || visited.find(x[i]) != visited.end()) {
                return false;
            }
            visited.insert(x[i]);
        } else {
            load--;
            if (visited.find(x[i] - N) == visited.end()) {
                return false;
            }
        }
    }
    return load == 0;
}

vector<int> neighborSolutionSwap(const vector<int>& x) {
    vector<int> neighbor = x;
    int i = randInt(1, 2 * N);
    int j = randInt(1, 2 * N);
    swap(neighbor[i], neighbor[j]);
    return neighbor;
}

vector<int> neighborSolution2Opt(const vector<int>& x) {
    vector<int> neighbor = x;
    int i = randInt(1, 2 * N - 1);
    int j = randInt(i + 1, 2 * N);
    reverse(neighbor.begin() + i, neighbor.begin() + j + 1);
    return neighbor;
}

vector<int> neighborSolutionInsert(const vector<int>& x) {
    vector<int> neighbor = x;
    int i = randInt(1, 2 * N);
    int j = randInt(1, 2 * N);
    int elem = neighbor[i];
    neighbor.erase(neighbor.begin() + i);
    neighbor.insert(neighbor.begin() + j, elem);
    return neighbor;
}

vector<int> neighborSolutionReverseSegment(const vector<int>& x) {
    vector<int> neighbor = x;
    int i = randInt(1, 2 * N - 1);
    int j = randInt(i + 1, 2 * N);
    reverse(neighbor.begin() + i, neighbor.begin() + j + 1);
    return neighbor;
}

vector<int> neighborSolutionShuffleSegment(const vector<int>& x) {
    vector<int> neighbor = x;
    int i = randInt(1, 2 * N - 1);
    int j = randInt(i + 1, 2 * N);
    random_shuffle(neighbor.begin() + i, neighbor.begin() + j + 1);
    return neighbor;
}

vector<int> neighborSolution(const vector<int>& x) {
    int method;
    vector<int> neighbor;
    do {
        method = randInt(1, 5);
        switch (method) {
            case 1: neighbor = neighborSolutionSwap(x); break;
            case 2: neighbor = neighborSolutionInsert(x); break;
            case 3: neighbor = neighborSolution2Opt(x); break;
            case 4: neighbor = neighborSolutionReverseSegment(x); break;
            case 5: neighbor = neighborSolutionShuffleSegment(x); break;
            
        }
    } while (!isValid(neighbor));
    return neighbor;
}


vector<int> initialSolution() {
    vector<int> solution(2 * N + 2); 
    vector<int> passengers(N);
    for (int i = 0; i < N; ++i) {
        passengers[i] = i + 1;
    }
    
    random_shuffle(passengers.begin(), passengers.end());
    solution[0] = 0;
    for (int i = 0; i < N; ++i) {
        solution[2 * i + 1] = passengers[i];
        solution[2 * i + 2] = passengers[i] + N;
    }
    solution[2 * N + 1] = 0; 
    return solution;
}

int objectiveFunction(const vector<int>& x) {
    int cost = 0;
    for (int i = 0; i < x.size() - 1; ++i) {
        cost += c[x[i]][x[i + 1]];
    }
    return cost;
}

vector<int> hillClimbing() {
    vector<int> currentSolution = initialSolution();
    while (!isValid(currentSolution)) {
        currentSolution = initialSolution();
    }
    int currentCost = objectiveFunction(currentSolution);
    vector<int> bestSolution = currentSolution;
    int bestCost = currentCost;

    for (int iter = 0; iter < MAX_ITER; ++iter) {
        vector<int> newSolution = neighborSolution(currentSolution);
        if (isValid(newSolution)) {
            int newCost = objectiveFunction(newSolution);
            if (newCost < currentCost) {
                currentSolution = newSolution;
                currentCost = newCost;

                if (newCost < bestCost) {
                    bestSolution = newSolution;
                    bestCost = newCost;
                }
            }
        }
    }

    return bestSolution;
}

int main() {
    srand(time(0));

    cin >> N >> cap;
    c.resize(2 * N + 1, vector<int>(2 * N + 1));

    for (int i = 0; i <= 2 * N; ++i) {
        for (int j = 0; j <= 2 * N; ++j) {
            cin >> c[i][j];
        }
    }
    
    auto start = std::chrono::high_resolution_clock::now();
    
    vector<int> sol = hillClimbing();

//	auto stop = std::chrono::high_resolution_clock::now();
//	auto duration = std::chrono::duration_cast<std::chrono::microseconds>(stop - start);

	int bestCost = objectiveFunction(sol);
    cout << N << endl;
    for (int i = 1; i <= 2 * N; ++i) {
        cout << sol[i];
        if (i != 2 * N + 1) cout << " ";
    }
//    cout << "Time taken by algorithm: "
//		<< duration.count() << " microseconds" << std::endl;
//	
//	cout << "f: " << objectiveFunction(sol);
    cout << endl;
    return 0;
}