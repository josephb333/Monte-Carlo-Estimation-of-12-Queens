#include <iostream>
#include <vector>
#include <ctime>
#include <cstdlib>
#include <algorithm>
#include <cmath>
#include <random>

using namespace std;

const int N = 12; // Board size

// Global counter for tracking operations
long long operationCount = 0;
long long solutionCount = 0;

// column[i] = j means queen in row i is at column j
// Check if placing a queen at row i, column[i] is safe
bool isPromising(vector<int>& column, int row) {
    operationCount++; // Count constraint checks
    
    // Check against all previously placed queens (rows 0 to row-1)
    for (int i = 0; i < row; i++) {
        operationCount++;
        
        // Check if in same column
        if (column[i] == column[row]) {
            return false;
        }
        
        // Check if on same diagonal
        // Two queens are on same diagonal if |row1 - row2| == |col1 - col2|
        if (abs(column[i] - column[row]) == abs(i - row)) {
            return false;
        }
    }
    return true;
}

// Monte Carlo backtracking - randomly select one promising child per level
bool solveNQueensMonteCarlo(vector<int>& column, int row, long long &solutionCount) {
    operationCount++; // Count node visits
    
    // Base case: all queens placed successfully
    if (row >= N) {
        solutionCount++;
        return true; // Found a solution
    }
    
    // Find all promising columns for this row
    vector<int> promisingCols;
    for (int col = 0; col < N; col++) {
        column[row] = col;
        if (isPromising(column, row)) {
            promisingCols.push_back(col);
        }
    }
    
    // If no promising children, backtrack
    if (promisingCols.empty()) {
        return false;
    }
    
    // MONTE CARLO: Randomly select ONE promising child
    int randomIndex = rand() % promisingCols.size();
    column[row] = promisingCols[randomIndex];
    
    // Recursively solve with the randomly selected column
    return solveNQueensMonteCarlo(column, row + 1, solutionCount);
}

// Run one Monte Carlo trial
long long runTrial(int trialNum) {
    operationCount = 0; // Reset counter for this trial
    solutionCount = 0;  // Reset solution count for this trial
    
    vector<int> column(N, -1); // column[row] = col position of queen
    
    // Seed random for this trial
    srand(time(NULL) + trialNum * 1000);
    
    solveNQueensMonteCarlo(column, 0, solutionCount);
    
    cout << "Trial " << trialNum << ": " 
         << "Solutions: " << solutionCount
         << " - Operations: " << operationCount << endl;
    
    return operationCount;
}

// Calculate statistics
void printStatistics(vector<long long>& numOps) {
    // TODO: Calculate and print:
    // - Minimum operations
    // - Maximum operations
    // - Average operations
    // - Median operations
    // - Standard deviation
    cout << "\nStatistics:" << endl;
    cout << "Operations performed " << numOps.size() << " number of trials:" << endl;
    for (size_t i = 0; i < numOps.size(); i++) {
        cout << "Trial " << (i + 1) << ": " << numOps[i] << " operations" << endl;
    }

}

int main() {
    srand(time(NULL));
    
    int numTrials;
    cout << "Enter number of Monte Carlo trials: ";
    cin >> numTrials;
    
    vector<long long> numOps;
    
    cout << "\n=== Running Monte Carlo Simulation ===" << endl;
    cout << "Solving " << N << "-Queens problem..." << endl << endl;
    
    clock_t startTime = clock();
    
    // Run multiple trials
    for (int i = 1; i <= numTrials; i++) {
        long long ops = runTrial(i);
        numOps.push_back(ops);
    }
    
    clock_t endTime = clock();
    double totalTime = double(endTime - startTime) / CLOCKS_PER_SEC;
    
    cout << "\n=== Results ===" << endl;
    cout << "Total execution time: " << totalTime << " seconds" << endl;
    cout << "Average time per trial: " << (totalTime / numTrials) << " seconds" << endl << endl;
    
    printStatistics(numOps);
    
    cout << "\n=== Time Complexity Estimate ===" << endl;
    cout << "Based on " << numTrials << " trials for n=" << N << endl;
    // TODO: Add analysis of complexity
    
    return 0;
}

/*PROFESSORS SOLUTION FROM SLIDES*/
/*numnodes = 1; mproduct = 1; i=0;
while (m!= 0 && i != n) {
    mproduct = mproduct * m;  // Computing # of nodes in pruned SST;
    numnodes = numnodes + mproduct * n; // Number of childer t is n in n-queens
    i++;
    // computing promising nodes in level i
    m = 0;
    promisingChildren = NULL;   // initilize set of promising nodes
    for (j=1;j<=n;j++){    
        column[i] = j;  // keep track of placements of ith queens
        if (isPromising(column,i)) {    // determine promising children
            m++;
            promisingChildren = promisingChildren union {j};
            }
        }
    if (m != 0){
        h = rand() % m; // select random child; Choosing one promising childe randomly.
        column[i] = j;
    }
    return numnodes;
}   
*/