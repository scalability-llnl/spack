# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections
import re

import llnl.util.tty as tty
import spack.compiler
from spack.package import *


class Xlc(Package):
    """IBM XL C/C++ is an advanced, high-performance compiler that can be
    used for developing complex, computationally intensive programs, including
    interlanguage calls with C and Fortran programs.
    """

    homepage = "https://www.ibm.com/support/knowledgecenter/SSXVZZ_16.1.1/com.ibm.compilers.linux.doc/welcome.html"

    variant('r', default=True, description='The _r version of compilers')

    def install(self, spec, prefix):
        raise InstallError(
            'XL compilers are not installable yet, but can be '
            'detected on a system where they are supplied by vendor'
        )

    executables = [r'xlc', r'xlC', r'xlc\+\+']

    @classmethod
    def determine_version(cls, exe):
        version_regex = re.compile(r'([0-9]?[0-9]\.[0-9])')
        try:
            output = spack.compiler.get_compiler_version_output(
                exe, '-qversion'
            )
            # Exclude spurious Fortran compilers
            if 'Fortran' in output:
                return None

            match = version_regex.search(output)
            if match:
                return match.group(1)
        except spack.util.executable.ProcessError:
            pass
        except Exception as e:
            tty.debug(str(e))

    @classmethod
    def determine_variants(cls, exes, version_str):
        variants = collections.defaultdict(dict)
        for exe in exes:
            # Determine the variant of the spec
            variant_str = '+r' if '_r' in exe else '~r'
            if 'xlc++' in exe:
                variants[variant_str]['cxx'] = exe
                continue

            if 'xlc' in exe:
                variants[variant_str]['c'] = exe
                continue

        results = []
        for variant_str, compilers in variants.items():
            results.append((variant_str, {'compilers': compilers}))

        return results

    @property
    def cc(self):
        if self.spec.external:
            return self.spec.extra_attributes['compilers']['c']
        msg = "cannot retrieve C compiler [spec is not concrete]"
        assert self.spec.concrete, msg

    @property
    def cxx(self):
        if self.spec.external:
            return self.spec.extra_attributes['compilers']['cxx']
        msg = "cannot retrieve C compiler [spec is not concrete]"
        assert self.spec.concrete, msg
