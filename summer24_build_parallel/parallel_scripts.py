import subprocess
from subprocess import call
import multiprocessing
from multiprocessing import Pool
import os
import sys

# var for bash commands from scripts
commands = []

# gets the executable commands from each script
# sets the env variables in an os.environ dict
def get_call(file):
    wdir = "cd ."
    with open(file) as f:
        for line in f:
            if line.startswith("#"):
                next
            elif line.startswith(" "):
                next
            elif line.startswith("export"): 
                 words = line.split()
                 if len(words) > 2:
                     pair = line.split(" ", 1)
                     val = pair[1].split('=', 1)
                     key = val[0]
                     val = val[1].rstrip(';\n"').strip('"')
                     os.environ[key] = val
                 else: 
                    rel = words[1].split()
                    pair = rel[0].split('=')
                    key = pair[0]
                    val = pair[1]
                    val = val[:-1]
                    os.environ[key] = val 
            elif line.startswith("unset"):
                words = line.split()
                var = words[1]
                var = var[:-1]
                if var in os.environ:
                    del os.environ[var]
                else:
                    next
            elif line.startswith("cd"):
                wdir = line.strip()
            else:
               commands.append(wdir+"; "+line.rstrip())

# calls and performs commands
def my_call(cmd):
    call(cmd,shell=True)

#def run_pool():
directory = './build_scripts'
files = sorted(os.listdir(directory))
index = 0
while index < len(files):
    filename = files[index]
    print("current file:", filename)
    if filename.endswith('.sh'):
        filepath = os.path.join(directory, filename)
        get_call(filepath)
        # distributes list to call function across (x) processes
        with Pool(25) as pool: #int(sys.argv[1])
            pool.map(my_call, commands)
        # reset the commands list
        commands.clear()
        index += 1
