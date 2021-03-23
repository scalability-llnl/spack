# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function
import contextlib
import multiprocessing
import os
import signal
import sys
import time

from typing import Optional  # novm
from types import ModuleType  # novm

import pytest

import llnl.util.tty.log
from llnl.util.lang import uniq
from llnl.util.tty.log import log_output
from llnl.util.tty.pty import PseudoShell

from spack.util.executable import which

termios = None  # type: Optional[ModuleType]
try:
    import termios as term_mod
    termios = term_mod
except ImportError:
    pass


@contextlib.contextmanager
def nullcontext():
    yield


def test_log_python_output_with_echo(capfd, tmpdir):
    with tmpdir.as_cwd():
        with log_output('foo.txt', echo=True):
            print('logged')

        # foo.txt has output
        with open('foo.txt') as f:
            assert f.read() == 'logged\n'

        # output is also echoed.
        assert capfd.readouterr()[0] == 'logged\n'


def test_log_python_output_without_echo(capfd, tmpdir):
    with tmpdir.as_cwd():
        with log_output('foo.txt'):
            print('logged')

        # foo.txt has output
        with open('foo.txt') as f:
            assert f.read() == 'logged\n'

        # nothing on stdout or stderr
        assert capfd.readouterr()[0] == ''


def test_log_python_output_and_echo_output(capfd, tmpdir):
    with tmpdir.as_cwd():
        # echo two lines
        with log_output('foo.txt') as logger:
            with logger.force_echo():
                print('force echo')
            print('logged')

        # log file contains everything
        with open('foo.txt') as f:
            assert f.read() == 'force echo\nlogged\n'

        # only force-echo'd stuff is in output
        assert capfd.readouterr()[0] == 'force echo\n'


@pytest.mark.skipif(not which('echo'), reason="needs echo command")
def test_log_subproc_and_echo_output_no_capfd(capfd, tmpdir):
    echo = which('echo')

    # this is split into two tests because capfd interferes with the
    # output logged to file when using a subprocess.  We test the file
    # here, and echoing in test_log_subproc_and_echo_output_capfd below.
    with capfd.disabled():
        with tmpdir.as_cwd():
            with log_output('foo.txt') as logger:
                with logger.force_echo():
                    echo('echo')
                print('logged')

            with open('foo.txt') as f:
                assert f.read() == 'echo\nlogged\n'


@pytest.mark.skipif(not which('echo'), reason="needs echo command")
def test_log_subproc_and_echo_output_capfd(capfd, tmpdir):
    echo = which('echo')

    # This tests *only* what is echoed when using a subprocess, as capfd
    # interferes with the logged data. See
    # test_log_subproc_and_echo_output_no_capfd for tests on the logfile.
    with tmpdir.as_cwd():
        with log_output('foo.txt') as logger:
            with logger.force_echo():
                echo('echo')
            print('logged')

        assert capfd.readouterr()[0] == "echo\n"


#
# Tests below use a pseudoterminal to test llnl.util.tty.log
#
def simple_logger(**kwargs):
    """Mock logger (minion) process for testing log.keyboard_input."""
    def handler(signum, frame):
        running[0] = False
    signal.signal(signal.SIGUSR1, handler)

    log_path = kwargs["log_path"]
    running = [True]
    with log_output(log_path):
        while running[0]:
            print("line")
            time.sleep(1e-3)


def mock_shell_fg(proc, ctl, **kwargs):
    """PseudoShell controller function for test_foreground_background."""
    ctl.fg()
    ctl.status()
    ctl.wait_enabled()

    os.kill(proc.pid, signal.SIGUSR1)


def mock_shell_fg_no_termios(proc, ctl, **kwargs):
    """PseudoShell controller function for test_foreground_background."""
    ctl.fg()
    ctl.status()
    ctl.wait_disabled_fg()

    os.kill(proc.pid, signal.SIGUSR1)


def mock_shell_bg(proc, ctl, **kwargs):
    """PseudoShell controller function for test_foreground_background."""
    ctl.bg()
    ctl.status()
    ctl.wait_disabled()

    os.kill(proc.pid, signal.SIGUSR1)


def mock_shell_tstp_cont(proc, ctl, **kwargs):
    """PseudoShell controller function for test_foreground_background."""
    ctl.tstp()
    ctl.wait_stopped()

    ctl.cont()
    ctl.wait_running()

    os.kill(proc.pid, signal.SIGUSR1)


def mock_shell_tstp_tstp_cont(proc, ctl, **kwargs):
    """PseudoShell controller function for test_foreground_background."""
    ctl.tstp()
    ctl.wait_stopped()

    ctl.tstp()
    ctl.wait_stopped()

    ctl.cont()
    ctl.wait_running()

    os.kill(proc.pid, signal.SIGUSR1)


def mock_shell_tstp_tstp_cont_cont(proc, ctl, **kwargs):
    """PseudoShell controller function for test_foreground_background."""
    ctl.tstp()
    ctl.wait_stopped()

    ctl.tstp()
    ctl.wait_stopped()

    ctl.cont()
    ctl.wait_running()

    ctl.cont()
    ctl.wait_running()

    os.kill(proc.pid, signal.SIGUSR1)


def mock_shell_bg_fg(proc, ctl, **kwargs):
    """PseudoShell controller function for test_foreground_background."""
    ctl.bg()
    ctl.status()
    ctl.wait_disabled()

    ctl.fg()
    ctl.status()
    ctl.wait_enabled()

    os.kill(proc.pid, signal.SIGUSR1)


def mock_shell_bg_fg_no_termios(proc, ctl, **kwargs):
    """PseudoShell controller function for test_foreground_background."""
    ctl.bg()
    ctl.status()
    ctl.wait_disabled()

    ctl.fg()
    ctl.status()
    ctl.wait_disabled_fg()

    os.kill(proc.pid, signal.SIGUSR1)


def mock_shell_fg_bg(proc, ctl, **kwargs):
    """PseudoShell controller function for test_foreground_background."""
    ctl.fg()
    ctl.status()
    ctl.wait_enabled()

    ctl.bg()
    ctl.status()
    ctl.wait_disabled()

    os.kill(proc.pid, signal.SIGUSR1)


def mock_shell_fg_bg_no_termios(proc, ctl, **kwargs):
    """PseudoShell controller function for test_foreground_background."""
    ctl.fg()
    ctl.status()
    ctl.wait_disabled_fg()

    ctl.bg()
    ctl.status()
    ctl.wait_disabled()

    os.kill(proc.pid, signal.SIGUSR1)


@contextlib.contextmanager
def no_termios():
    saved = llnl.util.tty.log.termios
    llnl.util.tty.log.termios = None
    try:
        yield
    finally:
        llnl.util.tty.log.termios = saved


@pytest.mark.skipif(not which("ps"), reason="requires ps utility")
@pytest.mark.skipif(not termios, reason="requires termios support")
@pytest.mark.parametrize('test_fn,termios_on_or_off', [
    # tests with termios
    (mock_shell_fg, nullcontext),
    (mock_shell_bg, nullcontext),
    (mock_shell_bg_fg, nullcontext),
    (mock_shell_fg_bg, nullcontext),
    (mock_shell_tstp_cont, nullcontext),
    (mock_shell_tstp_tstp_cont, nullcontext),
    (mock_shell_tstp_tstp_cont_cont, nullcontext),
    # tests without termios
    (mock_shell_fg_no_termios, no_termios),
    (mock_shell_bg, no_termios),
    (mock_shell_bg_fg_no_termios, no_termios),
    (mock_shell_fg_bg_no_termios, no_termios),
    (mock_shell_tstp_cont, no_termios),
    (mock_shell_tstp_tstp_cont, no_termios),
    (mock_shell_tstp_tstp_cont_cont, no_termios),
])
def test_foreground_background(test_fn, termios_on_or_off, tmpdir):
    """Functional tests for foregrounding and backgrounding a logged process.

    This ensures that things like SIGTTOU are not raised and that
    terminal settings are corrected on foreground/background and on
    process stop and start.

    """
    shell = PseudoShell(test_fn, simple_logger)
    log_path = str(tmpdir.join("log.txt"))

    # run the shell test
    with termios_on_or_off():
        shell.start(log_path=log_path, debug=True)
    exitcode = shell.join()

    # processes completed successfully
    assert exitcode == 0

    # assert log was created
    assert os.path.exists(log_path)


def synchronized_logger(**kwargs):
    """Mock logger (minion) process for testing log.keyboard_input.

    This logger synchronizes with the parent process to test that 'v' can
    toggle output.  It is used in ``test_foreground_background_output`` below.

    """
    def handler(signum, frame):
        running[0] = False
    signal.signal(signal.SIGUSR1, handler)

    log_path = kwargs["log_path"]
    write_lock = kwargs["write_lock"]
    v_lock = kwargs["v_lock"]

    running = [True]
    sys.stderr.write(os.getcwd() + "\n")
    with log_output(log_path) as logger:
        with logger.force_echo():
            print("forced output")

        while running[0]:
            with write_lock:
                if v_lock.acquire(False):  # non-blocking acquire
                    print("off")
                    v_lock.release()
                else:
                    print("on")       # lock held; v is toggled on
            time.sleep(1e-2)


def mock_shell_v_v(proc, ctl, **kwargs):
    """Controller function for test_foreground_background_output."""
    write_lock = kwargs["write_lock"]
    v_lock = kwargs["v_lock"]

    ctl.fg()
    ctl.wait_enabled()
    time.sleep(.1)

    write_lock.acquire()  # suspend writing
    v_lock.acquire()      # enable v lock
    ctl.write(b'v')       # toggle v on stdin
    time.sleep(.1)
    write_lock.release()  # resume writing

    time.sleep(.1)

    write_lock.acquire()  # suspend writing
    ctl.write(b'v')       # toggle v on stdin
    time.sleep(.1)
    v_lock.release()      # disable v lock
    write_lock.release()  # resume writing
    time.sleep(.1)

    os.kill(proc.pid, signal.SIGUSR1)


def mock_shell_v_v_no_termios(proc, ctl, **kwargs):
    """Controller function for test_foreground_background_output."""
    write_lock = kwargs["write_lock"]
    v_lock = kwargs["v_lock"]

    ctl.fg()
    ctl.wait_disabled_fg()
    time.sleep(.1)

    write_lock.acquire()  # suspend writing
    v_lock.acquire()      # enable v lock
    ctl.write(b'v\n')     # toggle v on stdin
    time.sleep(.1)
    write_lock.release()  # resume writing

    time.sleep(.1)

    write_lock.acquire()  # suspend writing
    ctl.write(b'v\n')     # toggle v on stdin
    time.sleep(.1)
    v_lock.release()      # disable v lock
    write_lock.release()  # resume writing
    time.sleep(.1)

    os.kill(proc.pid, signal.SIGUSR1)


@pytest.mark.skipif(not which("ps"), reason="requires ps utility")
@pytest.mark.skipif(not termios, reason="requires termios support")
@pytest.mark.parametrize('test_fn,termios_on_or_off', [
    (mock_shell_v_v, nullcontext),
    (mock_shell_v_v_no_termios, no_termios),
])
@pytest.mark.skipif(
    sys.version_info < (2, 7),
    reason="Python 2.6 tests are run in a container, where this fails often"
)
def test_foreground_background_output(
        test_fn, capfd, termios_on_or_off, tmpdir):
    """Tests hitting 'v' toggles output, and that force_echo works."""
    if (sys.version_info >= (3, 8) and sys.platform == 'darwin'
        and termios_on_or_off == no_termios):

        return

    shell = PseudoShell(test_fn, synchronized_logger)
    log_path = str(tmpdir.join("log.txt"))

    # Locks for synchronizing with minion
    write_lock = multiprocessing.Lock()  # must be held by minion to write
    v_lock = multiprocessing.Lock()  # held while controller is in v mode

    with termios_on_or_off():
        shell.start(
            write_lock=write_lock,
            v_lock=v_lock,
            debug=True,
            log_path=log_path
        )

    exitcode = shell.join()
    out, err = capfd.readouterr()
    print(err)  # will be shown if something goes wrong
    print(out)

    # processes completed successfully
    assert exitcode == 0

    # split output into lines
    output = out.strip().split("\n")

    # also get lines of log file
    assert os.path.exists(log_path)
    with open(log_path) as log:
        log = log.read().strip().split("\n")

    # Controller and minion process coordinate with locks such that the
    # minion writes "off" when echo is off, and "on" when echo is on. The
    # output should contain mostly "on" lines, but may contain "off"
    # lines if the controller is slow. The important thing to observe
    # here is that we started seeing 'on' in the end.
    assert (
        ['forced output', 'on'] == uniq(output) or
        ['forced output', 'off', 'on'] == uniq(output)
    )

    # log should be off for a while, then on, then off
    assert (
        ['forced output', 'off', 'on', 'off'] == uniq(log) and
        log.count("off") > 2  # ensure some "off" lines were omitted
    )
