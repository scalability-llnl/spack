# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SstMacro(AutotoolsPackage):
    """The Structural Simulation Toolkit Macroscale Element Library simulates
    large-scale parallel computer architectures for the coarse-grained study
    of distributed-memory applications. The simulator is driven from either a
    trace file or skeleton application. SST/macro's modular architecture can
    be extended with additional network models, trace file formats, software
    services, and processor models.
    """

    homepage = "http://sst.sandia.gov/about_sstmacro.html"
    git = "https://github.com/sstsimulator/sst-macro.git"
    url = "https://github.com/sstsimulator/sst-macro/releases/download/v10.0.0_Final/sstmacro-10.0.0.tar.gz"

    maintainers = ['jjwilke']

    version('10.1.0', sha256='e15d99ce58d282fdff849af6de267746a4c89f3b8c5ab6c1e1e7b53a01127e73')
    version('10.0.0', sha256='064b732256f3bec9b553e00bcbc9a1d82172ec194f2b69c8797f585200b12566')
    version('master',  branch='master')
    version('develop', branch='devel')

    depends_on('autoconf@1.68:', type='build', when='@master:')
    depends_on('automake@1.11.1:', type='build', when='@master:')
    depends_on('libtool@1.2.4:', type='build', when='@master:')
    depends_on('m4', type='build', when='@master:')

    depends_on('binutils', type='build')
    depends_on('zlib', type=('build', 'link'))
    depends_on('otf2', when='+otf2')
    depends_on('llvm+clang@5:9', when='+skeletonizer')
    depends_on('mpi', when='+pdes_mpi')
    depends_on('sst-core@develop',   when='@develop+core')
    depends_on('sst-core@master',  when='@master+core')
    depends_on('sst-core@10.1.0', when='@10.1.0+core')
    depends_on('sst-core@10.0.0', when='@10.0.0+core')
    depends_on('gettext')

    variant('pdes_threads', default=True,
            description='Enable thread-parallel PDES simulation')
    variant('pdes_mpi', default=False,
            description='Enable distributed PDES simulation')
    variant('core',     default=False, description='Use SST Core for PDES')
    variant('otf2',     default=False,
            description='Enable OTF2 trace emission and replay support')
    variant('skeletonizer', default=False,
            description='Enable Clang source-to-source autoskeletonization')

    variant('static', default=True, description='Build static libraries')
    variant('shared', default=True, description='Build shared libraries')

    variant('werror', default=False,
            description='Build with all warnings as errors')
    variant('warnings', default=False,
            description='Build with all possible warnings')

    # force out-of-source builds
    build_directory = 'spack-build'

    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./bootstrap.sh')

    def configure_args(self):
        args = ['--disable-regex']

        spec = self.spec
        args.append(
            '--enable-static=%s' % ('yes' if '+static' in spec else 'no'))
        args.append(
            '--enable-shared=%s' % ('yes' if '+shared' in spec else 'no'))

        if spec.satisfies("@8.0.0:"):
            args.extend([
                '--%sable-otf2' %
                ('en' if '+otf2' in spec else 'dis'),
                '--%sable-multithread' %
                ('en' if '+pdes_threads' in spec else 'dis')
            ])

            if '+skeletonizer' in spec:
                args.append('--with-clang=' + spec['llvm'].prefix)

        if spec.satisfies("@10:"):
            if "+warnings" in spec:
                args.append("--with-warnings")
            if "+werror" in spec:
                args.append("--with-werror")

        if '+core' in spec:
            args.append('--with-sst-core=%s' % spec['sst-core'].prefix)

        # Optional MPI support
        need_core_mpi = False
        if "+core" in spec:
            if "+pdes_mpi" in spec["sst-core"]:
                need_core_mpi = True
        if '+pdes_mpi' in spec or need_core_mpi:
            env['CC'] = spec['mpi'].mpicc
            env['CXX'] = spec['mpi'].mpicxx
            env['F77'] = spec['mpi'].mpif77
            env['FC'] = spec['mpi'].mpifc

        return args
