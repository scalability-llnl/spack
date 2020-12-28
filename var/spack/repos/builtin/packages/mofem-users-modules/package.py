# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class MofemUsersModules(CMakePackage):
    """MofemUsersModules creates installation environment for user-provided
    modules and extends of mofem-cephas package. For more information how to
    work with Spack and MoFEM see
    http://mofem.eng.gla.ac.uk/mofem/html/install_spack.html"""

    homepage = "http://mofem.eng.gla.ac.uk"
    git = "https://likask@bitbucket.org/mofem/users-modules-cephas.git"

    version('develop', branch='develop')
    version('0.8.17', commit='60b2341f1635f595d571096dd8c70a7cf7538aeb')
    version('0.8.16', commit='f6af51ad7db5b5dbc9d9acc6e753277a857c9f24')
    version('0.8.15', commit='4843b2d92ec21ad100a8d637698f56b3a2e14af3')
    version('0.8.14', commit='cfaa32133c574a31beaeb36202d033280521ddff')
    version('0.8.12', commit='7b2ce5595a95d1b919f50103513c44bb2bc9e6d2')
    version('0.8.11', commit='329b06d758137f1ec830f157d383b5ea415963de')
    version('0.8.10', commit='ca03a8222b20f9c8ff93a2d6f4c3babbcfde2058')
    version('0.8.8', commit='eb40f3c218badcd528ab08ee952835fb2ff07fd3')
    version('0.8.7', commit='a83b236f26f258f4d6bafc379ddcb9503088df56')

    maintainers = ['likask']

    variant('copy_user_modules', default=True,
            description='Copy user modules directory instead linking')

    extends('mofem-cephas')
    depends_on('mofem-cephas@0.8.17', when='@0.8.17')
    depends_on('mofem-cephas@0.8.16', when='@0.8.16')
    depends_on('mofem-cephas@0.8.15', when='@0.8.15')
    depends_on('mofem-cephas@0.8.14', when='@0.8.14')
    depends_on('mofem-cephas@0.8.12:0.8.13', when='@0.8.12')
    depends_on('mofem-cephas@0.8.11', when='@0.8.11')
    depends_on('mofem-cephas@0.8.10', when='@0.8.10')
    depends_on('mofem-cephas@0.8.8:0.8.9', when='@0.8.8')
    depends_on('mofem-cephas@0.8.7', when='@0.8.7')
    depends_on('mofem-cephas@develop', when='@develop')

    def cmake_args(self):
        spec = self.spec

        options = []

        # obligatory options
        options.extend([
            '-DMOFEM_DIR=%s' % spec['mofem-cephas'].prefix.users_module,
            '-DWITH_SPACK=YES',
            '-DSTAND_ALLONE_USERS_MODULES=%s' %
            ('YES' if '+copy_user_modules' in spec else 'NO')])

        # build tests
        options.append('-DMOFEM_UM_BUILD_TESTS={0}'.format(
            'ON' if self.run_tests else 'OFF'))

        return options

    # This function is not needed to run code installed by extension, nor in
    # the install process. However, the source code of users modules is
    # necessary to compile other sub-modules. Also, for users like to have
    # access to source code to play, change and make it. Having source code at
    # hand one can compile in own build directory it in package view when the
    # extension is activated.
    @run_after('install')
    def copy_source_code(self):
        source = self.stage.source_path
        prefix = self.prefix
        install_tree(source, prefix.users_modules)
