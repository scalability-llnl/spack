# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""The pty module handles pseudo-terminals.

Currently, the infrastructure here is only used to test llnl.util.tty.log.

If this is used outside a testing environment, we will want to reconsider
things like timeouts in ``ProcessController.wait()``, which are set to
get tests done quickly, not to avoid high CPU usage.

Note: The functionality in this module is unsupported on Windows
"""
import multiprocessing
import os
import re
import signal
import sys
import time
import traceback

import llnl.util.tty.log as log

from spack.util.executable import which

termios = None
try:
    import termios as term_mod

    termios = term_mod
except ImportError:
    pass


class ProcessController:
    """Wrapper around some fundamental process control operations.

    This allows one process (the controller) to drive another (the
    minion) similar to the way a shell would, by sending signals and I/O.

    """

    def __init__(self, pid, controller_fd, timeout=1, sleep_time=1e-1, debug=False):
        """Create a controller to manipulate the process with id ``pid``

        Args:
            pid (int): id of process to control
            controller_fd (int): controller fd attached to pid's stdin
            timeout (int): time in seconds for wait operations to time out
                (default 1 second)
            sleep_time (int): time to sleep after signals, to control the
                signal rate of the controller (default 1e-1)
            debug (bool): whether ``horizontal_line()`` and ``status()`` should
                produce output when called (default False)

        ``sleep_time`` allows the caller to insert delays after calls
        that signal or modify the controlled process. Python behaves very
        poorly if signals arrive too fast, and drowning a Python process
        with a Python handler with signals can kill the process and hang
        our tests, so we throttle this a closer-to-interactive rate.

        """
        self.pid = pid
        self.pgid = os.getpgid(pid)
        self.controller_fd = controller_fd
        self.timeout = timeout
        self.sleep_time = sleep_time
        self.debug = debug

        # we need the ps command to wait for process statuses
        self.ps = which("ps", required=True)

    def get_canon_echo_attrs(self):
        """Get echo and canon attributes of the terminal of controller_fd."""
        cfg = termios.tcgetattr(self.controller_fd)
        return (bool(cfg[3] & termios.ICANON), bool(cfg[3] & termios.ECHO))

    def horizontal_line(self, name):
        """Labled horizontal line for debugging."""
        if self.debug:
            sys.stderr.write("------------------------------------------- %s\n" % name)

    def status(self):
        """Print debug message with status info for the minion."""
        if self.debug:
            canon, echo = self.get_canon_echo_attrs()
            sys.stderr.write(
                "canon: %s, echo: %s\n" % ("on" if canon else "off", "on" if echo else "off")
            )
            sys.stderr.write("input: %s\n" % self.input_on())
            sys.stderr.write("bg: %s\n" % self.background())
            sys.stderr.write("\n")

    def input_on(self):
        """True if keyboard input is enabled on the controller_fd pty."""
        return self.get_canon_echo_attrs() == (False, False)

    def background(self):
        """True if pgid is in a background pgroup of controller_fd's tty."""
        return self.pgid != os.tcgetpgrp(self.controller_fd)

    def tstp(self):
        """Send SIGTSTP to the controlled process."""
        self.horizontal_line("tstp")
        os.killpg(self.pgid, signal.SIGTSTP)
        time.sleep(self.sleep_time)

    def cont(self):
        self.horizontal_line("cont")
        os.killpg(self.pgid, signal.SIGCONT)
        time.sleep(self.sleep_time)

    def fg(self):
        self.horizontal_line("fg")
        with log.ignore_signal(signal.SIGTTOU):
            os.tcsetpgrp(self.controller_fd, os.getpgid(self.pid))
        time.sleep(self.sleep_time)

    def bg(self):
        self.horizontal_line("bg")
        with log.ignore_signal(signal.SIGTTOU):
            os.tcsetpgrp(self.controller_fd, os.getpgrp())
        time.sleep(self.sleep_time)

    def write(self, byte_string):
        self.horizontal_line("write '%s'" % byte_string.decode("utf-8"))
        os.write(self.controller_fd, byte_string)

    def wait(self, condition):
        start = time.time()
        while ((time.time() - start) < self.timeout) and not condition():
            time.sleep(1e-2)
        assert condition()

    def wait_enabled(self):
        self.wait(lambda: self.input_on() and not self.background())

    def wait_disabled(self):
        self.wait(lambda: not self.input_on() and self.background())

    def wait_disabled_fg(self):
        self.wait(lambda: not self.input_on() and not self.background())

    def proc_status(self):
        status = self.ps("-p", str(self.pid), "-o", "stat", output=str)
        status = re.split(r"\s+", status.strip(), re.M)
        return status[1]

    def wait_stopped(self):
        self.wait(lambda: "T" in self.proc_status())

    def wait_running(self):
        self.wait(lambda: "T" not in self.proc_status())


class PseudoShell:
    """Sets up controller and minion processes with a PTY.

    You can create a ``PseudoShell`` if you want to test how some
    function responds to terminal input.  This is a pseudo-shell from a
    job control perspective; ``controller_function`` and ``minion_function``
    are set up with a pseudoterminal (pty) so that the controller can drive
    the minion through process control signals and I/O.

    The two functions should have signatures like this::

        def controller_function(proc, ctl, **kwargs)
        def minion_function(**kwargs)

    ``controller_function`` is spawned in its own process and passed three
    arguments:

    proc
        the ``multiprocessing.Process`` object representing the minion
    ctl
        a ``ProcessController`` object tied to the minion
    kwargs
        keyword arguments passed from ``PseudoShell.start()``.

    ``minion_function`` is only passed ``kwargs`` delegated from
    ``PseudoShell.start()``.

    The ``ctl.controller_fd`` will have its ``controller_fd`` connected to
    ``sys.stdin`` in the minion process. Both processes will share the
    same ``sys.stdout`` and ``sys.stderr`` as the process instantiating
    ``PseudoShell``.

    Here are the relationships between processes created::

        ._________________________________________________________.
        | Minion Process                                          | pid     2
        | - runs minion_function                                  | pgroup  2
        |_________________________________________________________| session 1
            ^
            | create process with controller_fd connected to stdin
            | stdout, stderr are the same as caller
        ._________________________________________________________.
        | Controller Process                                      | pid     1
        | - runs controller_function                              | pgroup  1
        | - uses ProcessController and controller_fd to           | session 1
        |   control minion                                        |
        |_________________________________________________________|
            ^
            | create process
            | stdin, stdout, stderr are the same as caller
        ._________________________________________________________.
        | Caller                                                  |  pid     0
        | - Constructs, starts, joins PseudoShell                 |  pgroup  0
        | - provides controller_function, minion_function         |  session 0
        |_________________________________________________________|

    """

    def __init__(self, controller_function, minion_function):
        self.proc = None
        self.controller_function = controller_function
        self.minion_function = minion_function

        # these can be optionally set to change defaults
        self.controller_timeout = 3
        self.sleep_time = 0.1

    def start(self, **kwargs):
        """Start the controller and minion processes.

        Arguments:
            kwargs (dict): arbitrary keyword arguments that will be
                passed to controller and minion functions

        The controller process will create the minion, then call
        ``controller_function``.  The minion process will call
        ``minion_function``.

        """
        self.proc = multiprocessing.Process(
            target=PseudoShell._set_up_and_run_controller_function,
            args=(
                self.controller_function,
                self.minion_function,
                self.controller_timeout,
                self.sleep_time,
            ),
            kwargs=kwargs,
        )
        self.proc.start()

    def join(self):
        """Wait for the minion process to finish, and return its exit code."""
        self.proc.join()
        return self.proc.exitcode

    @staticmethod
    def _set_up_and_run_minion_function(
        tty_name, stdout_fd, stderr_fd, ready, minion_function, **kwargs
    ):
        """Minion process wrapper for PseudoShell.

        Handles the mechanics of setting up a PTY, then calls
        ``minion_function``.

        """
        # new process group, like a command or pipeline launched by a shell
        os.setpgrp()

        # take controlling terminal and set up pty IO
        stdin_fd = os.open(tty_name, os.O_RDWR)
        os.dup2(stdin_fd, sys.stdin.fileno())
        os.dup2(stdout_fd, sys.stdout.fileno())
        os.dup2(stderr_fd, sys.stderr.fileno())
        os.close(stdin_fd)

        if kwargs.get("debug"):
            sys.stderr.write("minion: stdin.isatty(): %s\n" % sys.stdin.isatty())

        # tell the parent that we're really running
        if kwargs.get("debug"):
            sys.stderr.write("minion: ready!\n")
        ready.value = True

        try:
            minion_function(**kwargs)
        except BaseException:
            traceback.print_exc()

    @staticmethod
    def _set_up_and_run_controller_function(
        controller_function, minion_function, controller_timeout, sleep_time, **kwargs
    ):
        """Set up a pty, spawn a minion process, execute controller_function.

        Handles the mechanics of setting up a PTY, then calls
        ``controller_function``.

        """
        os.setsid()  # new session; this process is the controller

        controller_fd, minion_fd = os.openpty()
        pty_name = os.ttyname(minion_fd)

        # take controlling terminal
        pty_fd = os.open(pty_name, os.O_RDWR)
        os.close(pty_fd)

        ready = multiprocessing.Value("i", False)
        minion_process = multiprocessing.Process(
            target=PseudoShell._set_up_and_run_minion_function,
            args=(pty_name, sys.stdout.fileno(), sys.stderr.fileno(), ready, minion_function),
            kwargs=kwargs,
        )
        minion_process.start()

        # wait for subprocess to be running and connected.
        while not ready.value:
            time.sleep(1e-5)
            pass

        if kwargs.get("debug"):
            sys.stderr.write("pid:        %d\n" % os.getpid())
            sys.stderr.write("pgid:       %d\n" % os.getpgrp())
            sys.stderr.write("sid:        %d\n" % os.getsid(0))
            sys.stderr.write("tcgetpgrp:  %d\n" % os.tcgetpgrp(controller_fd))
            sys.stderr.write("\n")

            minion_pgid = os.getpgid(minion_process.pid)
            sys.stderr.write("minion pid:  %d\n" % minion_process.pid)
            sys.stderr.write("minion pgid: %d\n" % minion_pgid)
            sys.stderr.write("minion sid:  %d\n" % os.getsid(minion_process.pid))
            sys.stderr.write("\n")
            sys.stderr.flush()
        # set up controller to ignore SIGTSTP, like a shell
        signal.signal(signal.SIGTSTP, signal.SIG_IGN)

        # call the controller function once the minion is ready
        try:
            controller = ProcessController(
                minion_process.pid, controller_fd, debug=kwargs.get("debug")
            )
            controller.timeout = controller_timeout
            controller.sleep_time = sleep_time
            error = controller_function(minion_process, controller, **kwargs)
        except BaseException:
            error = 1
            traceback.print_exc()

        minion_process.join()

        # return whether either the parent or minion failed
        return error or minion_process.exitcode
