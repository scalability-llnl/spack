# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost


class Cbtf(CMakePackage):
    """CBTF project contains the base code for CBTF that supports creating
       components, component networks and the support to connect these
       components and component networks into sequential and distributed
       network tools.

    """
    homepage = "http://sourceforge.net/p/cbtf/wiki/Home"
    git      = "https://github.com/OpenSpeedShop/cbtf.git"

    version('develop', branch='master')
    version('1.9.3', branch='1.9.3')
    version('1.9.2', branch='1.9.2')
    version('1.9.1.2', branch='1.9.1.2')
    version('1.9.1.1', branch='1.9.1.1')
    version('1.9.1.0', branch='1.9.1.0')

    variant('cti', default=False,
            description="Build MRNet with the CTI startup option")

    variant('runtime', default=False,
            description="build only the runtime libraries and collectors.")

    variant('build_type', default='None', values=('None',),
            description='CMake build type')

    depends_on("cmake@3.0.2:", type='build')

    # for rpcgen
    depends_on("rpcsvc-proto")

    # for rpc
    depends_on("libtirpc", type='link')

    depends_on("boost@1.66.0:1.69.0")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)

    # For MRNet
    depends_on("mrnet@5.0.1-3:+cti", when='@develop+cti')
    depends_on("mrnet@5.0.1-3:+lwthreads", when='@develop')
    depends_on("mrnet@5.0.1-3+cti", when='@1.9.1.0:9999+cti')
    depends_on("mrnet@5.0.1-3+lwthreads", when='@1.9.1.0:9999')

    # For Xerces-C
    depends_on("xerces-c")

    # For XML2
    depends_on("libxml2")

    parallel = False

    build_directory = 'build_cbtf'

    def cmake_args(self):

        spec = self.spec

        # Boost_NO_SYSTEM_PATHS  Set to TRUE to suppress searching
        # in system paths (or other locations outside of BOOST_ROOT
        # or BOOST_INCLUDEDIR).  Useful when specifying BOOST_ROOT.
        # Defaults to OFF.

        compile_flags = "-O2 -g"

        if spec.satisfies('+runtime'):

            # Install message tag include file for use in Intel MIC
            # cbtf-krell build
            # FIXME
            cmake_args = [
                '-DCMAKE_CXX_FLAGS=%s'     % compile_flags,
                '-DCMAKE_C_FLAGS=%s'       % compile_flags,
                '-DRUNTIME_ONLY=TRUE',
                '-DBoost_NO_SYSTEM_PATHS=TRUE',
                '-DXERCESC_DIR=%s'         % spec['xerces-c'].prefix,
                '-DBOOST_ROOT=%s'          % spec['boost'].prefix,
                '-DMRNET_DIR=%s'           % spec['mrnet'].prefix,
                '-DCMAKE_MODULE_PATH=%s'   % join_path(
                    prefix.share, 'KrellInstitute', 'cmake')]
        else:
            cmake_args = [
                '-DCMAKE_CXX_FLAGS=%s'     % compile_flags,
                '-DCMAKE_C_FLAGS=%s'       % compile_flags,
                '-DBoost_NO_SYSTEM_PATHS=TRUE',
                '-DXERCESC_DIR=%s'         % spec['xerces-c'].prefix,
                '-DBOOST_ROOT=%s'          % spec['boost'].prefix,
                '-DMRNET_DIR=%s'           % spec['mrnet'].prefix,
                '-DCMAKE_MODULE_PATH=%s'   % join_path(
                    prefix.share, 'KrellInstitute', 'cmake')]

        return cmake_args
