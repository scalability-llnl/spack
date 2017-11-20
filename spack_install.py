import subprocess
import os

def install(spec):
    # Install the spec package if absent
    if "No package" in subprocess.check_output("spack find {}".format(spec), shell=True).decode("utf-8"):
        print("{} not found. Build it.".format(spec))
        os.system("spack install --restage {}".format(spec))

def check_pass(pkg, compiler, mpi, spec):
    if ('cuda' not in pkg) and ('+cuda' not in mpi): return True
    if ('+cuda' in pkg) and ('~cuda' in mpi): return False
    if ('~cuda' in pkg) and ('+cuda' in mpi): return False
    return True
