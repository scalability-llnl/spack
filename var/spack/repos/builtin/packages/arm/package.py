# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path
import re

import llnl.util.tty as tty
import spack.compiler
import spack.util.executable
from spack.package import *


class Arm(Package):
    """Arm Compiler combines the optimized tools and libraries from Arm
    with a modern LLVM-based compiler framework.
    """

    homepage = "https://developer.arm.com/tools-and-software/server-and-hpc/arm-allinea-studio"
    url = "https://developer.arm.com/-/media/Files/downloads/hpc/arm-allinea-studio/20-2-1/Ubuntu16.04/arm-compiler-for-linux_20.2.1_Ubuntu-16.04_aarch64.tar"

    # FIXME: The version is checksummed for Ubuntu 16.04, but this is not
    # FIXME: important at the moment since the package is only meant to
    # FIXME: provide detection
    version('20.2.1', sha256='dc3f945b05b867809d9b507cb8ebba9cf72a6818d349207dbe1392c13dc0ad79')

    def install(self, spec, prefix):
        raise InstallError(
            'No install method available yet, only system detection.'
        )

    executables = [r'armclang', r'armclang\+\+', r'armflang']

    @classmethod
    def determine_version(cls, exe):
        regex_str = r'Arm C\/C\+\+\/Fortran Compiler version ([\d\.]+) '\
                    r'\(build number (\d+)\) '
        version_regex = re.compile(regex_str)
        try:
            output = spack.compiler.get_compiler_version_output(
                exe, '--version'
            )
            match = version_regex.search(output)
            if match:
                if match.group(1).count('.') == 1:
                    return match.group(1) + ".0." + match.group(2)
                return match.group(1) + "." + match.group(2)
        except spack.util.executable.ProcessError:
            pass
        except Exception as e:
            tty.debug(e)

    @classmethod
    def determine_variants(cls, exes, version_str):
        compilers = {}
        for exe in exes:
            if 'armclang' in exe:
                compilers['c'] = exe
            if 'armclang++' in exe:
                compilers['cxx'] = exe
            if 'armflang' in exe:
                compilers['fortran'] = exe
        return '', {'compilers': compilers}

    @property
    def cc(self):
        msg = "cannot retrieve C compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes['compilers'].get('c', None)
        return str(self.spec.prefix.bin.armclang)

    @property
    def cxx(self):
        msg = "cannot retrieve C++ compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes['compilers'].get('cxx', None)
        return os.path.join(self.spec.prefix.bin, 'armclang++')

    @property
    def fortran(self):
        msg = "cannot retrieve Fortran compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes['compilers'].get('fortran', None)
        return str(self.spec.prefix.bin.armflang)
