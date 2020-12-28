# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Gsl(AutotoolsPackage, GNUMirrorPackage):
    """The GNU Scientific Library (GSL) is a numerical library for C and C++
    programmers. It is free software under the GNU General Public License. The
    library provides a wide range of mathematical routines such as random
    number generators, special functions and least-squares fitting. There are
    over 1000 functions in total with an extensive test suite."""

    homepage = "http://www.gnu.org/software/gsl"
    gnu_mirror_path = "gsl/gsl-2.3.tar.gz"

    version('2.5', sha256='0460ad7c2542caaddc6729762952d345374784100223995eb14d614861f2258d')
    version('2.4',   sha256='4d46d07b946e7b31c19bbf33dda6204d7bedc2f5462a1bae1d4013426cd1ce9b')
    version('2.3',   sha256='562500b789cd599b3a4f88547a7a3280538ab2ff4939504c8b4ac4ca25feadfb')
    version('2.2.1', sha256='13d23dc7b0824e1405f3f7e7d0776deee9b8f62c62860bf66e7852d402b8b024')
    version('2.1',   sha256='59ad06837397617f698975c494fe7b2b698739a59e2fcf830b776428938a0c66')
    version('2.0',   sha256='e361f0b19199b5e6c21922e9f16adf7eca8dd860842802424906d0f83485ca2d')
    version('1.16',  sha256='73bc2f51b90d2a780e6d266d43e487b3dbd78945dd0b04b14ca5980fe28d2f53')

    variant('external-cblas', default=False, description='Build against external blas')

    # from https://dev.gentoo.org/~mgorny/dist/gsl-2.3-cblas.patch.bz2
    patch('gsl-2.3-cblas.patch', when="+external-cblas")

    conflicts('+external-cblas', when="@:2.2.9999")
    depends_on('m4',       type='build', when='+external-cblas')
    depends_on('autoconf', type='build', when='+external-cblas')
    depends_on('automake', type='build', when='+external-cblas')
    depends_on('libtool',  type='build', when='+external-cblas')
    depends_on('blas', when='+external-cblas')

    @property
    def force_autoreconf(self):
        # The external cblas patch touches configure
        return self.spec.satisfies('+external-cblas')

    def configure_args(self):
        configure_args = []
        if self.spec.satisfies('+external-cblas'):
            configure_args.append('--with-external-cblas')
            configure_args.append('CBLAS_CFLAGS=%s'
                                  % self.spec['blas'].headers.include_flags)
            configure_args.append('CBLAS_LIBS=%s'
                                  % self.spec['blas'].libs.ld_flags)

        return configure_args
