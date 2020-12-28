# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRhtslib(RPackage):
    """HTSlib high-throughput sequencing library as an R package.

       This package provides version 1.7 of the 'HTSlib' C library for high-
       throughput sequence analysis. The package is primarily useful to
       developers of other R packages who wish to make use of HTSlib.
       Motivation and instructions for use of this package are in the vignette,
       vignette(package="Rhtslib", "Rhtslib")."""

    homepage = "https://bioconductor.org/packages/Rhtslib"
    git      = "https://git.bioconductor.org/packages/Rhtslib.git"

    version('1.18.1', commit='751a2ebaed43b7991204b27bd6c7870645001d82')
    version('1.16.3', commit='3ed0b5db2ee3cf0df1c6096fde8855c8485eebd4')
    version('1.14.1', commit='4be260720f845a34d0ac838278fce1363f645230')
    version('1.12.1', commit='e3487b1355995d09b28fde5d0a7504a3e79a7203')
    version('1.10.0', commit='53dcf7dfe35d735283956c77c011a97ca3f4eb26')
    version('1.8.0', commit='3b5493473bed42958614091c58c739932ffcfa79')

    depends_on('r-zlibbioc', type=('build', 'run'))

    depends_on('bzip2', type=('build', 'link', 'run'))
    depends_on('xz', type=('build', 'link', 'run'))
    depends_on('curl', type=('build', 'link', 'run'))
    depends_on('gmake', type='build')

    # Some versions of this package will leave the temporary installation
    # directory in the htslib shared object. R will fix this if patchelf is
    # available
    depends_on('patchelf', when='@1.12:1.14', type='build')

    patch('use_spack_Makeconf.patch', when='@1.12:')
    patch('find_deps-1.12.patch', when='@1.12:1.14')
    patch('find_deps-1.16.patch', when='@1.16:')

    @when('@1.12:')
    def setup_build_environment(self, env):
        env.set('BZIP2_INCLUDE', self.spec['bzip2'].headers.include_flags)
        env.set('XZ_INCLUDE', self.spec['xz'].headers.include_flags)
        env.set('BZIP2_LIB', self.spec['bzip2'].libs.search_flags)
        env.set('XZ_LIB', self.spec['xz'].libs.search_flags)
