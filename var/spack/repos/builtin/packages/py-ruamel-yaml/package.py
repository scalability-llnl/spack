# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRuamelYaml(PythonPackage):
    """
    a YAML parser/emitter that supports roundtrip preservation of comments,
    seq/map flow style, and map key order
    """

    homepage = "https://sourceforge.net/p/ruamel-yaml/code/ci/default/tree"
    url      = "https://pypi.io/packages/source/r/ruamel.yaml/ruamel.yaml-0.16.10.tar.gz"

    version('0.16.10', sha256='099c644a778bf72ffa00524f78dd0b6476bca94a1da344130f4bf3381ce5b954')
    version('0.16.5',  sha256='412a6f5cfdc0525dee6a27c08f5415c7fd832a7afcb7a0ed7319628aed23d408')
    version('0.11.7',  sha256='c89363e16c9eafb9354e55d757723efeff8682d05e56b0881450002ffb00a344')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-ruamel-ordereddict', when='@0.15:^python@:2', type=('build', 'run'))
    depends_on('py-ruamel-yaml-clib@0.1.2:', when='@0.16:^python@:3.8', type=('build', 'run'))

    @run_after('install')
    def fix_import_error(self):
        if str(self.spec['python'].version.up_to(1)) == '2':
            touch = which('touch')
            touch(self.prefix + '/' +
                  self.spec['python'].package.site_packages_dir +
                  '/ruamel/__init__.py')
