# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Lcio(CMakePackage):
    """HEP Library for Linear Collider Input/Output"""

    homepage = "http://lcio.desy.de"
    git      = "https://github.com/iLCSoft/LCIO.git"
    url      = "https://github.com/iLCSoft/LCIO/archive/v02-13-03.tar.gz"

    tags = ['hep']

    maintainers = ['gaede', 'vvolkl']

    version('master', branch='master')
    version('2.16.1', sha256='992a649f864785e62fe12d7a638b2696c91f9535881de33f22b3cceabcdcdbaf')
    version('2.16',   sha256='aff7707750d821f31cbae3d7529fd8e22457f48d759e834ec01aa9389b5dbf1a')
    version('2.15.4', sha256='720c8130762d445df44d2c245da01c0a1ca807d7ed62362cebf7b3a99f9a37d7')
    version('2.15.3', sha256='a00f9e1e8fc98151e88e603bbfca8088ded21ae3daca5c91869628a19af0cefb')
    version('2.15.2', sha256='9886c6f5c275c1c51bde978e4f5514bb4ea9588239f1d3ee95a76ef4b686e69d')
    version('2.15.1', sha256='32921feb162408357d00a81cdd489c374b3ed8ab6f442d798b22835de7243d32')
    version('2.15',   sha256='27ea161a36ca93bf6b11381b63e90d100d3aeda3a00377bebcf2972c436aa3a7')
    version('2.14.2', sha256='e64f4bf932edf6d6cdaf0162e5104f8fbf3e5fd9737c7a080c48859009621919')
    version('2.14.1', sha256='ef670b10b6a01649fd4f3afcf38cbbee4cd83133612f922977260a6fea2bf30f')
    version('2.14',   sha256='85a7da4873b3501887d371cb8d993cb9f373323b190a8d523ad91b900a5f1284')
    version('2.13.3', sha256='35aaa7989be33574a7c44ea7e6d7780ab26ef8bd4aa29d495f3831a3cd269304')
    version('2.13.2', sha256='9f153ba13e56ee16795378f9192678d40df1faca51d00aaa8fb80547bfecb8d8')
    version('2.13.1', sha256='aa572e2ba38c0cadd6a92fa933c3ed97e21d016c7982578d3f293901169f4ec0')

    variant('cxxstd',
            default='17',
            values=('11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')
    variant("jar", default=False,
            description="Turn on to build/install lcio.jar")
    variant("rootdict", default=True,
            description="Turn on to build/install ROOT dictionary.")
    variant("examples", default=False,
            description="Turn on to build LCIO examples")

    depends_on('sio@0.0.2:', when='@2.14:')
    depends_on('sio@0.1:', when='@2.16:')

    depends_on('root@6.04:', when="+rootdict")
    depends_on('openjdk', when="+jar")
    # build error with +termlib, to be investigated
    depends_on('ncurses~termlib', when="+examples")
    depends_on('delphes', when="+examples")
    depends_on('readline', when="+examples")

    def cmake_args(self):
        args = [
            self.define('CMAKE_CXX_STANDARD',
                        self.spec.variants['cxxstd'].value),
            self.define('BUILD_TESTING', self.run_tests),
            self.define_from_variant("BUILD_LCIO_EXAMPLES", 'examples'),
            self.define_from_variant("BUILD_ROOTDICT", 'rootdict'),
            self.define_from_variant("INSTALL_JAR", 'jar'),
        ]
        return args

    def url_for_version(self, version):
        base_url = self.url.rsplit('/', 1)[0]
        major = str(version[0]).zfill(2)
        minor = str(version[1]).zfill(2)
        # handle the different cases for the patch version:
        # first case, no patch version is given in spack, i.e 0.1
        if len(version) == 2:
            url = base_url + "/v%s-%s.tar.gz" % (major, minor)
        # a patch version is specified in spack, i.e. 0.1.x ...
        elif len(version) == 3:
            patch = str(version[2]).zfill(2)
            # ... but it is zero, and not part of the ilc release url
            if version[2] == 0:
                url = base_url + "/v%s-%s.tar.gz" % (major, minor)
            # ... if it is non-zero, it is part  of the release url
            else:
                url = base_url + "/v%s-%s-%s.tar.gz" % (major, minor, patch)
        else:
            print('Error - Wrong version format provided')
            return
        return url

    def setup_run_environment(self, env):
        env.set('LCIO', self.prefix)
        env.prepend_path('PYTHONPATH', self.prefix.python)
        # needed for the python bindings to find "Exceptions.h"
        env.prepend_path('CPATH', self.prefix)

    @run_after('install')
    def install_source(self):
        # these files are needed for the python bindings and root to
        # find the headers
        install_tree('src/cpp/include/pre-generated/',
                     self.prefix.include + '/pre-generated')
        install('src/cpp/include/IOIMPL/LCEventLazyImpl.h',
                self.prefix.include + '/IOIMPL/')
