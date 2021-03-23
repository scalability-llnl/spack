# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ipopt(AutotoolsPackage):
    """Ipopt (Interior Point OPTimizer, pronounced eye-pea-Opt) is a
       software package for large-scale nonlinear optimization."""
    homepage = "https://projects.coin-or.org/Ipopt"
    url      = "http://www.coin-or.org/download/source/Ipopt/Ipopt-3.12.4.tgz"

    version('3.12.10', sha256='e1a3ad09e41edbfe41948555ece0bdc78757a5ca764b6be5a9a127af2e202d2e')
    version('3.12.9', sha256='8ff3fe1a8560896fc5559839a87c2530cac4ed231b0806e487bfd3cf2d294ab8')
    version('3.12.8', sha256='62c6de314220851b8f4d6898b9ae8cf0a8f1e96b68429be1161f8550bb7ddb03')
    version('3.12.7', sha256='9c8b02149fa4f0cdf63e838ae68f86aa41a577d7f05932139eede9179f314861')
    version('3.12.6', sha256='6aaa6bd862d54eba6fb966950fa6928ca01d66cf4cb842b2f41a7ebfa61eee2b')
    version('3.12.5', sha256='53e7af6eefcb6de1f8e936c9c887c7bcb5a9fa4fcf7673a227f16de131147325')
    version('3.12.4', sha256='292afd952c25ec9fe6225041683dcbd3cb76e15a128764671927dbaf881c2e89')
    version('3.12.3', sha256='754fb9473bc683b59a53d2057ff852d0a8d56198bcdba2e2529ce299243fdaa5')
    version('3.12.2', sha256='3903657788bff7d7743f8bb25c34ccf91c445e72a4710cb821c024107bd1b474')
    version('3.12.1', sha256='d6c18f7c5bf486712b493167d27ec6e940ad376c5b903b97acc5a3ade1c0a3ef')
    version('3.12.0', sha256='ed19e5e7174355e93c93c798b5056036e2fd2ec78cf0f3954876483f74fe618b')

    variant('coinhsl', default=False,
            description="Build with Coin Harwell Subroutine Libraries")
    variant('metis', default=False,
            description="Build with METIS partitioning support")
    variant('debug', default=False,
            description="Build debug instead of optimized version")
    variant('mumps', default=True,
            description='Build with support for linear solver MUMPS')

    depends_on("blas")
    depends_on("lapack")
    depends_on("pkgconfig", type='build')
    depends_on("mumps+double~mpi", when='+mumps')
    depends_on('coinhsl', when='+coinhsl')
    depends_on('metis@4.0:', when='+metis')

    # Must have at least one linear solver available!
    conflicts('~mumps', when='~coinhsl')

    patch('ipopt_ppc_build.patch', when='arch=ppc64le')

    flag_handler = build_system_flags
    build_directory = 'spack-build'

    # IPOPT does not build correctly in parallel on OS X
    parallel = False

    def configure_args(self):
        spec = self.spec
        # Dependency directories
        blas_dir = spec['blas'].prefix
        lapack_dir = spec['lapack'].prefix

        blas_lib = spec['blas'].libs.ld_flags
        lapack_lib = spec['lapack'].libs.ld_flags

        args = [
            "--prefix=%s" % self.prefix,
            "--enable-shared",
            "coin_skip_warn_cxxflags=yes",
            "--with-blas-incdir=%s" % blas_dir.include,
            "--with-blas-lib=%s" % blas_lib,
            "--with-lapack-incdir=%s" % lapack_dir.include,
            "--with-lapack-lib=%s" % lapack_lib
        ]

        if '+mumps' in spec:
            # Add directory with fake MPI headers in sequential MUMPS
            # install to header search path
            mumps_dir = spec['mumps'].prefix
            mumps_flags = "-ldmumps -lmumps_common -lpord -lmpiseq"
            mumps_libcmd = "-L%s " % mumps_dir.lib + mumps_flags
            args.extend([
                "--with-mumps-incdir=%s" % mumps_dir.include,
                "--with-mumps-lib=%s" % mumps_libcmd])

        if 'coinhsl' in spec:
            args.extend([
                '--with-hsl-lib=%s' % spec['coinhsl'].libs.ld_flags,
                '--with-hsl-incdir=%s' % spec['coinhsl'].prefix.include])

        if 'metis' in spec:
            args.extend([
                '--with-metis-lib=%s' % spec['metis'].libs.ld_flags,
                '--with-metis-incdir=%s' % spec['metis'].prefix.include])

        # The IPOPT configure file states that '--enable-debug' implies
        # '--disable-shared', but adding '--enable-shared' overrides
        # '--disable-shared' and builds a shared library with debug symbols
        if '+debug' in spec:
            args.append('--enable-debug')
        else:
            args.append('--disable-debug')

        return args
