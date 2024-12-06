# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from ctest_log_parser import CTestLogParser


def test_log_parser(tmpdir):
    log_file = tmpdir.join("log.txt")

    with log_file.open("w") as f:
        f.write(
            """#!/bin/sh\n
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
"""
        )

    parser = CTestLogParser()
    errors, warnings = parser.parse(str(log_file))

    assert len(errors) == 4
    assert all(e.text.endswith("E") for e in errors)

    assert len(warnings) == 1
    assert all(w.text.endswith("W") for w in warnings)
