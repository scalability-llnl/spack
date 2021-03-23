# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Xrootd(CMakePackage):
    """The XROOTD project aims at giving high performance, scalable fault
       tolerant access to data repositories of many kinds."""
    homepage = "http://xrootd.org"
    url      = "http://xrootd.org/download/v5.0.1/xrootd-5.0.1.tar.gz"

    version('5.1.0', sha256='c639536f1bdc5b6b365e807f3337ed2d41012cd3df608d40e91ed05f1c568b6d')
    version('5.0.3', sha256='be40a1897d6c1f153d3e23c39fe96e45063bfafc3cc073db88a1a9531db79ac5')
    version('5.0.1', sha256='ff4462b0b61db4cc01dda0e26abdd78e43649ee7ac5e90f7a05b74328ff5ac83')
    version('4.12.6', sha256='1a9056ab7aeeaafa586ea77e442960c71d233c9ba60c7f9db9262c1410954ac4')
    version('4.12.3', sha256='6f2ca1accc8d49d605706bb556777c753860bf46d845b1ee11393a5cb5987f15')
    version('4.12.2', sha256='29f7bc3ea51b9d5d310eabd177152245d4160223325933c67f938ed5120f67bb')
    version('4.12.1', sha256='7350d9196a26d17719b839fd242849e3995692fda25f242e67ac6ec907218d13')
    version('4.12.0', sha256='69ef4732256d9a88127de4bfdf96bbf73348e0c70ce1d756264871a0ffadd2fc')
    version('4.11.3', sha256='8e7a64fd55dfb452b6d5f76a9a97c493593943227b377623a3032da9197c7f65')
    version('4.11.2', sha256='4620824db97fcc37dc3dd26110da8e5c3aab1d8302e4921d4f32e83207060603')
    version('4.10.0', sha256='f07f85e27d72e9e8ff124173c7b53619aed8fcd36f9d6234c33f8f7fd511995b')
    version('4.8.5',  sha256='42e4d2cc6f8b442135f09bcc12c7be38b1a0c623a005cb5e69ff3d27997bdf73')
    version('4.8.4',  sha256='f148d55b16525567c0f893edf9bb2975f7c09f87f0599463e19e1b456a9d95ba')
    version('4.8.3',  sha256='9cd30a343758b8f50aea4916fa7bd37de3c37c5b670fe059ae77a8b2bbabf299')
    version('4.8.2',  sha256='8f28ec53e799d4aa55bd0cc4ab278d9762e0e57ac40a4b02af7fc53dcd1bef39')
    version('4.8.1',  sha256='edee2673d941daf7a6e5c963d339d4a69b4db5c4b6f77b4548b3129b42198029')
    version('4.8.0',  sha256='0b59ada295341902ca01e9d23e29780fb8df99a6d2bd1c2d654e9bb70c877ad8')
    version('4.7.1',  sha256='90ddc7042f05667045b06e02c8d9c2064c55d9a26c02c50886254b8df85fc577')
    version('4.7.0',  sha256='6cc69d9a3694e8dcf2392e9c3b518bd2497a89b3a9f25ffaec62efa52170349b')
    version('4.6.1',  sha256='0261ce760e8788f85d68918d7702ae30ec677a8f331dae14adc979b4cc7badf5')
    version('4.6.0',  sha256='b50f7c64ed2a4aead987de3fdf6fce7ee082407ba9297b6851cd917db72edd1d')
    version('4.5.0',  sha256='27a8e4ef1e6bb6bfe076fef50afe474870edd198699d43359ef01de2f446c670')
    version('4.4.1',  sha256='3c295dbf750de086c04befc0d3c7045fd3976611c2e75987c1477baca37eb549')
    version('4.4.0',  sha256='f066e7488390c0bc50938d23f6582fb154466204209ca92681f0aa06340e77c8')
    version('4.3.0',  sha256='d34865772d975b5d58ad80bb05312bf49aaf124d5431e54dc8618c05a0870e3c')

    variant('http', default=True,
            description='Build with HTTP support')

    variant('python', default=False,
            description='Build pyxroot Python extension')

    variant('readline', default=True,
            description='Use readline')

    variant('cxxstd',
            default='11',
            values=('98', '11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    conflicts('cxxstd=98', when='@4.7.0:')

    depends_on('bzip2')
    depends_on('cmake@2.6:', type='build')
    depends_on('libxml2', when='+http')
    depends_on('uuid', when="@4.11.0:")
    depends_on('openssl')
    depends_on('python', when='+python')
    depends_on('readline', when='+readline')
    depends_on('xz')
    depends_on('zlib')

    extends('python', when='+python')
    patch('python-support.patch', level=1, when='@:4.8.99+python')

    def patch(self):
        """Remove hardcoded -std=c++0x flag
        """
        if self.spec.satisfies('@4.7.0:'):
            filter_file(r'\-std=c\+\+0x', r'', 'cmake/XRootDOSDefs.cmake')

    def cmake_args(self):
        spec = self.spec
        options = [
            '-DENABLE_HTTP:BOOL={0}'.
            format('ON' if '+http' in spec else 'OFF'),
            '-DENABLE_PYTHON:BOOL={0}'.
            format('ON' if '+python' in spec else 'OFF'),
            '-DENABLE_READLINE:BOOL={0}'.
            format('ON' if '+readline' in spec else 'OFF'),
            '-DENABLE_CEPH:BOOL=OFF'
        ]
        # see https://github.com/spack/spack/pull/11581
        if '+python' in self.spec:
            options.append('-DPYTHON_EXECUTABLE=%s' %
                           spec['python'].command.path)

        return options

    def setup_build_environment(self, env):
        cxxstdflag = ''
        if self.spec.variants['cxxstd'].value == '98':
            cxxstdflag = self.compiler.cxx98_flag
        elif self.spec.variants['cxxstd'].value == '11':
            cxxstdflag = self.compiler.cxx11_flag
        elif self.spec.variants['cxxstd'].value == '14':
            cxxstdflag = self.compiler.cxx14_flag
        elif self.spec.variants['cxxstd'].value == '17':
            cxxstdflag = self.compiler.cxx17_flag
        else:
            # The user has selected a (new?) legal value that we've
            # forgotten to deal with here.
            tty.die(
                "INTERNAL ERROR: cannot accommodate unexpected variant ",
                "cxxstd={0}".format(self.spec.variants['cxxstd'].value))

        if cxxstdflag:
            env.append_flags('CXXFLAGS', cxxstdflag)
