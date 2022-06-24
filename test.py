import subprocess
password_ubuntu_input = 'epics4fau'
# print(subprocess.run(["wsl", "sudo", "-S", "<<<", f"{password_ubuntu_input}", "apt", "update"],
#                stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE))

test = subprocess.Popen(["wsl", "sudo", "-S", "<<<", f"{password_ubuntu_input}", "apt", "dist-upgrade", '-y'],  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

for line in iter(test.stdout.readline, b''):
    text = line.decode().rstrip()
    print(text)