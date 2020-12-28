# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Edm4hep(CMakePackage):
    """Event data model of Key4hep."""

    homepage = "https://github.com/key4hep/EDM4hep"
    url = "https://github.com/key4hep/EDM4hep/archive/v00-01.tar.gz"
    git = "https://github.com/key4hep/EDM4hep.git"

    maintainers = ['vvolkl']

    tags = ["hep", "key4hep"]

    version('master', branch='master')
    version('0.3', sha256='d0ad8a486c3ed1659ea97d47b268fe56718fdb389b5935f23ba93804e4d5fbc5')

    variant('cxxstd',
            default='17',
            values=('17',),
            multi=False,
            description='Use the specified C++ standard when building.')

    depends_on('cmake@3.3:', type='build')
    depends_on('python', type='build')

    depends_on('root@6.08:')
    depends_on('podio@0.13:')

    depends_on('hepmc@:2.99.99', type='test')
    depends_on('heppdt', type='test')

    def cmake_args(self):
        args = []
        # C++ Standard
        args.append(self.define('CMAKE_CXX_STANDARD',
                    self.spec.variants['cxxstd'].value))
        return args

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
