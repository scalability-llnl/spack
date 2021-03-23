# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import os
import sys
import code
import argparse
import platform
import runpy

import llnl.util.tty as tty

import spack

description = "launch an interpreter as spack would launch a command"
section = "developer"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '-V', '--version', action='store_true',
        help='print the Python version number and exit')
    subparser.add_argument(
        '-c', dest='python_command', help='command to execute')
    subparser.add_argument(
        '-i', dest='python_interpreter', help='python interpreter',
        choices=['python', 'ipython'], default='python')
    subparser.add_argument(
        '-m', dest='module', action='store',
        help='run library module as a script')
    subparser.add_argument(
        '--path', action='store_true', dest='show_path',
        help='show path to python interpreter that spack uses')
    subparser.add_argument(
        'python_args', nargs=argparse.REMAINDER,
        help="file to run plus arguments")


def python(parser, args, unknown_args):
    if args.version:
        print('Python', platform.python_version())
        return

    if args.show_path:
        print(sys.executable)
        return

    if args.module:
        sys.argv = ['spack-python'] + unknown_args + args.python_args
        runpy.run_module(args.module, run_name="__main__", alter_sys=True)
        return

    if unknown_args:
        tty.die("Unknown arguments:", " ".join(unknown_args))

    # Unexpected behavior from supplying both
    if args.python_command and args.python_args:
        tty.die("You can only specify a command OR script, but not both.")

    # Run user choice of interpreter
    if args.python_interpreter == "ipython":
        return spack.cmd.python.ipython_interpreter(args)
    return spack.cmd.python.python_interpreter(args)


def ipython_interpreter(args):
    """An ipython interpreter is intended to be interactive, so it doesn't
    support running a script or arguments
    """
    try:
        import IPython
    except ImportError:
        tty.die("ipython is not installed, install and try again.")

    if "PYTHONSTARTUP" in os.environ:
        startup_file = os.environ["PYTHONSTARTUP"]
        if os.path.isfile(startup_file):
            with open(startup_file) as startup:
                exec(startup.read())

    # IPython can also support running a script OR command, not both
    if args.python_args:
        IPython.start_ipython(argv=args.python_args)
    elif args.python_command:
        IPython.start_ipython(argv=['-c', args.python_command])
    else:
        header = ("Spack version %s\nPython %s, %s %s"
                  % (spack.spack_version, platform.python_version(),
                     platform.system(), platform.machine()))

        __name__ = "__main__"  # noqa
        IPython.embed(module="__main__", header=header)


def python_interpreter(args):
    """A python interpreter is the default interpreter
    """
    # Fake a main python shell by setting __name__ to __main__.
    console = code.InteractiveConsole({'__name__': '__main__',
                                       'spack': spack})
    if "PYTHONSTARTUP" in os.environ:
        startup_file = os.environ["PYTHONSTARTUP"]
        if os.path.isfile(startup_file):
            with open(startup_file) as startup:
                console.runsource(startup.read(), startup_file, 'exec')

    if args.python_command:
        console.runsource(args.python_command)
    elif args.python_args:
        sys.argv = args.python_args
        with open(args.python_args[0]) as file:
            console.runsource(file.read(), args.python_args[0], 'exec')
    else:
        # Provides readline support, allowing user to use arrow keys
        console.push('import readline')

        console.interact("Spack version %s\nPython %s, %s %s"
                         % (spack.spack_version, platform.python_version(),
                            platform.system(), platform.machine()))
