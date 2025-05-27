#This script parses device inforamation using Python and Paramiko
import paramiko

hostname = '192.168.83.100'
username = 'admin'
password = 'pfsense'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

commands = [
    'uptime',
    'hostname',
    'netstat -rn',
    'df -h',
    'ifconfig',
]

try:
    print("Connecting to pfSense...")
    ssh.connect(hostname, username=username, password=password)

    for cmd in commands:
        print(f"Executing command: {cmd}")
        stdin, stdout, stderr = ssh.exec_command(cmd)

        exit_status = stdout.channel.recv_exit_status()

        if exit_status == 0:
            output_lines = stdout.readlines()
            if output_lines:
                print("".join(output_lines))
            else:
                print("No output returned.")

        else:
            error_lines = stderr.readlines()
            print(f"Command failed with exit status {exit_status}.")
            print("".join(error_lines))
                
    ssh.close()
    print("Connection closed.")

except Exception as e:
    print(f"An error occurred: {e}")
