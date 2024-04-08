"""
Score program performance results
Outputs a CSV file of the program name and the score value
"""

import csv


PERFORMANCE_RESULTS_FILE = "program_performance_results.csv"
OUTPUT_FILE = "program_scores.csv"
RUNS_PER_PROGRAM = 3

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
            score_results[current_program] = current_score / RUNS_PER_PROGRAM
            current_program = row['program'][:-2]
            current_score = 0.0
        current_score += compute_score(row)
    # final program needs added
    score_results[current_program] = current_score / RUNS_PER_PROGRAM
    # empty starting entry needs deleted
    del score_results[""]

with open(OUTPUT_FILE, 'w', newline='') as output_file:
    writer = csv.DictWriter(output_file, fieldnames=['program', 'score'])
    writer.writeheader()
    for k, v in score_results.items():
        writer.writerow({'program': k, 'score': v})

        