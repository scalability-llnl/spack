# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Scorep(AutotoolsPackage):
    """The Score-P measurement infrastructure is a highly scalable and
    easy-to-use tool suite for profiling, event tracing, and online analysis
    of HPC applications.
    """

    homepage = "http://www.vi-hps.org/projects/score-p"
    url      = "https://www.vi-hps.org/cms/upload/packages/scorep/scorep-4.1.tar.gz"

    version('6.0',   sha256='5dc1023eb766ba5407f0b5e0845ec786e0021f1da757da737db1fb71fc4236b8')
    version('5.0',   sha256='0651614eacfc92ffbe5264a3efebd0803527ae6e8b11f7df99a56a02c37633e1')
    version('4.1',   sha256='7bb6c1eecdd699b4a3207caf202866778ee01f15ff39a9ec198fcd872578fe63')
    version('4.0',   sha256='c050525606965950ad9b35c14077b88571bcf9bfca08599279a3d8d1bb00e655')
    version('3.1',   sha256='49efe8a4e02afca752452809e1b21cba42e8ccb0a0772f936d4459d94e198540')
    version('3.0',   sha256='c9e7fe0a8239b3bbbf7628eb15f7e90de9c36557818bf3d01aecce9fec2dc0be')
    version('2.0.2', sha256='d19498408781048f0e9039a1a245bce6b384f09fbe7d3643105b4e2981ecd610')
    version('1.4.2', sha256='d7f3fcca2efeb2f5d5b5f183b3b2c4775e66cbb3400ea2da841dd0428713ebac')
    version('1.3',   sha256='dcfd42bd05f387748eeefbdf421cb3cd98ed905e009303d70b5f75b217fd1254')

    patch('gcc7.patch', when='@1.4:3')
    patch('gcc10.patch', when='@3.1:')

    variant('mpi', default=True, description="Enable MPI support")
    variant('papi', default=True, description="Enable PAPI")
    variant('pdt', default=False, description="Enable PDT")
    variant('shmem', default=False, description='Enable shmem tracing')
    variant('unwind', default=False,
            description="Enable sampling via libunwind and lib wrapping")

    # Dependencies for SCORE-P are quite tight. See the homepage for more
    # information. Starting with scorep 4.0 / cube 4.4, Score-P only depends on
    # two components of cube -- cubew and cubelib.

    # SCOREP 6
    depends_on('otf2@2.2:', when='@6:')
    # SCOREP 4 and 5
    depends_on('otf2@2.1:', when='@4:')
    depends_on('opari2@2.0:', when='@4:')
    depends_on('cubew@4.4:', when='@4:')
    depends_on('cubelib@4.4:', when='@4:')
    # SCOREP 3
    depends_on('otf2@2:', when='@3:3.99')
    depends_on('opari2@2:', when='@3:3.99')
    depends_on('cube@4.3:', when='@3:3.99')
    # SCOREP 2.0.2
    depends_on('otf2@2.0', when='@2.0.2')
    depends_on('opari2@2.0', when='@2.0.2')
    depends_on('cube@4.3:4.4', when='@2.0.2')
    # SCOREP 1.4.2
    depends_on('otf2@1.5:1.6', when='@1.4.2')
    depends_on('opari2@1.1.4', when='@1.4.2')
    depends_on('cube@4.3:4.4', when='@1.4.2')
    # SCOREP 1.3
    depends_on("otf2@1.4", when='@1.3')
    depends_on("opari2@1.1.4", when='@1.3')
    depends_on("cube@4.2.3", when='@1.3')

    depends_on('mpi', when="+mpi")
    depends_on('papi', when="+papi")
    depends_on('pdt', when="+pdt")
    depends_on('llvm', when="+unwind")
    depends_on('libunwind', when="+unwind")

    # Score-P requires a case-sensitive file system, and therefore
    # does not work on macOS
    # https://github.com/spack/spack/issues/1609
    conflicts('platform=darwin')

    def configure_args(self):
        spec = self.spec

        config_args = [
            "--with-otf2=%s" % spec['otf2'].prefix.bin,
            "--with-opari2=%s" % spec['opari2'].prefix.bin,
            "--enable-shared"]

        cname = spec.compiler.name
        config_args.append('--with-nocross-compiler-suite={0}'.format(cname))

        if self.version >= Version('4.0'):
            config_args.append("--with-cubew=%s" % spec['cubew'].prefix.bin)
            config_args.append("--with-cubelib=%s" %
                               spec['cubelib'].prefix.bin)
        else:
            config_args.append("--with-cube=%s" % spec['cube'].prefix.bin)

        if "+papi" in spec:
            config_args.append("--with-papi-header=%s" %
                               spec['papi'].prefix.include)
            config_args.append("--with-papi-lib=%s" % spec['papi'].prefix.lib)

        if "+pdt" in spec:
            config_args.append("--with-pdt=%s" % spec['pdt'].prefix.bin)

        if "+unwind" in spec:
            config_args.append("--with-libunwind=%s" %
                               spec['libunwind'].prefix)

        config_args += self.with_or_without('shmem')
        config_args += self.with_or_without('mpi')

        if spec.satisfies('^intel-mpi'):
            config_args.append('--with-mpi=intel3')
        elif spec.satisfies('^mpich') or spec.satisfies('^mvapich2'):
            config_args.append('--with-mpi=mpich3')
        elif spec.satisfies('^openmpi'):
            config_args.append('--with-mpi=openmpi')

        config_args.extend([
            'CFLAGS={0}'.format(self.compiler.cc_pic_flag),
            'CXXFLAGS={0}'.format(self.compiler.cxx_pic_flag)
        ])

        if "+mpi" in spec:
            config_args.extend([
                'MPICC={0}'.format(spec['mpi'].mpicc),
                'MPICXX={0}'.format(spec['mpi'].mpicxx),
                'MPIF77={0}'.format(spec['mpi'].mpif77),
                'MPIFC={0}'.format(spec['mpi'].mpifc)
            ])

        return config_args
