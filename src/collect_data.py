"""
Collection Program Performance Data
"""

import csv
from time import sleep

import paramiko

# List of all programs that will be run and measured
COMMANDS = [
    # {'name': "add_100000", 'command': "./add/add 100000", 'process-name': "add"},
    {"name": "copy_1000", "command": "./copy-file/copy 1000", "process-name": "copy"},
    # {"name": "fib_naive_45", "command": "./fibonacci-naive/fibonacci 45", "process-name": "fibonacci"},
    # {"name": "fib_mem_100000000", "command": "./fibonacci-mem/fibonacci 100000000", "process-name": "fibonacci"},
    # {"name": "disk_write_1000000", "command": "./disk-write/disk 1000000", "process-name": "disk"},
]

def format_perf_stat(raw: [str]) -> dict:
    """
    """
    measurements = [
        "cache-references",
        "cache-misses",
        "mem_access",
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

    return results


def format_cpudist(raw: [str]) -> dict:
    """
    """

    results = {}
    raw_split = raw.splitlines()
    found = False
    for i in range(len(raw_split)):
        if found:
            line = raw_split[i].replace(" ", "")
            if not line.startswith("usecs"):
                stripped_line = line.strip("|*")
                k, v = stripped_line.split(":")
                print(f"key = {k}, value = {v}")
        if raw_split[i].startswith("^C"):
            found = True
        

    return results


def get_current_setting():
    """
    """
    # To change CPU governor policy, go to /etc/default/cpu_governor, uncomment the variable, and add the correct value
    # "sudo" must be used to edit file and then the system needs to be rebooted
    # "performance" statically runs the CPU at the highest frequency and for a default RPI4, that is 1.5GHz
    # "powersave" statically runs the CPU at the lowest frequency and for a default RPI4, that is 0.6GHz
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.load_system_host_keys()
        ssh_client.connect(hostname="10.0.0.165", username="philiplutz", password="raspberry")
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
    """
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.load_system_host_keys()
        ssh_client.connect(hostname="10.0.0.165", username="philiplutz", password="raspberry")
        print("Executing perf stat on:\n" + command['name'])
        stdin_raw, stdout_raw, stderr_raw = ssh_client.exec_command(
            f"sudo perf stat -e cache-references:uk,cache-misses:uk,mem_access:uk,context-switches:uk,cycles:uk,instructions:uk {command['command']}"
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
    """
    try:
        ssh_client_program = paramiko.SSHClient()
        ssh_client_program.load_system_host_keys()
        ssh_client_program.connect(hostname="10.0.0.165", username="philiplutz", password="raspberry")

        ssh_client_cpudist = paramiko.SSHClient()
        ssh_client_cpudist.load_system_host_keys()
        ssh_client_cpudist.connect(hostname="10.0.0.165", username="philiplutz", password="raspberry")

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


# main
get_current_setting()

for command in COMMANDS:
    # collect_perf_stat(command)
    collect_cpudist(command)

