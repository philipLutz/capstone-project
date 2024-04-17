"""
Collection Script for Program Performance Data
Assumes Raspberry Pi has test programs already compiled and is connected on local network
Outputs a CSV file with the on-CPU and off-CPU measurements of each program
"""

import csv
from time import sleep

import paramiko

# List of all programs that will be run and measured
COMMANDS = [
    {'name': "add", 'command': "./add/add 100000", 'process-name': "add"},
    {'name': "thread_add", 'command': "./thread-add/add 30000", 'process-name': "add"},
    {"name": "copy_file", "command": "./copy-file/copy 1000", "process-name": "copy"},
    {"name": "copy_file_o1", "command": "./copy-file-o1/copy 1000", "process-name": "copy"},
    {"name": "copy_file_o2", "command": "./copy-file-o2/copy 1000", "process-name": "copy"},
    {"name": "copy_file_o3", "command": "./copy-file-o3/copy 1000", "process-name": "copy"},
    {"name": "thread_copy_file", "command": "./thread-copy-file/copy 150", "process-name": "copy"},
    {"name": "thread_copy_file_o1", "command": "./thread-copy-file-o1/copy 150", "process-name": "copy"},
    {"name": "thread_copy_file_o2", "command": "./thread-copy-file-o2/copy 150", "process-name": "copy"},
    {"name": "thread_copy_file_o3", "command": "./thread-copy-file-o3/copy 150", "process-name": "copy"},
    {"name": "fibonacci_naive", "command": "./fibonacci-naive/fibonacci 45", "process-name": "fibonacci"},
    {"name": "fibonacci_naive_o1", "command": "./fibonacci-naive-o1/fibonacci 45", "process-name": "fibonacci"},
    {"name": "fibonacci_naive_o2", "command": "./fibonacci-naive-o2/fibonacci 47", "process-name": "fibonacci"},
    {"name": "fibonacci_naive_o3", "command": "./fibonacci-naive-o3/fibonacci 47", "process-name": "fibonacci"},
    {"name": "fibonacci_mem", "command": "./fibonacci-mem/fibonacci 100000000", "process-name": "fibonacci"},
    {"name": "disk_write", "command": "./disk-write/disk 1000000", "process-name": "disk"},
    {"name": "disk_write_o1", "command": "./disk-write-o1/disk 1000000", "process-name": "disk"},
    {"name": "disk_write_o2", "command": "./disk-write-o2/disk 1000000", "process-name": "disk"},
    {"name": "disk_write_o3", "command": "./disk-write-o3/disk 1000000", "process-name": "disk"},
    {"name": "thread_disk_write", "command": "./thread-disk-write/disk 500000", "process-name": "disk"},
    {"name": "thread_disk_write_o1", "command": "./thread-disk-write-o1/disk 500000", "process-name": "disk"},
    {"name": "thread_disk_write_o2", "command": "./thread-disk-write-o2/disk 500000", "process-name": "disk"},
    {"name": "thread_disk_write_o3", "command": "./thread-disk-write-o3/disk 500000", "process-name": "disk"},
    {"name": "prime_naive", "command": "./prime-naive/prime 20000000", "process-name": "prime"},
    {"name": "prime_naive_o1", "command": "./prime-naive-o1/prime 15000000", "process-name": "prime"},
    {"name": "prime_naive_o2", "command": "./prime-naive-o2/prime 15000000", "process-name": "prime"},
    {"name": "prime_naive_o3", "command": "./prime-naive-o3/prime 15000000", "process-name": "prime"},
    {"name": "thread_prime_naive", "command": "./thread-prime-naive/prime 40000000", "process-name": "prime"},
    {"name": "thread_prime_naive_o1", "command": "./thread-prime-naive-o1/prime 40000000", "process-name": "prime"},
    {"name": "thread_prime_naive_o2", "command": "./thread-prime-naive-o2/prime 40000000", "process-name": "prime"},
    {"name": "thread_prime_naive_o3", "command": "./thread-prime-naive-o3/prime 40000000", "process-name": "prime"},
    {"name": "prime_sieve", "command": "./prime-sieve/prime 500000000", "process-name": "prime"},
    {"name": "prime_sieve_o1", "command": "./prime-sieve-o1/prime 600000000", "process-name": "prime"},
    {"name": "prime_sieve_o2", "command": "./prime-sieve-o2/prime 600000000", "process-name": "prime"},
    {"name": "prime_sieve_o3", "command": "./prime-sieve-o3/prime 600000000", "process-name": "prime"},
    {"name": "bubble_sort_worst", "command": "./bubble-sort-worst/sort 50000", "process-name": "sort"},
    {"name": "bubble_sort_worst_o1", "command": "./bubble-sort-worst-o1/sort 100000", "process-name": "sort"},
    {"name": "bubble_sort_worst_o2", "command": "./bubble-sort-worst-o2/sort 100000", "process-name": "sort"},
    {"name": "bubble_sort_worst_o3", "command": "./bubble-sort-worst-o3/sort 120000", "process-name": "sort"},
    {"name": "bubble_sort_random", "command": "./bubble-sort-random/sort 50000", "process-name": "sort"},
    {"name": "bubble_sort_random_o1", "command": "./bubble-sort-random-o1/sort 80000", "process-name": "sort"},
    {"name": "bubble_sort_random_o2", "command": "./bubble-sort-random-o2/sort 80000", "process-name": "sort"},
    {"name": "bubble_sort_random_o3", "command": "./bubble-sort-random-o3/sort 80000", "process-name": "sort"},
    {"name": "qsort_worst", "command": "./qsort-worst/sort 100000000", "process-name": "sort"},
    {"name": "qsort_random", "command": "./qsort-random/sort 30000000", "process-name": "sort"},
    {"name": "string_resize_small", "command": "./string-resize-small/string 200000", "process-name": "string"},
    {"name": "thread_string_resize_small", "command": "./thread-string-resize-small/string 100000", "process-name": "string"},
    {'name': "multiply", 'command': "./multiply/multiply 1000000", 'process-name': "multiply"},
    {'name': "thread_multiply", 'command': "./thread-multiply/multiply 500000", 'process-name': "multiply"},
    {'name': "get_random_numbers", 'command': "./get-random-numbers/random 1000000", 'process-name': "random"},
    {'name': "thread_get_random_numbers", 'command': "./thread-get-random-numbers/random 5000000", 'process-name': "random"},
    {'name': "collatz", 'command': "./collatz/collatz 12000000", "process-name": "collatz"},
    {'name': "collatz_o1", 'command': "./collatz-o1/collatz 50000000", "process-name": "collatz"},
    {'name': "collatz_o2", 'command': "./collatz-o2/collatz 50000000", "process-name": "collatz"},
    {'name': "collatz_o3", 'command': "./collatz-o3/collatz 20000000", "process-name": "collatz"},
    # scratch counting sort, worst case
    # scratch counting sort, random
]

# List of all columns for CSV file
FIELDNAMES = [
    "program",
    "cache-misses-percent",
    "context-switches",
    "instructions-per-cycle",
    "elapsed",
    "user",
    "sys",
    "0-31",
    "32-63",
    "64-127",
    "128-255",
    "256-511",
    "512-1023",
    "1024-2047",
    "2048-4095",
    "4096-8191",
    "8192-16383",
    "16384-32767",
    "32768-65535",
    "65536-131071",
]

# SSH credentials
HOSTNAME = ""
USERNAME = ""
PASSWORD = ""
with open("ssh.txt", "r") as credentials:
    creds = []
    for line in credentials:
        creds.append((line.partition("=")[2]).strip())
    HOSTNAME, USERNAME, PASSWORD = creds

# Output CSV file name
OUTPUT_FILENAME = "program_performance_results.csv"


def format_perf_stat(raw: list[str]) -> dict:
    """
    Formats raw string output from perf stat to be used for csv.DictWriter

    Args:
        raw [str]: list of strings which are each line of the perf stat output

    Returns:
        dict: performance counter measurements and associated values
    """
    measurements = [
        "cache-references",
        "cache-misses",
        "context-switches",
        "cycles",
        "instructions",
        "elapsed",
        "user",
        "sys"
    ]

    results = {}
    for s in raw:
        line_result = s.split()
        if len(line_result) >= 2:
            for m in measurements:
                if line_result[1].startswith(m):
                    results[m] = int(line_result[0].replace(",", ""))
        if len(line_result) == 3:
            for m in measurements:
                if line_result[2].startswith(m):
                    results[m] = float(line_result[0].replace(",", ""))
        if len(line_result) == 4 and line_result[3].startswith("elapsed"):
            results['elapsed'] = float(line_result[0].replace(",", ""))

    results['cache-misses-percent'] = results['cache-misses'] / results['cache-references']
    del results['cache-misses']
    del results['cache-references']

    results['instructions-per-cycle'] = results['instructions'] / results['cycles']
    del results['instructions']
    del results['cycles']

    return results


def format_cpudist(raw: list[str]) -> dict:
    """
    Formats raw string output from cpudist-bpfcc to be used for csv.DictWriter

    Args:
        raw [str]: list of strings which are the lines of the captured shell output

    Returns:
        dict: off-CPU times, key is length of time in microseconds, value is count of occurrence 
    """
    measurements = [
        "0-1",
        "2-3",
        "4-7",
        "8-15",
        "16-31",
        "32-63",
        "64-127",
        "128-255",
        "256-511",
        "512-1023",
        "1024-2047",
        "2048-4095",
        "4096-8191",
        "8192-16383",
        "16384-32767",
        "32768-65535",
        "65536-131071",
    ]

    results = {}
    raw_split = raw.splitlines()
    found = False
    for i in range(len(raw_split)):
        if found:
            line = raw_split[i].replace(" ", "")
            if not line.startswith("usecs"):
                stripped_line = line.strip("|*")
                k, v = stripped_line.split(":")
                results[k.replace(">", "")] = v
        if raw_split[i].startswith("^C"):
            found = True

    for k in list(results.keys()):
        if k not in measurements:
            del results[k]

    for f in measurements:
        if f not in list(results.keys()):
            results[f] = 0

    for k in list(results.keys()):
        results[k] = int(results[k])

    results['0-31'] = results['0-1'] + results['2-3'] + results['4-7'] + results['8-15'] + results['16-31']
    del results['0-1']
    del results['2-3']
    del results['4-7']
    del results['8-15']
    del results['16-31']

    return results


def get_current_setting():
    """
    Print the current CPU governor settings on the Raspberry Pi

    To change CPU governor policy, go to /etc/default/cpu_governor, uncomment the variable, and add the correct value
    "sudo" must be used to edit file and then the system needs to be rebooted
    "performance" statically runs the CPU at the highest frequency and for a default RPI4, that is 1.5GHz
    "powersave" statically runs the CPU at the lowest frequency and for a default RPI4, that is 0.6GHz
    """
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.load_system_host_keys()
        ssh_client.connect(hostname=HOSTNAME, username=USERNAME, password=PASSWORD)
        stdin_raw, stdout_raw, stderr_raw = ssh_client.exec_command(
            "cat /sys/devices/system/cpu/cpufreq/policy0/scaling_governor"
        )
        
        print("CPU GOVERNOR POLICY:")
        for line in stdout_raw:
            print(line)

        stdin_raw, stdout_raw, stderr_raw = ssh_client.exec_command("vcgencmd measure_clock arm")
        print("CPU FREQUENCY:")
        for line in stdout_raw:
            print(line)

        ssh_client.close()
        del ssh_client, stdin_raw, stdout_raw, stderr_raw

    except Exception as e:
        print(e)
        try:
            ssh_client.close()
        except:
            pass


def collect_perf_stat(command: dict) -> dict:
    """
    Connect over SSH and run perf stat on a test program
    Test program must terminate

    Args:
        command (dict): name, command, and process name of program to measure

    Returns:
        dict: performance counter measurements and associated values
    """
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.load_system_host_keys()
        ssh_client.connect(hostname=HOSTNAME, username=USERNAME, password=PASSWORD)
        print("Executing perf stat on:\n" + command['name'])
        stdin_raw, stdout_raw, stderr_raw = ssh_client.exec_command(
            f"sudo perf stat -e cache-references:uk,cache-misses:uk,context-switches:uk,cycles:uk,instructions:uk {command['command']}"
        )

        stderr = []
        for line in stderr_raw:
            stderr.append(line.strip())

        ssh_client.close()
        # https://github.com/paramiko/paramiko/issues/1078
        del ssh_client, stdin_raw, stdout_raw, stderr_raw

        return format_perf_stat(stderr)

    except Exception as e:
        print(e)
        try:
            ssh_client.close()
        except:
            pass
        return {}


def collect_cpudist(command: dict) -> dict:
    """
    Connect over SSH with two connections, measure test program with cpudist-bpfcc
    Test program must run for minimum of 30 seconds, process will be killed

    Args:
        command (dict): name, command, and process name of program to measure

    Returns:
        dict: off-CPU times, key is length of time in microseconds, value is count of occurrence 
    """
    try:
        ssh_client_program = paramiko.SSHClient()
        ssh_client_program.load_system_host_keys()
        ssh_client_program.connect(hostname=HOSTNAME, username=USERNAME, password=PASSWORD)

        ssh_client_cpudist = paramiko.SSHClient()
        ssh_client_cpudist.load_system_host_keys()
        ssh_client_cpudist.connect(hostname=HOSTNAME, username=USERNAME, password=PASSWORD)

        print("Executing cpudist-bpfcc on:\n" + command['name'])
        # start program that will be measured
        ssh_client_program.exec_command(command['command'])
        # in a separate SSH connection, start cpudist-bpfcc
        shell = ssh_client_cpudist.invoke_shell()
        shell.send(f"sudo cpudist-bpfcc -O -p $(pgrep -nx {command['process-name']})\n")

        # cpudist-bpfcc takes a few seconds to start measuring the target process
        # the target process should run for at least 45 seconds
        sleep(45)
        # send "Control-C" keyboard interrupt to stop cpudist-bpfcc execution
        shell.send('\x03')
        # wait a few seconds for the shell to write the output
        sleep(5)
        result = shell.recv(2000).decode()
        # stop the target process because it is no longer being measured
        ssh_client_program.exec_command(f"kill -9 $(pgrep -nx {command['process-name']})")

        ssh_client_cpudist.close()
        ssh_client_program.close()

        return format_cpudist(result)

    except Exception as e:
        print(e)
        try:
            ssh_client_program.close()
            ssh_client_cpudist.close()
        except:
            pass
        return {}


def collect_results(command: dict) -> dict:
    """
    Run perf stat and cpudist-bpfcc on target

    Args:
        command (dict): name, command, and process name of program to measure

    Returns:
        dict: performance measurements and associated values
    """
    results = {"program": command["name"]}
    results.update(collect_perf_stat(command))
    results.update(collect_cpudist(command))
    return results

# main
get_current_setting()

# Check if file contains the header row, otherwise write it
try:    
    with open(OUTPUT_FILENAME, 'r+', newline='') as csvfile:
        print("reading existing file")
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            try:
                if row[0] != "program":
                    print("writing header on existing file")
                    writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
                    writer.writeheader()
                break
            except(IndexError):
                print("writing header on existing file")
                writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
                writer.writeheader()
        if reader.line_num == 0:
            print("writing header on existing file")
            writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
            writer.writeheader()
except(FileNotFoundError):
    with open(OUTPUT_FILENAME, 'w', newline='') as csvfile:
        print("writing header in new file")
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
        writer.writeheader()

# Check if program performance results have already been collected, otherwise run and append results
for command in COMMANDS:
    contains_program_result = False
    with open(OUTPUT_FILENAME, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if command['name'] in row[0]:
                contains_program_result = True
                break

    if not contains_program_result:
        with open(OUTPUT_FILENAME, 'a', newline='') as csvfile:
            print(f"need to run {command['name']}")
            # Multiple executions of each test program
            for i in range(3):
                results = collect_results(command)
                results["program"] += f"_{i+1}"
                writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
                writer.writerow(results)
                
