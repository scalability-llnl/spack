# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PyLineProfiler(PythonPackage):
    """Line-by-line profiler."""

    homepage = "https://github.com/rkern/line_profiler"
    url      = "https://pypi.io/packages/source/l/line_profiler/line_profiler-2.0.tar.gz"

    version('2.1.2', sha256='efa66e9e3045aa7cb1dd4bf0106e07dec9f80bc781a993fbaf8162a36c20af5c')
    version('2.0', sha256='739f8ad0e4bcd0cb82e99afc09e00a0351234f6b3f0b1f7f0090a8a2fbbf8381')

    depends_on('python@2.5:', type=('build', 'run'))
    depends_on('py-setuptools',     type='build')
    depends_on('py-cython',         type='build')
    depends_on('py-ipython@0.13:',  type=('build', 'run'))

    # See https://github.com/rkern/line_profiler/issues/166
    @run_before('build')
    def fix_cython(self):
        # TODO: Replace the check with a `@when('^python@3.7:')` decorator once
        # https://github.com/spack/spack/issues/12736 is resolved
        if not self.spec.satisfies("^python@3.7:"):
            return
        cython = self.spec['py-cython'].command
        for root, _, files in os.walk('.'):
            for fn in files:
                if fn.endswith('.pyx'):
                    cython(os.path.join(root, fn))
