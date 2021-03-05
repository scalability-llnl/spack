# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
#   Spack Project Developers. See the top-level COPYRIGHT file for details.
# Copyright 2019-2021 GSI Helmholtz Centre for Heavy Ion Research GmbH,
#   Darmstadt, Germany
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dds(CMakePackage):
    """The Dynamic Deployment System (DDS)
       A tool-set that automates and significantly simplifies a deployment
       of user defined processes and their dependencies on any resource
       management system using a given topology.
    """

    homepage = "http://dds.gsi.de"
    git = "https://github.com/FairRootGroup/DDS"
    maintainers = ['dennisklein', 'ChristianTackeGSI']

    version('develop', branch='master', get_full_repo=True)
    version('3.5.4', commit='892e68d5acf07f6dd5877f0c8b1c84bd6bb40bda', no_cache=True)
    version('3.5.3', commit='f1eae89fdff266be86ec962c19e1c7930baf002c', no_cache=True)
    version('3.5.2', tag='3.5.2', commit='0813fd5772d1836c055370f4f16d46c961aa0d19', no_cache=True)
    version('3.4', tag='3.4', commit='e0900e946069d840c76e00f29113fd56158fdaa4', no_cache=True)
    version('3.2', tag='3.2', commit='03efdc71eb9aa35091ed1fbc41680c44e2ac7f54', no_cache=True)
    version('3.0', tag='3.0', commit='8b00716622962929ab4e19d0bb13e761d955fd87', no_cache=True)
    version('2.5-odc', tag='2.5-odc', commit='77d8452e15b390eaa6314c78c6073c3a9d687202', no_cache=True)
    version('2.4', tag='2.4', commit='7499753bdec9b5ed2468a712e57c5578ca25e7a6', no_cache=True)
    version('2.2', tag='2.2', commit='7c633d61d011af6e38c591152d77a979f841ce8c', no_cache=True)
    # TODO Once https://github.com/spack/spack/issues/14344 is resolved, enable
    #      source caching again (by removing the `no_cache` argument).

    patch('fix_wn_bin_2.2.patch', when='@2.2')
    patch('fix_wn_bin_2.4.patch', when='@2.4')
    patch('fix_wn_bin_2.5-odc.patch', when='@2.5-odc')
    patch('fix_wn_bin_3.0.patch', when='@3.0')
    patch('fix_wn_bin_3.2_3.5.2.patch', when='@3.2:3.5.2')
    patch('fix_wn_bin_3.5.3.patch', when='@3.5.3')
    patch('fix_wn_bin_3.5.4.patch', when='@3.5.4')
    patch('fix_wn_bin_master.patch', when='@develop')
    # TODO Upstream the wn_bin fix
    patch('fix_uuid_init.patch', when='@2.5-odc:3.0')

    depends_on('boost +shared+log+thread+program_options+filesystem+system+regex+test', when='@2.4:')
    depends_on('boost@1.67:1.72', when='@2.4:3.5.3')
    depends_on('boost@1.67:1.75', when='@3.5.4:')
    depends_on('boost@1.67:1.68 +shared+log+thread+program_options+filesystem+system+regex+test+signals', when='@:2.3')
    conflicts('^boost@1.70:', when='^cmake@:3.14')

    depends_on('cmake@3.16:', type='build')
    depends_on('cmake@3.18:', type='build', when='os=bigsur')
    depends_on('git', type='build')

    variant('cxxstd', default='default',
            values=('default', '11', '14', '17'),
            multi=False,
            description='Force the specified C++ standard when building.')
    conflicts('cxxstd=11', when='@3.5.4:')
    conflicts('cxxstd=14', when='@3.5.4:')

    build_targets = ['all', 'wn_bin']

    def cmake_args(self):
        args = []
        if self.spec.satisfies('@:2.5'):
            args.append('-DBUILD_SHARED_LIBS=ON')
        cxxstd = self.spec.variants['cxxstd'].value
        if cxxstd != 'default':
            args.append('-DCMAKE_CXX_STANDARD=%s' % cxxstd)
        if self.spec.satisfies('^boost@:1.69.99'):
            args.append('-DBoost_NO_BOOST_CMAKE=ON')
        return args
