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

cos=platform.system()

print("Building for "+cos)
cwd=os.getcwd()
if cos == "Linux":
    p=subprocess.Popen('pyinstaller -y -F -w -i "'+cwd+'/favicon.ico" --add-data "'+cwd+'/dirt.png":"." --add-data "'+cwd+'/favicon.png":"." --add-data "'+cwd+'/logo.png":"." "launcher.py"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
elif cos == "Windows":
    p=subprocess.Popen('pyinstaller -y -F -w -i "'+cwd+'/favicon.ico" --add-data "'+cwd+'/dirt.png";"." --add-data "'+cwd+'/favicon.png";"." --add-data "'+cwd+'/logo.png";"." "launcher.py"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
    print(line)
retval = p.wait()