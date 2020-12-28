# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AdolC(AutotoolsPackage):
    """A package for the automatic differentiation of first and higher
    derivatives of vector functions in C and C++ programs by operator
    overloading."""

    homepage = "https://github.com/coin-or/ADOL-C"
    url      = "https://github.com/coin-or/ADOL-C/archive/releases/2.7.2.tar.gz"
    git      = "https://github.com/coin-or/ADOL-C.git"
    version('master',  branch='master')
    version('2.7.2', sha256='701e0856baae91b98397960d5e0a87a549988de9d4002d0e9a56fa08f5455f6e')
    version('2.7.1', sha256='a05422cc7faff5700e134e113822d1934fb540ad247e63778524d5d6d75bb0ef')
    version('2.7.0', sha256='a75cfa6240de8692b2a3e8e782319efefc316f1e595234fcee972ab0e7afa3cd')
    version('2.6.3', sha256='9750a0a06dcab9a0dba2010f07872ea9057ed29781e9e7d571691c27aa559b04')
    version('2.6.2', sha256='4ef6ff15b4691235c0ea6580917c7eb17d09ded485ac524a0a33ac7e99ab004b')
    version('2.6.1', sha256='48b41c40d1c8437fb98eeed4b24deaf3e59da804f34ac9c848da1b049b3b071a')
    version('2.6.0', sha256='26a1fcb8561f15781f645d245fc345c83497147ec7bb64d4bfc96e32c34c6c1c')
    version('2.5.2', sha256='390edb1513f749b2dbf6fb90db12ce786f6532af80e589f161ff43646b3a78a6')
    version('2.5.1', sha256='dedb93c3bb291366d799014b04b6d1ec63ca4e7216edf16167776c07961e3b4a')
    version('2.5.0', sha256='9d51c426d831884aac8f418be410c001eb62f3a11cb8f30c66af0b842edffb96')

    variant('advanced_branching', default=False,
            description='Enable advanced branching to reduce retaping')
    variant('atrig_erf', default=True,
            description='Enable arc-trig and error functions')
    variant('doc',      default=True,  description='Install documentation')
    variant('openmp',   default=False, description='Enable OpenMP support')
    variant('sparse',   default=False, description='Enable sparse drivers')
    variant('examples', default=True,  description='Install examples')
    variant('boost',    default=False, description='Enable boost')

    # Build dependencies
    depends_on('automake', type='build', when='@develop')
    depends_on('autoconf', type='build', when='@develop')
    depends_on('libtool',  type='build', when='@develop')
    depends_on('m4',       type='build', when='@develop')

    # Link dependencies
    depends_on('boost+system', when='+boost')

    # FIXME: add
    #  --with-colpack=DIR      path to the colpack library and headers
    #                       [default=system libraries]
    #  --with-mpi-root=MPIROOT absolute path to the MPI root directory
    #  --with-mpicc=MPICC      name of the MPI C++ compiler (default mpicc)
    #  --with-mpicxx=MPICXX    name of the MPI C++ compiler (default mpicxx)
    #  --with-ampi=AMPI_DIR    full path to the installation of adjoinable MPI
    #                           (AMPI)

    patch('openmp_exam_261.patch', when='@2.6.1')

    def configure_args(self):
        spec = self.spec

        configure_args = []

        if '+boost' in spec:
            configure_args.append(
                '--with-boost={0}'.format(spec['boost'].prefix)
            )
        else:
            configure_args.append(
                '--with-boost=no'
            )

        if '+advanced_branching' in spec:
            configure_args.append(
                '--enable-advanced-branching'
            )

        if '+atrig_erf' in spec:
            configure_args.append(
                '--enable-atrig-erf'
            )

        if '+openmp' in spec:
            configure_args.append(
                '--with-openmp-flag={0}'.format(self.compiler.openmp_flag)
            )

        if '+sparse' in spec:
            configure_args.append(
                '--enable-sparse'
            )

        # We can simply use the bundled examples to check
        # whether Adol-C works as expected
        if '+examples' in spec:
            configure_args.extend([
                '--enable-docexa',  # Documented examples
                '--enable-addexa'  # Additional examples
            ])
            if '+openmp' in spec:
                configure_args.append(
                    '--enable-parexa'  # Parallel examples
                )

        return configure_args

    @run_after('install')
    def install_additional_files(self):
        spec = self.spec
        prefix = self.prefix

        # Copy the config.h file, as some packages might require it
        source_directory = self.stage.source_path
        config_h = join_path(source_directory, 'ADOL-C', 'src', 'config.h')
        install(config_h, join_path(prefix.include, 'adolc'))

        # Install documentation to {prefix}/share
        if '+doc' in spec:
            install_tree(join_path('ADOL-C', 'doc'),
                         join_path(prefix.share, 'doc'))

        # Install examples to {prefix}/share
        if '+examples' in spec:
            install_tree(join_path('ADOL-C', 'examples'),
                         join_path(prefix.share, 'examples'))

            # Run some examples that don't require user input
            # TODO: Check that bundled examples produce the correct results
            with working_dir(join_path(
                    source_directory, 'ADOL-C', 'examples')):
                Executable('./tapeless_scalar')()
                Executable('./tapeless_vector')()

            with working_dir(join_path(
                    source_directory,
                    'ADOL-C', 'examples', 'additional_examples')):
                Executable('./checkpointing/checkpointing')()

            if '+openmp' in spec:
                with working_dir(join_path(
                        source_directory,
                        'ADOL-C', 'examples', 'additional_examples')):
                    Executable('./checkpointing/checkpointing')()
