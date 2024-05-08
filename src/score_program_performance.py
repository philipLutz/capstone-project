"""
Score program performance results
Outputs a CSV file of the program name and the score value
"""

import csv
import math
import sys


PERFORMANCE_RESULTS_FILE = "program_performance_results.csv"
OUTPUT_FILE = "program_scores.csv"
RUNS_PER_PROGRAM = 3

SCORE_CLASS_MAPPING = {
    0: 1,
    1: 1,
    2: 2,
    3: 2,
    4: 2,
    5: 3,
    6: 3,
    7: 3,
}

def order_of_magnitude(num):
    if num == 0.0:
        return 0
    return math.floor(math.log(num, 10))

def compute_score(run: dict) -> float:
    """
    Given a vector of performance metrics, compute a single real number.

    Args:
        run (dict): single row of the performance results CSV file
    
    Returns:
        float: Larger values indicate the program is less affected by CPU frequency changes (less CPU-bound)
    """
    fields_to_ignore = [
        "program",
        "cache-misses-percent",
        "context-switches",
        "instructions-per-cycle",
        "elapsed",
        "user",
        "sys",

    ]
    
    max_block_time = 0
    most_frequent_block_time = 0
    most_frequent_block_time_count = 0
    for k, v in run.items():
        if k not in fields_to_ignore:
            low, high = k.split('-')
            average_block_time = (int(low) + int(high)) / 2
            if int(v) and average_block_time > max_block_time:
                max_block_time = average_block_time
            if int(v) >= most_frequent_block_time_count:
                most_frequent_block_time = average_block_time
                most_frequent_block_time_count = int(v)

    return (float(run['cache-misses-percent']) / float(run['instructions-per-cycle'])) * (most_frequent_block_time + max_block_time)


# main
score_results = {}

with open(PERFORMANCE_RESULTS_FILE, 'r', newline='') as results_file:
    reader = csv.DictReader(results_file)
    current_program = ""
    current_score = 0.0
    for row in reader:
        if row['program'][:-2] != current_program:
            real_score = current_score / RUNS_PER_PROGRAM
            score_results[current_program] = order_of_magnitude(real_score)
            # print("REAL: " + str(real_score))
            # print("ORDER: " + str(order_of_magnitude(real_score)))
            current_program = row['program'][:-2]
            current_score = 0.0
        current_score += compute_score(row)
    # final program needs added
    real_score = current_score / RUNS_PER_PROGRAM
    score_results[current_program] = order_of_magnitude(real_score)
    # empty starting entry needs deleted
    del score_results[""]

# Get the smallest order of magnitude so the first category is 1
minimum_order_of_magnitude = min(score_results.values())

with open(OUTPUT_FILE, 'w', newline='') as output_file:
    writer = csv.DictWriter(output_file, fieldnames=['program', 'score'])
    writer.writeheader()
    for k, v in score_results.items():
        writer.writerow({'program': k, 'score': SCORE_CLASS_MAPPING[(v + abs(minimum_order_of_magnitude))]})

        