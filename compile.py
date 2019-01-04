import subprocess, platform, os

lambda: os.system('cls' if os.name=='nt' else 'clear')

try:
    fh = open('build/launcher.exe', 'r')
    print("File launcher.exe exists. Overwrite? (y/N)")
    inp=input(": ")
    while inp.lower() != "y" or inp.lower() != "n":
        lambda: os.system('cls' if os.name=='nt' else 'clear')
    print("File launcher.exe exists. Overwrite? (y/N)")
    inp=input(": ")

except FileNotFoundError:
    pass

print("Building for "+platform.system())
cwd=os.getcwd()
p=subprocess.Popen('pyinstaller -y -F -w -i "'+cwd+'/favicon.ico" --add-data "'+cwd+'/dirt.png";"." --add-data "'+cwd+'/favicon.png";"." --add-data "'+cwd+'/logo.png";"." "launcher.py"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
    print(line)
retval = p.wait()