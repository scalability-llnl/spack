# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost


class Gunrock(CMakePackage, CudaPackage):
    """High-Performance Graph Primitives on GPUs"""

    homepage = "https://gunrock.github.io/docs/"
    git      = "https://github.com/gunrock/gunrock.git"

    version('master',   submodules=True)
    version('1.2',      submodules=True, tag='v1.2')
    # v1.1 build is broken. See:
    # https://github.com/gunrock/gunrock/issues/777
    version('1.1',      submodules=True, tag='v1.1')
    version('1.0',      submodules=True, tag='v1.0')
    version('0.5.1',    submodules=True, tag='v0.5.1')
    version('0.5',      submodules=True, tag='v0.5')
    version('0.4',      submodules=True, tag='v0.4')
    version('0.3.1',    submodules=True, tag='v0.3.1')
    version('0.3',      submodules=True, tag='v0.3')
    version('0.2',      submodules=True, tag='v0.2')
    version('0.1',      submodules=True, tag='v0.1')

    variant('cuda', default=True, description="Build with Cuda support")

    variant('lib',                  default=True,  description='Build main gunrock library')
    variant('shared_libs',          default=True,  description='Turn off to build for static libraries')
    variant('tests',                default=True,  description='Build functional tests / examples')
    variant('mgpu_tests',           default=False, description='Builds Gunrock applications and enables the ctest framework for single GPU implementations')
    variant('cuda_verbose_ptxas',   default=False, description='Enable verbose output from the PTXAS assembler')
    variant('google_tests',         default=False, description='Build unit tests using googletest')
    variant('code_coverage',        default=False, description="run code coverage on Gunrock's source code")
    # apps
    msg = 'select either all or individual applications'
    variant(
        "applications",
        values=disjoint_sets(
            ('all',), ('bc', 'bfs', 'cc', 'pr', 'sssp', 'dobfs', 'hits',
                       'salsa', 'mst', 'wtf', 'topk')
        ).allow_empty_set().with_default('all').with_error(msg),
        description="Application to be built"
    )

    variant('boost', default=True, description='Build with Boost')
    variant('metis', default=False, description='Build with Metis support')

    depends_on('googletest', when='+google_tests')
    depends_on('lcov', when='+code_coverage')
    depends_on('boost@1.58.0:', when='+boost')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, when='+boost')
    depends_on('metis', when='+metis')

    conflicts('cuda_arch=none', when='+cuda',
              msg='Must specify CUDA compute capabilities of your GPU. \
See "spack info gunrock"')

    def cmake_args(self):
        spec = self.spec
        args = []
        args.extend([
                    '-DGUNROCK_BUILD_LIB={0}'.format(
                        'ON' if '+lib' in spec else 'OFF'),
                    '-DGUNROCK_BUILD_SHARED_LIBS={0}'.format(
                        'ON' if '+shared_libs' in spec else 'OFF'),
                    '-DGUNROCK_BUILD_TESTS={0}'.format(
                        'ON' if '+tests' in spec else 'OFF'),
                    '-DGUNROCK_MGPU_TESTS={0}'.format(
                        'ON' if '+mgpu_tests' in spec else 'OFF'),
                    '-DCUDA_VERBOSE_PTXAS={0}'.format(
                        'ON' if '+cuda_verbose_ptxas' in spec else 'OFF'),
                    '-DGUNROCK_GOOGLE_TESTS={0}'.format(
                        'ON' if '+google_tests' in spec else 'OFF'),
                    '-DGUNROCK_CODE_COVERAGE={0}'.format(
                        'ON' if '+code_coverage' in spec else 'OFF'),
                    ])

        # turn off auto detect, which undoes custom cuda arch options
        args.append('-DCUDA_AUTODETECT_GENCODE=OFF')

        cuda_arch_list = self.spec.variants['cuda_arch'].value
        if cuda_arch_list[0] != 'none':
            for carch in cuda_arch_list:
                args.append('-DGUNROCK_GENCODE_SM' + carch + '=ON')

        app_list = self.spec.variants['applications'].value
        if app_list[0] != 'none':
            args.extend([
                '-DGUNROCK_BUILD_APPLICATIONS={0}'.format(
                    'ON' if spec.satisfies('applications=all') else 'OFF'),
                '-DGUNROCK_APP_BC={0}'.format(
                    'ON' if spec.satisfies('applications=bc') else 'OFF'),
                '-DGUNROCK_APP_BFS={0}'.format(
                    'ON' if spec.satisfies('applications=bfs') else 'OFF'),
                '-DGUNROCK_APP_CC={0}'.format(
                    'ON' if spec.satisfies('applications=cc') else 'OFF'),
                '-DGUNROCK_APP_PR={0}'.format(
                    'ON' if spec.satisfies('applications=pr') else 'OFF'),
                '-DGUNROCK_APP_SSSP={0}'.format(
                    'ON' if spec.satisfies('applications=sssp') else 'OFF'),
                '-DGUNROCK_APP_DOBFS={0}'.format(
                    'ON' if spec.satisfies('applications=dobfs') else 'OFF'),
                '-DGUNROCK_APP_HITS={0}'.format(
                    'ON' if spec.satisfies('applications=hits') else 'OFF'),
                '-DGUNROCK_APP_SALSA={0}'.format(
                    'ON' if spec.satisfies('applications=salsa') else 'OFF'),
                '-DGUNROCK_APP_MST={0}'.format(
                    'ON' if spec.satisfies('applications=mst') else 'OFF'),
                '-DGUNROCK_APP_WTF={0}'.format(
                    'ON' if spec.satisfies('applications=wtf') else 'OFF'),
                '-DGUNROCK_APP_TOPK={0}'.format(
                    'ON' if spec.satisfies('applications=topk') else 'OFF'),
            ])

        return args

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            install_tree('lib', prefix.lib)
            # bin dir is created only if tests/examples are built
            if '+tests' in spec:
                install_tree('bin', prefix.bin)
