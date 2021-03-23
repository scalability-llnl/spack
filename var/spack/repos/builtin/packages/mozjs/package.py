# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mozjs(AutotoolsPackage):
    """SpiderMonkey is Mozilla's JavaScript engine written in C/C++.
    It is used in various Mozilla products, including Firefox, and is
    available under the MPL2."""

    homepage = "https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey"

    version('24.2.0', sha256='e62f3f331ddd90df1e238c09d61a505c516fe9fd8c5c95336611d191d18437d8',
            url="http://ftp.mozilla.org/pub/js/mozjs-24.2.0.tar.bz2")
    version('17.0.0', sha256='321e964fe9386785d3bf80870640f2fa1c683e32fe988eeb201b04471c172fba',
            url="http://ftp.mozilla.org/pub/js/mozjs17.0.0.tar.gz")
    version('1.8.5',  sha256='5d12f7e1f5b4a99436685d97b9b7b75f094d33580227aa998c406bbae6f2a687',
            url="http://ftp.mozilla.org/pub/js/js185-1.0.0.tar.gz")

    depends_on('perl@5.6:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('python@2.7.3:2.8', type='build')
    depends_on('zip',  type='build')
    depends_on('unzip', type='build')
    depends_on('nspr', when='@:27')
    depends_on('libffi@3.0.9:')
    depends_on('readline', when='@17.0.0:')
    depends_on('zlib@1.2.3')

    configure_directory = 'js/src'
    build_directory = 'js/src/spack-build'

    patch('perl-bug.patch')
    # Note: According to https://github.com/apache/couchdb-pkg/tree/master/js/rpm/SOURCES
    #       There is some patch for mozjs@1.8.5 to fix compile issue.
    #       Patches required to fix the issue:https://bugzilla.mozilla.org/show_bug.cgi?id=638056
    patch('Bug-638056-Avoid-The-cacheFlush-support-is-missing-o.patch',
          sha256='b1c869a65f5ebc10741d4631cc2e1e166c6ed53035cfa56bede55a4c19b7b118', when='@1.8.5')
    patch('fix-811665.patch',
          sha256='2b298b8a693865b38e2b0d33277bb5ffe152c6ecf43648e85113fec586aa4752', when='@1.8.5')

    def configure_args(self):
        spec = self.spec
        config_args = [
            '--enable-readline',    # enables readline support in JS shell
            '--enable-threadsafe',  # enables support for multiple threads
            '--enable-system-ffi',
            '--with-system-zlib={0}'.format(spec['zlib'].prefix),
            '--with-system-nspr',
            '--with-nspr-prefix={0}'.format(spec['nspr'].prefix),
        ]
        if spec.target.family == 'aarch64':
            config_args.append('--host=aarch64-linux-gnu')
        if spec.satisfies('@1.8.5'):
            config_args.append('--disable-readline')
        return config_args
