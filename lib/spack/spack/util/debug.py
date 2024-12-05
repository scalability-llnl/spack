# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Debug signal handler: prints a stack trace and enters interpreter.

``register_interrupt_handler()`` enables a ctrl-C handler that prints
a stack trace and drops the user into an interpreter.

"""
import code
import io
import os
import pdb
import signal
import sys
import traceback


def debug_handler(sig, frame):
    """Interrupt running process, and provide a python prompt for
    interactive debugging."""
    d = {"_frame": frame}  # Allow access to frame object.
    d.update(frame.f_globals)  # Unless shadowed by global
    d.update(frame.f_locals)

    i = code.InteractiveConsole(d)
    message = "Signal received : entering python shell.\nTraceback:\n"
    message += "".join(traceback.format_stack(frame))
    i.interact(message)
    os._exit(1)  # Use os._exit to avoid test harness.


def register_interrupt_handler():
    """Print traceback and enter an interpreter on Ctrl-C"""
    signal.signal(signal.SIGINT, debug_handler)


# Subclass of the debugger to keep readline working.  See
# https://stackoverflow.com/questions/4716533/how-to-attach-debugger-to-a-python-subproccess/23654936
class ForkablePdb(pdb.Pdb):
    """
    This class allows the python debugger to follow forked processes
    and can set tracepoints allowing the Python Debugger Pdb to be used
    from a python multiprocessing child process.

    This is used the same way one would normally use Pdb, simply import this
    class and use as a drop in for Pdb, although the syntax here is slightly different,
    requiring the instantiton of this class, i.e. ForkablePdb().set_trace().

    This should be used when attempting to call a debugger from a
    child process spawned by the python multiprocessing such as during
    the run of Spack.install, or any where else Spack spawns a child process.
    """

    try:
        _original_stdin_fd = sys.stdin.fileno()
    except io.UnsupportedOperation:
        _original_stdin_fd = None
    _original_stdin = None

    def __init__(self, stdout_fd=None, stderr_fd=None):
        pdb.Pdb.__init__(self, nosigint=True)
        self._stdout_fd = stdout_fd
        self._stderr_fd = stderr_fd

    def _cmdloop(self):
        current_stdin = sys.stdin
        try:
            if not self._original_stdin:
                self._original_stdin = os.fdopen(self._original_stdin_fd)
            sys.stdin = self._original_stdin
            if self._stdout_fd is not None:
                os.dup2(self._stdout_fd, sys.stdout.fileno())
                os.dup2(self._stdout_fd, self.stdout.fileno())
            if self._stderr_fd is not None:
                os.dup2(self._stderr_fd, sys.stderr.fileno())
            self.cmdloop()
        finally:
            sys.stdin = current_stdin
