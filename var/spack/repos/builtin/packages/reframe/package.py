# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import shutil


class Reframe(Package):
    """ReFrame is a framework for writing regression tests for HPC systems.
    The goal of this framework is to abstract away the complexity of the
    interactions with the system, separating the logic of a regression test
    from the low-level details, which pertain to the system configuration and
    setup. This allows users to write easily portable regression tests,
    focusing only on the functionality."""

    homepage = 'https://reframe-hpc.readthedocs.io'
    url      = 'https://github.com/eth-cscs/reframe/archive/v2.21.tar.gz'
    git      = 'https://github.com/eth-cscs/reframe.git'

    # notify when the package is updated.
    maintainers = ['victorusu', 'vkarak']

    version('master', branch='master')
    version('3.5.0',  sha256='81b501be4252c99f12043cb21b0b7b8059207a340fc94173b180444599773f1a')
    version('3.4.2',  sha256='0c5c6dbd234b8007be929be2ccbe6a00d9a5ec75cc86e129557590b83f71acca')
    version('3.4.1',  sha256='aed5752a2f687002839923c5432784d3a25d3a29d43b69122dcbf72befa0fdbf')
    version('3.4',    sha256='7e74b1c7468b94e89cff4cd4a91934645ab227ad61d57a9ddf6a7d3d0726010e')
    version('3.3',    sha256='9da150a051e9fa4ffea1361f30e8593261e7f6ebc71ec91ed32143539f871ad7')
    version('3.2',    sha256='dc7f72e31386e549a874699067666607a72835914fef18c38ae6032ab5e5ed51')
    version('3.1',    sha256='a9f6ac1ae8fdc51be8032d5cc79c117ff602f57b57aace2e195b2cfe1bd3a16f')
    version('3.0',    sha256='fb76b4513c03b84f5b3bbbc988f7747e5b58f04c983b3935bab1f2e81adccb82')
    version('2.21',   sha256='f35d4fda2f9672c87d3ef664d9a2d6eb0c01c88218a31772a6645c32c8934c4d')
    version('2.20',   sha256='310c18d705858bbe6bd9a2dc4d382b254c1f093b0671d72363f2111e8c162ba4')
    version('2.17.3', sha256='dc8dfb2ccb9a966303879b7cdcd188c47063e9b7999cbd5d6255223b066bf357')
    version('2.17.2', sha256='092241cdc15918040aacb922c806aecb59c5bdc3ff7db034a4f355d39aecc101')
    version('2.17.1', sha256='0b0d32a892607840a7d668f5dcea6f03f7022a26b23e5042a0faf5b8c41cb146')

    variant('docs', default=False,
            description='Build ReFrame\'s man page documentation')
    variant('gelf', default=False,
            description='Add graylog handler support')

    # ReFrame requires git up to version 3.1, see:
    # https://github.com/eth-cscs/reframe/issues/1464
    depends_on('git', when='@2.0:3.1', type='run')

    # supported python versions
    depends_on('python@3.5:', when='@2.0:2.999', type='run')
    depends_on('python@3.6:', when='@3.0:', type='run')

    # build dependencies
    depends_on('py-setuptools', type='build')

    # runtime dependencies
    depends_on('py-argcomplete', when='@3.4.1:', type='run')
    depends_on('py-importlib-metadata', type='run')
    depends_on('py-jsonschema', type='run')
    depends_on('py-pyyaml', when='@3.4.1:', type='run')
    depends_on('py-requests', when='@3.4.1:', type='run')
    depends_on('py-semver', when='@3.4.2:', type='run')

    # extension dependencies
    depends_on('py-pygelf', when='+gelf', type='run')

    # documentation dependencies
    depends_on('py-sphinx', when='+docs', type='build')
    depends_on('py-sphinx-rtd-theme', when='+docs', type='build')

    # sanity check
    sanity_check_is_file = ['bin/reframe']
    sanity_check_is_dir  = ['bin', 'config', 'docs', 'reframe', 'tutorials',
                            'unittests', 'cscs-checks']

    # check if we can run reframe
    @run_after('install')
    @on_package_attributes(run_tests=True)
    def check_list(self):
        with working_dir(self.stage.source_path):
            reframe = Executable(self.prefix + '/bin/reframe')
            reframe('-l')

    def install(self, spec, prefix):
        if spec.version >= Version('3.0'):
            if '+docs' in spec:
                with working_dir('docs'):
                    make('man')
                    make('html')
                    with working_dir('man'):
                        mkdir('man1')
                        shutil.move('reframe.1', 'man1')
                        mkdir('man8')
                        shutil.move('reframe.settings.8', 'man8')
        install_tree(self.stage.source_path, self.prefix)

    def setup_run_environment(self, env):
        if self.spec.version >= Version('3.0'):
            if '+docs' in self.spec:
                env.prepend_path('MANPATH',  self.prefix.docs.man)
