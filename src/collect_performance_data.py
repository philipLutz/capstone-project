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
    {'name': "add_100000", 'command': "./add/add 100000", 'process-name': "add"},
    {"name": "copy_1000", "command": "./copy-file/copy 1000", "process-name": "copy"},
    {"name": "fib_naive_45", "command": "./fibonacci-naive/fibonacci 45", "process-name": "fibonacci"},
    {"name": "fib_mem_100000000", "command": "./fibonacci-mem/fibonacci 100000000", "process-name": "fibonacci"},
    {"name": "disk_write_1000000", "command": "./disk-write/disk 1000000", "process-name": "disk"},
    {"name": "prime_naive_20000000", "command": "./prime-naive/prime 20000000", "process-name": "prime"},
    {"name": "prime_sieve_500000000", "command": "./prime-sieve/prime 500000000", "process-name": "prime"},
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
        # the target process should run for at least 30 seconds
        sleep(25)
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

with open('program_results.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
    writer.writeheader()

    for command in COMMANDS:
        # Multiple executions of each test program
        for i in range(2):
            results = collect_results(command)
            results["program"] += f"_{i+1}"
            writer.writerow(results)

