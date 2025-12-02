"""
Monte Carlo Estimation for 12-Queens Problem

This program implements the Monte Carlo method to estimate the number of nodes
that would be visited by a backtracking algorithm when solving the N-Queens problem.

The Monte Carlo estimation works by:
1. At each row, count valid positions for placing a queen
2. Randomly select one valid position and move to the next row
3. Multiply the number of valid positions at each level to get an estimate
4. Repeat multiple trials and average the results

Author: Joseph B
Date: 2025
"""

import random
import time


def is_safe(board, row, col, n):
    """
    Check if placing a queen at (row, col) is safe.
    
    Args:
        board: List where board[i] is the column of the queen in row i
        row: The row to check
        col: The column to check
        n: Board size
        
    Returns:
        True if the position is safe, False otherwise
    """
    for i in range(row):
        # Check column conflict
        if board[i] == col:
            return False
        # Check diagonal conflicts
        if abs(board[i] - col) == abs(i - row):
            return False
    return True


def get_valid_positions(board, row, n):
    """
    Get all valid column positions for placing a queen in the given row.
    
    Args:
        board: Current board state
        row: The row to find valid positions for
        n: Board size
        
    Returns:
        List of valid column indices
    """
    valid = []
    for col in range(n):
        if is_safe(board, row, col, n):
            valid.append(col)
    return valid


def monte_carlo_estimate(n, num_trials=1000, seed=None):
    """
    Estimate the number of nodes visited by backtracking using Monte Carlo method.
    
    The estimation is based on the formula:
    E = 1 + m1 + m1*m2 + m1*m2*m3 + ... + m1*m2*...*mn
    
    Where mi is the number of valid positions at level i.
    
    Args:
        n: Board size (number of queens)
        num_trials: Number of Monte Carlo trials to run
        seed: Optional random seed for reproducibility
        
    Returns:
        Tuple of (average_estimate, individual_estimates, avg_time_per_trial)
    """
    if seed is not None:
        random.seed(seed)
    
    estimates = []
    start_time = time.time()
    
    for _ in range(num_trials):
        board = [-1] * n
        estimate = 1  # Root node
        product = 1
        
        for row in range(n):
            valid_positions = get_valid_positions(board, row, n)
            m = len(valid_positions)
            
            if m == 0:
                # Dead end reached - this trial hit a dead end before completing
                # The partial estimate is still valid as it represents this path's
                # contribution to the tree size estimate
                break
            
            product *= m
            estimate += product
            
            # Randomly choose one valid position
            board[row] = random.choice(valid_positions)
        
        estimates.append(estimate)
    
    end_time = time.time()
    avg_time = (end_time - start_time) / num_trials
    
    return sum(estimates) / len(estimates), estimates, avg_time


def backtracking_count_nodes(n):
    """
    Count the actual number of nodes visited by the backtracking algorithm.
    
    Args:
        n: Board size
        
    Returns:
        Tuple of (node_count, solutions_found, time_taken)
    """
    node_count = [0]  # Using list to allow modification in nested function
    solutions = [0]
    
    def backtrack(board, row):
        node_count[0] += 1
        
        if row == n:
            solutions[0] += 1
            return
        
        for col in range(n):
            if is_safe(board, row, col, n):
                board[row] = col
                backtrack(board, row + 1)
                board[row] = -1
    
    board = [-1] * n
    start_time = time.time()
    backtrack(board, 0)
    end_time = time.time()
    
    return node_count[0], solutions[0], end_time - start_time


def print_board(board, n):
    """Print a chess board with queens placed."""
    for row in range(n):
        line = ""
        for col in range(n):
            if board[row] == col:
                line += "Q "
            else:
                line += ". "
        print(line)
    print()


def main():
    """Main function to run Monte Carlo estimation and compare with actual backtracking."""
    n = 12  # 12-Queens problem
    num_trials = 1000  # Number of Monte Carlo trials
    num_runs = 5  # Number of times to run the entire estimation
    
    # Set random seed for reproducibility (comment out for different results each run)
    random.seed(42)
    
    print("=" * 70)
    print("Monte Carlo Estimation for 12-Queens Problem")
    print("=" * 70)
    print(f"\nBoard Size: {n}x{n}")
    print(f"Number of Monte Carlo trials per run: {num_trials}")
    print(f"Number of runs: {num_runs}")
    print()
    
    # First, get the actual backtracking result for comparison
    print("-" * 70)
    print("Running Actual Backtracking Algorithm...")
    print("-" * 70)
    actual_nodes, solutions, bt_time = backtracking_count_nodes(n)
    print(f"Actual nodes visited by backtracking: {actual_nodes:,}")
    print(f"Number of solutions found: {solutions}")
    print(f"Backtracking execution time: {bt_time:.4f} seconds")
    print()
    
    # Run Monte Carlo estimation multiple times
    print("-" * 70)
    print("Running Monte Carlo Estimations...")
    print("-" * 70)
    
    all_estimates = []
    all_times = []
    
    for run in range(1, num_runs + 1):
        avg_estimate, estimates, avg_trial_time = monte_carlo_estimate(n, num_trials)
        all_estimates.append(avg_estimate)
        all_times.append(avg_trial_time)
        
        min_est = min(estimates)
        max_est = max(estimates)
        
        print(f"\nRun {run}:")
        print(f"  Average estimated nodes: {avg_estimate:,.0f}")
        print(f"  Min estimate: {min_est:,}")
        print(f"  Max estimate: {max_est:,}")
        print(f"  Average time per trial: {avg_trial_time * 1000:.4f} ms")
    
    # Summary statistics
    print()
    print("-" * 70)
    print("Summary Statistics")
    print("-" * 70)
    overall_avg = sum(all_estimates) / len(all_estimates)
    # Use sample variance (n-1) for statistical accuracy
    variance = sum((x - overall_avg) ** 2 for x in all_estimates) / (len(all_estimates) - 1)
    std_dev = variance ** 0.5
    
    print(f"\nActual nodes (backtracking): {actual_nodes:,}")
    print(f"Overall average estimate (Monte Carlo): {overall_avg:,.0f}")
    print(f"Standard deviation: {std_dev:,.0f}")
    print(f"Estimation error: {abs(overall_avg - actual_nodes) / actual_nodes * 100:.2f}%")
    print()
    
    # Time complexity analysis
    print("-" * 70)
    print("Time Complexity Analysis")
    print("-" * 70)
    print(f"\nBacktracking algorithm:")
    print(f"  - Visited {actual_nodes:,} nodes")
    print(f"  - Execution time: {bt_time:.4f} seconds")
    print(f"  - Time per node: {bt_time / actual_nodes * 1e6:.4f} microseconds")
    print()
    print(f"Monte Carlo estimation:")
    print(f"  - {num_trials} trials per run")
    print(f"  - Average time per trial: {sum(all_times) / len(all_times) * 1000:.4f} ms")
    print(f"  - Provides O(n) complexity per trial vs O(n!) worst case for backtracking")
    print()
    
    print("=" * 70)
    print("Conclusion")
    print("=" * 70)
    print(f"""
The Monte Carlo method estimates the backtracking tree size by randomly
sampling paths and extrapolating. For the {n}-Queens problem:

1. The backtracking algorithm explores {actual_nodes:,} nodes to find
   all {solutions} solutions.

2. The Monte Carlo estimation averages to approximately {overall_avg:,.0f}
   nodes with a standard deviation of {std_dev:,.0f}.

3. The time complexity of the backtracking algorithm is estimated to be
   O({actual_nodes:,}) for n={n}, which grows exponentially with n.

4. Monte Carlo provides a fast way to estimate this complexity without
   running the full backtracking algorithm.
""")
    
    print("=" * 70)
    print("Additional Runs for Statistical Confidence")
    print("=" * 70)
    
    # Run more trials for better statistical analysis
    print("\nRunning 10 additional Monte Carlo estimations...")
    additional_runs = 10
    additional_estimates = []
    
    for i in range(additional_runs):
        avg_est, _, _ = monte_carlo_estimate(n, num_trials)
        additional_estimates.append(avg_est)
        print(f"Run {i + 1}: Estimated nodes = {avg_est:,.0f}")
    
    total_estimates = all_estimates + additional_estimates
    final_avg = sum(total_estimates) / len(total_estimates)
    # Use sample variance (n-1) for statistical accuracy
    final_var = sum((x - final_avg) ** 2 for x in total_estimates) / (len(total_estimates) - 1)
    final_std = final_var ** 0.5
    
    print(f"\nFinal average (all {len(total_estimates)} runs): {final_avg:,.0f}")
    print(f"Final standard deviation: {final_std:,.0f}")
    print(f"Coefficient of variation: {final_std / final_avg * 100:.2f}%")
    print(f"Final estimation error: {abs(final_avg - actual_nodes) / actual_nodes * 100:.2f}%")


if __name__ == "__main__":
    main()
