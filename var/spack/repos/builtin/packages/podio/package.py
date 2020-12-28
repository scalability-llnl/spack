# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Podio(CMakePackage):
    """PODIO, or plain-old-data I/O, is a C++ library to support the creation
    and handling of data models in particle physics."""

    homepage = "https://github.com/AIDASoft/podio"
    url      = "https://github.com/AIDASoft/podio/archive/v00-09-02.tar.gz"
    git      = "https://github.com/AIDASoft/podio.git"

    maintainers = ['vvolkl', 'drbenmorgan']

    tags = ["hep", "key4hep"]

    version('master', branch='master')
    version('0.13', sha256='e9cbd4e25730003d3706ad82e28b15cb5bdc524a78b0a26e90b89ea852101498')
    version('0.12', sha256='1729a2ce21e8b307fc37dfb9a9f5ae031e9f4be4992385cf99dba3e5fdf5323a')
    version('0.11', sha256='4b2765566a14f0ddece2c894634e0a8e4f42f3e44392addb9110d856f6267fb6')
    version('0.10', sha256='b5b42770ec8b96bcd2748abc05669dd3e4d4cc84f81ed57d57d2eda1ade90ef2')
    version('0.9.2', sha256='8234d1b9636029124235ef81199a1220968dcc7fdaeab81cdc96a47af332d240')
    version('0.9', sha256='3cde67556b6b76fd2d004adfaa3b3b6173a110c0c209792bfdb5f9353e21076f')
    version('0.8', sha256='9d035a7f5ebfae5279a17405003206853271af692f762e2bac8e73825f2af327')

    variant('build_type', default='Release',
            description='The build type to build',
            values=('Debug', 'Release'))

    variant('sio', default=False,
            description='Build the SIO I/O backend')

    # cpack config throws an error on some systems
    patch('cpack.patch', when="@:0.10.0")
    patch('dictloading.patch', when="@0.10.0")

    depends_on('root@6.08.06: cxxstd=17')

    depends_on('cmake@3.8:', type='build')
    depends_on('python', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-jinja2@2.10.1:', type=('build', 'run'), when='@0.12.0:')
    depends_on('sio', type=('build', 'run'), when='+sio')

    conflicts('+sio', when='@:0.12', msg='sio support requires at least podio@0.13')

    def cmake_args(self):
        args = [
            self.define_from_variant('ENABLE_SIO', 'sio')
        ]
        return args

    def setup_run_environment(self, env):
        env.prepend_path('PYTHONPATH', self.prefix.python)

    def url_for_version(self, version):
        """Translate version numbers to ilcsoft conventions.
        in spack, the convention is: 0.1 (or 0.1.0) 0.1.1, 0.2, 0.2.1 ...
        in ilcsoft, releases are dashed and padded with a leading zero
        the patch version is omitted when 0
        so for example v01-12-01, v01-12 ...
        :param self: spack package class that has a url
        :type self: class: `spack.package_base.PackageBase`
        :param version: version
        :type param: str
        """
        base_url = self.url.rsplit('/', 1)[0]

        if len(version) == 1:
            major = version[0]
            minor, patch = 0, 0
        elif len(version) == 2:
            major, minor = version
            patch = 0
        else:
            major, minor, patch = version

        # By now the data is normalized enough to handle it easily depending
        # on the value of the patch version
        if patch == 0:
            version_str = 'v%02d-%02d.tar.gz' % (major, minor)
        else:
            version_str = 'v%02d-%02d-%02d.tar.gz' % (major, minor, patch)

        return base_url + '/' + version_str
