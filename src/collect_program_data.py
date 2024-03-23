"""
Collection Script for Static Analysis Data
Frama-C Metrics is run on each program's source code
"""

import csv
import os
import subprocess

# Mappings of Frama-c names to fieldnames for CSV file
MAPPING = {
    "Total operators": "total-operators",
    "Distinct operators": "distinct-operators",
    "Total_operands": "total-operands",
    "Distinct operands": "distinct-operands",
    "Function call": "sum-function-calls",
    "Loop": "sum-loops",
    "Assignment": "sum-assignment",
    "Cyclomatic complexity": "sum-cyclomatic-complexity",
}


def collect_static_metrics(program: str) -> dict:
    """

    """
    metrics = {}

    frama_c_result = subprocess.run(
        [
            "/Users/philiplutz/.opam/4.14.1/bin/frama-c",
            "-metrics",
            "-metrics-by-function",
            "-metrics-ast",
            "cabs",
            program
        ],
        capture_output=True,
        text=True,
    )

    # print(frama_c_result.stdout)
    
    for s in frama_c_result.stdout.splitlines():
        for k, v in MAPPING.items():
            if k in s:
                print(s)
                if (k == "Function call"
                    or k == "Loop"
                    or k == "Assignment"
                    or k == "Cyclomatic complexity"):
                    s_k, s_v = s.split("=")
                    if v in metrics:
                        metrics[v] += int(s_v)
                    else:
                        metrics[v] = int(s_v)
                else:
                    s_k, s_v = s.split(":")
                    metrics[v] = int(s_v)


    return metrics

# print(collect_static_metrics("test-programs/add/add.c"))


# main

for root, dirs, files in os.walk("test-programs"):
    for file in files:
        if ".c" in file:
            print(root, dirs, files)
            print(collect_static_metrics((root + "/" + file)))

