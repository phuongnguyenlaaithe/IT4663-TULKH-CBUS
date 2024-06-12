#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, k;
    cin >> n >> k;
    vector<vector<int>> c(2 * n + 1, vector<int>(2 * n + 1));
    for (int i = 0; i <= 2 * n; ++i) {
        for (int j = 0; j <= 2 * n; ++j) {
            cin >> c[i][j];
        }
    }

    vector<bool> pickedUp(n + 1, false);
    vector<bool> droppedOff(n + 1, false);
    vector<int> sequence;
    int currentPos = 0;
    int passengersOnBus = 0;
    int totalPassengers = 0;

    while (totalPassengers < n) {
        int nearest = -1;
        int minDist = INT_MAX;

        // Find the nearest passenger to pick up or drop off
        for (int i = 1; i <= n; ++i) {
            if (!pickedUp[i] && passengersOnBus < k && c[currentPos][i] < minDist) {
                nearest = i;
                minDist = c[currentPos][i];
            }
            if (pickedUp[i] && !droppedOff[i] && c[currentPos][i + n] < minDist) {
                nearest = i + n;
                minDist = c[currentPos][i + n];
            }
        }

        sequence.push_back(nearest);
        currentPos = nearest;
        if (nearest <= n) {
            // Pickup
            pickedUp[nearest] = true;
            passengersOnBus++;
        } else {
            // Drop off
            droppedOff[nearest - n] = true;
            passengersOnBus--;
            totalPassengers++;
        }
    }

    // Return to the start point
    sequence.push_back(0);

    // Output results
    cout << n << endl;
    for (int point : sequence) {
        cout << point << " ";
    }
    cout << endl;

    return 0;
}
