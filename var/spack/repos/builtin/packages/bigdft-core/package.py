# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class BigdftCore(AutotoolsPackage, CudaPackage):
    """BigDFT: electronic structure calculation based on Daubechies wavelets."""

    homepage = "https://bigdft.org/"
    url      = "https://gitlab.com/l_sim/bigdft-suite/-/archive/1.9.1/bigdft-suite-1.9.1.tar.gz"
    git      = "https://gitlab.com/l_sim/bigdft-suite.git"

    version('1.9.1',   sha256='3c334da26d2a201b572579fc1a7f8caad1cbf971e848a3e10d83bc4dc8c82e41')
    version('1.9.0',   sha256='4500e505f5a29d213f678a91d00a10fef9dc00860ea4b3edf9280f33ed0d1ac8')
    version('1.8.3',   sha256='f112bb08833da4d11dd0f14f7ab10d740b62bc924806d77c985eb04ae0629909')
    version('1.8.2',   sha256='042e5a3b478b1a4c050c450a9b1be7bcf8e13eacbce4759b7f2d79268b298d61')
    version('1.8.1',   sha256='e09ff0ba381f6ffbe6a3c0cb71db5b73117874beb41f22a982a7e5ba32d018b3')

    variant('mpi',       default=True,  description='Enable MPI support')
    variant('openmp',    default=True,  description='Enable OpenMP support')
    variant('scalapack', default=True,  description='Enable SCALAPACK support')
    variant('openbabel', default=False, description='Enable detection of openbabel compilation')

    depends_on('python@:2.8', type='build', when="@:1.9.0")
    depends_on('python@3.0:', type='build', when="@1.9.1:")

    depends_on('blas')
    depends_on('lapack')
    depends_on('py-pyyaml')
    depends_on('libgain')
    depends_on('mpi',                      when='+mpi')
    depends_on('bigdft-futile@develop',    when='@develop')
    depends_on('bigdft-futile@1.9.1',      when='@1.9.1')
    depends_on('bigdft-futile@1.9.0',      when='@1.9.0')
    depends_on('bigdft-futile@1.8.3',      when='@1.8.3')
    depends_on('bigdft-futile@1.8.2',      when='@1.8.2')
    depends_on('bigdft-futile@1.8.1',      when='@1.8.1')
    depends_on('bigdft-chess@develop',     when='@develop')
    depends_on('bigdft-chess@1.9.1',       when='@1.9.1')
    depends_on('bigdft-chess@1.9.0',       when='@1.9.0')
    depends_on('bigdft-chess@1.8.3',       when='@1.8.3')
    depends_on('bigdft-chess@1.8.2',       when='@1.8.2')
    depends_on('bigdft-chess@1.8.1',       when='@1.8.1')
    depends_on('bigdft-psolver@develop',   when='@develop')
    depends_on('bigdft-psolver@1.9.1',     when='@1.9.1')
    depends_on('bigdft-psolver@1.9.0',     when='@1.9.0')
    depends_on('bigdft-psolver@1.8.3',     when='@1.8.3')
    depends_on('bigdft-psolver@1.8.2',     when='@1.8.2')
    depends_on('bigdft-psolver@1.8.1',     when='@1.8.1')
    depends_on('bigdft-libabinit@develop', when='@develop')
    depends_on('bigdft-libabinit@1.9.1',   when='@1.9.1')
    depends_on('bigdft-libabinit@1.9.0',   when='@1.9.0')
    depends_on('bigdft-libabinit@1.8.3',   when='@1.8.3')
    depends_on('bigdft-libabinit@1.8.2',   when='@1.8.2')
    depends_on('bigdft-libabinit@1.8.1',   when='@1.8.1')
    depends_on('libxc@:2.2.2',             when='@:1.9.1')
    depends_on('libxc@:4.3.4',             when='@develop')
    depends_on('scalapack',                when='+scalapack')
    depends_on('openbabel',                when='+openbabel')

    phases = ['autoreconf', 'configure', 'build', 'install']

    def autoreconf(self, spec, prefix):
        autoreconf = which('autoreconf')

        with working_dir('bigdft'):
            autoreconf('-fi')

    def configure(self, spec, prefix):
        linalg = []
        fcflags = []
        cflags = []

        python_version = spec['python'].version.up_to(2)
        pyyaml = join_path(spec['py-pyyaml'].prefix.lib,
                           'python{0}'.format(python_version))

        if '+openmp' in spec:
            fcflags.append(self.compiler.openmp_flag)

        if '+scalapack' in spec:
            linalg.append(spec['scalapack'].libs.ld_flags)
        linalg = [spec['blas'].libs.ld_flags, spec['lapack'].libs.ld_flags]

        args = [
            "FCFLAGS=%s" % " ".join(fcflags),
            "CFLAGS=%s" % " ".join(cflags),
            "--with-ext-linalg=%s" % " ".join(linalg),
            "--with-pyyaml-path=%s" % pyyaml,
            "--with-futile-libs=%s" % spec['bigdft-futile'].prefix.lib,
            "--with-futile-incs=%s" % spec['bigdft-futile'].headers.include_flags,
            "--with-chess-libs=%s" % spec['bigdft-chess'].prefix.lib,
            "--with-chess-incs=%s" % spec['bigdft-chess'].headers.include_flags,
            "--with-psolver-libs=%s" % spec['bigdft-psolver'].prefix.lib,
            "--with-psolver-incs=%s" % spec['bigdft-psolver'].headers.include_flags,
            "--with-libABINIT-libs=%s" % spec['bigdft-libabinit'].prefix.lib,
            "--with-libABINIT-incs=%s" % spec['bigdft-libabinit'].headers.include_flags,
            "--with-libgain-libs=%s" % spec['libgain'].libs.ld_flags,
            "--with-libgain-incs=%s" % spec['libgain'].headers.include_flags,
            "--with-libxc-libs=%s %s" % (spec['libxc'].libs.ld_flags,
                                         spec['libxc'].libs.ld_flags + "f90"),
            "--with-libxc-incs=%s" % spec['libxc'].headers.include_flags,
            "--without-etsf-io",
            "--with-moduledir=%s" % prefix.include,
            "--prefix=%s" % prefix,
        ]

        if '+mpi' in spec:
            args.append("CC=%s" % spec['mpi'].mpicc)
            args.append("CXX=%s" % spec['mpi'].mpicxx)
            args.append("FC=%s" % spec['mpi'].mpifc)
            args.append("F90=%s" % spec['mpi'].mpifc)
            args.append("F77=%s" % spec['mpi'].mpif77)
        else:
            args.append("--disable-mpi")

        if '+openmp' in spec:
            args.append("--with-openmp")
        else:
            args.append("--without-openmp")

        if '+cuda' in spec:
            args.append("--enable-opencl")
            args.append("--with-ocl-path=%s" % spec['cuda'].prefix)
            args.append("--enable-cuda-gpu")
            args.append("--with-cuda-path=%s" % spec['cuda'].prefix)
            args.append("--with-cuda-libs=%s" % spec['cuda'].libs.link_flags)

        if '+openbabel' in spec:
            args.append("--enable-openbabel")
            args.append("--with-openbabel-libs=%s" % spec['openbabel'].prefix.lib)
            args.append("--with-openbabel-incs=%s" % spec['openbabel'].prefix.include)

        with working_dir('bigdft'):
            configure(*args)

    def build(self, spec, prefix):
        with working_dir('bigdft'):
            make()

    def install(self, spec, prefix):
        with working_dir('bigdft'):
            make('install')

    @property
    def libs(self):
        shared = "+shared" in self.spec
        return find_libraries(
            'libbigdft-*', root=self.prefix, shared=shared, recursive=True
        )
