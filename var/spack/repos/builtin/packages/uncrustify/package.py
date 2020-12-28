# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Uncrustify(Package):
    """Source Code Beautifier for C, C++, C#, ObjectiveC, Java, and others."""

    homepage = "http://uncrustify.sourceforge.net/"
    url      = "http://downloads.sourceforge.net/project/uncrustify/uncrustify/uncrustify-0.61/uncrustify-0.61.tar.gz"

    version('0.67', sha256='54f15c8ebddef120522db21f38fac1dd3b0a285fbf60a8b71f9e333e96cf6ddc')
    version('0.61', sha256='1df0e5a2716e256f0a4993db12f23d10195b3030326fdf2e07f8e6421e172df9')

    depends_on('cmake', type='build', when='@0.64:')

    @when('@0.64:')
    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake('..', *std_cmake_args)
            make()
            make('install')

    @when('@:0.62')
    def install(self, spec, prefix):
        configure('--prefix={0}'.format(self.prefix))
        make()
        make('install')
