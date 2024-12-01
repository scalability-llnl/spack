# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class BuildWarnings(Package):
    """This package's install fails but only emits warnings."""

    homepage = "http://www.example.com/trivial_install"
    url = "http://www.unit-test-should-replace-this-url/trivial_install-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    def install(self, spec, prefix):
        if sys.platform == "win32":
            with open("configure.bat", "w") as f:
                f.write(
                    """
  @ECHO off
  ECHO 'checking for gcc... /Users/gamblin2/src/spack/lib/spack/env/clang/clang'
  ECHO 'checking whether the C compiler works... yes'
  ECHO 'checking for C compiler default output file name... a.out'
  ECHO 'WARNING: ALL CAPITAL WARNING!'
  ECHO 'checking for suffix of executables...'
  ECHO 'foo.c:89: warning: some weird warning!'
  EXIT /B 1
                  """
                )

            Executable("configure.bat")("--prefix=%s" % self.prefix)
        else:
            with open("configure", "w") as f:
                f.write(
                    """#!/bin/sh\n
  echo 'checking for gcc... /Users/gamblin2/src/spack/lib/spack/env/clang/clang'
  echo 'checking whether the C compiler works... yes'
  echo 'checking for C compiler default output file name... a.out'
  echo 'WARNING: ALL CAPITAL WARNING!'
  echo 'checking for suffix of executables...'
  echo 'foo.c:89: warning: some weird warning!'
  exit 1
  """
                )
            configure()
