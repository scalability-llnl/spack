# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import re

import llnl.util.tty as tty
import spack.compiler
import spack.util.executable
from spack.package import *


class Fj(Package):
    """The Fujitsu compiler system is a high performance, production quality
    code generation tool designed for high performance parallel
    computing workloads.
    """

    homepage = "https://www.fujitsu.com/us/"

    maintainers = ['t-karatsu']

    def install(self, spec, prefix):
        raise InstallError(
            'Fujitsu compilers are not installable yet, but can be '
            'detected on a system where they are supplied by vendor'
        )

    executables = ['^fcc', '^FCC', '^frt']

    @classmethod
    def determine_version(cls, exe):
        version_regex = re.compile(r'\((?:FCC|FRT)\) ([a-z\d.]+)')
        try:
            output = spack.compiler.get_compiler_version_output(
                exe, '--version'
            )
            match = version_regex.search(output)
            if match:
                return match.group(1)
        except spack.util.executable.ProcessError:
            pass
        except Exception as e:
            tty.debug(e)

    @classmethod
    def determine_variants(cls, exes, version_str):
        compilers = {}
        for exe in exes:
            if 'fcc' in exe:
                compilers['c'] = exe
            if 'FCC' in exe:
                compilers['cxx'] = exe
            if 'frt' in exe:
                compilers['fortran'] = exe
        return '', {'compilers': compilers}
