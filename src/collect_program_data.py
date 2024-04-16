"""
Collection Script for Static Analysis Data
Frama-C Metrics is run on each program's source code
"""

import csv
import os
import subprocess


# Fieldnames for CSV file
FIELDNAMES = [
    "program",
    "total-operators",
    "distinct-operators",
    "total-operands",
    "distinct-operands",
    "function-calls",
    "loops",
    "assignments",
    "max-cyclomatic-complexity",
    "sum-cyclomatic-complexity",
    "dynamic-memory-calls",
    "file-access",
    "file-operation",
    "file-position",
    "file-error",
    "input-output",
    "optimization",
]

# Mappings of Frama-c names to fieldnames for CSV file
MAPPING = {
    "Total operators": "total-operators",
    "Distinct operators": "distinct-operators",
    "Total_operands": "total-operands",
    "Distinct operands": "distinct-operands",
    "Function call": "function-calls",
    "Loop": "loops",
    "Assignment": "assignments",
    "Cyclomatic complexity": "sum-cyclomatic-complexity",
    "malloc": "dynamic-memory-calls",
    "aligned_alloc": "dynamic-memory-calls",
    "realloc": "dynamic-memory-calls",
    "calloc": "dynamic-memory-calls",
    "free": "dynamic-memory-calls",
    "fopen": "file-access",
    "freopen": "file-access",
    "fflush": "file-access",
    "fclose": "file-access",
    "setbuf": "file-access",
    "setvbuf": "file-access",
    "fwide": "file-access",
    "remove": "file-operation",
    "rename": "file-operation",
    "tmpfile": "file-operation",
    "tmpnam": "file-operation",
    "ftell": "file-position",
    "fseek": "file-position",
    "fgetpos": "file-position",
    "fsetpos": "file-position",
    "rewind": "file-position",
    "clearerr": "file-error",
    "feof": "file-error",
    "ferror": "file-error",
    "fread": "input-output",
    "fwrite": "input-output",
    "fgetc": "input-output",
    "fgetwc": "input-output",
    "getc": "input-output",
    "getwc": "input-output",
    "fgets": "input-output",
    "fgetws": "input-output",
    "fputc": "input-output",
    "fputwc": "input-output",
    "putc": "input-output",
    "putwc": "input-output",
    "fputs": "input-output",
    "fputws": "input-output",
    "getchar": "input-output",
    "getwchar": "input-output",
    "gets": "input-output",
    "putchar": "input-output",
    "putwchar": "input-output",
    "puts": "input-output",
    "ungetc": "input-output",
    "ungetwc": "input-output",
    "scanf": "input-output",
    "wscanf": "input-output",
    "fscanf": "input-output",
    "fwscanf": "input-output",
    "sscanf": "input-output",
    "swscanf": "input-output",
    "vscanf": "input-output",
    "vwscanf": "input-output",
    "vfscanf": "input-output",
    "vfwscanf": "input-output",
    "vsscanf": "input-output",
    "vswscanf": "input-output",
    "printf": "input-output",
    "wprintf": "input-output",
    "fprintf": "input-output",
    "fwprintf": "input-output",
    "sprintf": "input-output",
    "swprintf": "input-output",
    "snprintf": "input-output",
    "vprintf": "input-output",
    "vwprintf": "input-output",
    "vfprintf": "input-output",
    "vfwprintf": "input-output",
    "vsprintf": "input-output",
    "vswprintf": "input-output",
    "vsnprintf": "input-output",
    "perror": "input-output",
}


def collect_static_metrics(program: str) -> dict:
    """
    Run Frama-C Metrics tool on C program source code

    Args:
        program (str): path to program source code

    Returns:
        dict: static analysis metrics from Frama-c
    """
    metrics = {"max-cyclomatic-complexity": -1}

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

    lines = frama_c_result.stdout.splitlines()
    # frama-c output metrics have '=' as the separator for key/value pairs in beginning and ':' for the rest
    split_character_change = False
    for i in range(len(lines)):
        if "[metrics] Halstead metrics" in lines[i]:
            split_character_change = True
        for k, v in MAPPING.items():
            if k in lines[i]:
                try:
                    if split_character_change:
                        s_k, s_v = lines[i].split(":")
                    else:
                        s_k, s_v = lines[i].split("=")
                    if k == s_k.strip():
                        if k == "Cyclomatic complexity":
                            if metrics['max-cyclomatic-complexity'] < int(s_v):
                                metrics['max-cyclomatic-complexity'] = int(s_v)
                        if v in metrics:
                            metrics[v] += int(s_v)
                        else:
                            metrics[v] = int(s_v)
                except(ValueError):
                    pass
            
    return metrics


# main
with open('static_analysis_results.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
    writer.writeheader()

    for root, dirs, files in os.walk("test-programs"):
        for file in files:
            if ".c" in file:
                print(root)
                results = {"program": root.split('/')[1].replace('-', '_')}
                if "_o" in results['program'][-3:]:
                    results['optimization'] = int(results['program'][-1])
                else:
                    results['optimization'] = 0
                results.update(collect_static_metrics((root + "/" + file)))
                writer.writerow(results)

