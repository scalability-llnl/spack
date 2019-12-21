# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function
import pytest

from llnl.util.tty.log import log_output
from spack.util.executable import which


def test_log_python_output_with_python_stream(capsys, tmpdir):
    # pytest's DontReadFromInput object does not like what we do here, so
    # disable capsys or things hang.
    with tmpdir.as_cwd():
        with capsys.disabled():
            with log_output('foo.txt'):
                print('logged')

        with open('foo.txt') as f:
            assert f.read() == 'logged\n'

        assert capsys.readouterr() == ('', '')


def test_log_python_output_with_fd_stream(capfd, tmpdir):
    with tmpdir.as_cwd():
        with log_output('foo.txt'):
            print('logged')

        with open('foo.txt') as f:
            assert f.read() == 'logged\n'

        assert capfd.readouterr() == ('', '')


def test_pass_input(capfd, tmpdir):
    import sys
    import os
    import multiprocessing
    import time

    def child_write(write_fd):
        sending_end = os.fdopen(write_fd, 'w')
        sending_end.write('example input\n')

    save_stdin = sys.stdin
    try:
        sub_stdin_fd, write_fd = os.pipe()
        sys.stdin = os.fdopen(sub_stdin_fd, 'r')
        with tmpdir.as_cwd():
            with log_output('foo.txt') as logger:
                writing_proc = multiprocessing.Process(
                    target=child_write, args=(write_fd,))

                with logger._pass_input():
                    writing_proc.start()
                    time.sleep(1)
                    if sys.version_info < (3,):
                        x = raw_input()
                    else:
                        x = input()

                writing_proc.join()
                assert x == 'example input'
                print('logged')

            with open('foo.txt') as f:
                assert f.read() == 'logged\n'
    finally:
        sys.stdin = save_stdin


def test_log_python_output_and_echo_output(capfd, tmpdir):
    with tmpdir.as_cwd():
        with log_output('foo.txt') as logger:
            with logger.force_echo():
                print('echo')
            print('logged')

        assert capfd.readouterr() == ('echo\n', '')

        with open('foo.txt') as f:
            assert f.read() == 'echo\nlogged\n'


@pytest.mark.skipif(not which('echo'), reason="needs echo command")
def test_log_subproc_output(capsys, tmpdir):
    echo = which('echo')

    # pytest seems to interfere here, so we need to use capsys.disabled()
    # TODO: figure out why this is and whether it means we're doing
    # sometihng wrong with OUR redirects.  Seems like it should work even
    # with capsys enabled.
    with tmpdir.as_cwd():
        with capsys.disabled():
            with log_output('foo.txt'):
                echo('logged')

        with open('foo.txt') as f:
            assert f.read() == 'logged\n'


@pytest.mark.skipif(not which('echo'), reason="needs echo command")
def test_log_subproc_and_echo_output(capfd, tmpdir):
    echo = which('echo')

    with tmpdir.as_cwd():
        with log_output('foo.txt') as logger:
            with logger.force_echo():
                echo('echo')
            print('logged')

        assert capfd.readouterr() == ('echo\n', '')

        with open('foo.txt') as f:
            assert f.read() == 'logged\n'
