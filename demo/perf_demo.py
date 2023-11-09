import paramiko

# I need better example programs to test CPU-bound vs. memory-bound
COMMANDS = (
    # "perf stat -e cache-references,cache-misses,cycles,instructions -x \; ./empty-loop/loop",
    # "sudo perf stat -e cache-references,cache-misses,cycles:uk,instructions:uk,'block:*' ./empty-loop/loop",
    # "sudo perf stat -e cache-references:uk,cache-misses:uk,mem_access:uk,cycles:uk,instructions:uk ./empty-loop/loop",
    "sudo perf stat -e cache-references:uk,cache-misses:uk,mem_access:uk,context-switches:uk,cycles:uk,instructions:uk ./disk-write/disk",
    # "sudo perf stat -e cache-references:uk,cache-misses:uk,mem_access:uk,cycles:uk,instructions:uk ./digits-pi/pi",
    "sudo perf stat -e cache-references:uk,cache-misses:uk,mem_access:uk,context-switches:uk,cycles:uk,instructions:uk ./fibonacci/fibonacci",
    "sudo perf stat -e cache-references:uk,cache-misses:uk,mem_access:uk,context-switches:uk,cycles:uk,instructions:uk ./add/add",
)

def get_current_setting():
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
        # exit_code = stdout_raw.channel.recv_exit_status()
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


def run_command(command: str):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.load_system_host_keys()
        ssh_client.connect(hostname="10.0.0.165", username="philiplutz", password="raspberry")
        print("Executing:\n" + command)
        stdin_raw, stdout_raw, stderr_raw = ssh_client.exec_command(command)


        stderr = []
        for line in stderr_raw:
            stderr.append(line.strip())

        ssh_client.close()
        # https://github.com/paramiko/paramiko/issues/1078
        del ssh_client, stdin_raw, stdout_raw, stderr_raw

        print("Results:")
        for line in stderr:
            print(line)

    except Exception as e:
        print(e)
        try:
            ssh_client.close()
        except:
            pass


# main
get_current_setting()

for command in COMMANDS:
    run_command(command)

