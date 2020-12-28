# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlModuleBuildTiny(PerlPackage):
    """Module::Build::Tiny - A tiny replacement for Module::Build"""

    homepage = "https://metacpan.org/pod/Module::Build::Tiny"
    url      = "https://cpan.metacpan.org/authors/id/L/LE/LEONT/Module-Build-Tiny-0.039.tar.gz"

    version('0.039', sha256='7d580ff6ace0cbe555bf36b86dc8ea232581530cbeaaea09bccb57b55797f11c')

    depends_on('perl-module-build', type='build')
    depends_on('perl-extutils-config', type=('build', 'run'))
    depends_on('perl-extutils-helpers', type=('build', 'run'))
    depends_on('perl-extutils-installpaths', type=('build', 'run'))
