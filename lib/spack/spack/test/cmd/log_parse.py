# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.main

logparse = spack.main.SpackCommand('log-parse')


@pytest.fixture()
def log_prase_file(tmpdir):
    log_file = tmpdir.join('log.txt')

    with log_file.open('w') as f:
        f.write("""#!/bin/sh\n
checking build system type... x86_64-apple-darwin16.6.0
checking host system type... x86_64-apple-darwin16.6.0
error: weird_error.c:145: something weird happened                          E
checking for gcc... /Users/gamblin2/src/spack/lib/spack/env/clang/clang
checking whether the C compiler works... yes
/var/tmp/build/foo.py:60: warning: some weird warning                       W
checking for C compiler default output file name... a.out
ld: fatal: linker thing happened                                            E
checking for suffix of executables...
configure: error: in /path/to/some/file:                                    E
configure: error: cannot run C compiled programs.                           E
""")

    yield log_file


def test_log_parse_width(log_prase_file):

    output = logparse('-w', '16', '-c', '1', str(log_prase_file))
    lines = output.split('\n')

    assert 15 == len(lines[1])


def test_log_parse_show(log_prase_file):

    output = logparse('--show', 'warnings', '-c', '1', str(log_prase_file))
    lines = output.strip().split('\n')

    assert "1 warnings" == lines[0]
    assert len(lines) == 5
