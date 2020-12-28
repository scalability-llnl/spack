# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFuture(PythonPackage):
    """Clean single-source support for Python 3 and 2"""

    homepage = "https://python-future.org/"
    url = "https://pypi.io/packages/source/f/future/future-0.18.2.tar.gz"

    version('0.18.2', sha256='b1bead90b70cf6ec3f0710ae53a525360fa360d306a86583adc6bf83a4db537d')
    version('0.17.1', sha256='67045236dcfd6816dc439556d009594abf643e5eb48992e36beac09c2ca659b8')
    version('0.17.0', sha256='eb6d4df04f1fb538c99f69c9a28b255d1ee4e825d479b9c62fc38c0cf38065a4')
    version('0.16.0', sha256='e39ced1ab767b5936646cedba8bcce582398233d6a627067d4c6a454c90cfedb')
    version('0.15.2', sha256='3d3b193f20ca62ba7d8782589922878820d0a023b885882deec830adbf639b97')

    depends_on('py-setuptools', type='build')
    depends_on('py-importlib', type=('build', 'run'), when='^python@:2.6')
    depends_on('py-argparse', type=('build', 'run'), when='^python@:2.6')

    @property
    def import_modules(self):
        modules = [
            'copyreg', '_thread', 'past', 'past.types', 'past.translation',
            'past.utils', 'past.builtins', 'reprlib', 'html', 'builtins',
            'http', '_dummy_thread', 'queue', 'xmlrpc', 'libfuturize',
            'libfuturize.fixes', 'future', 'future.moves', 'future.moves.test',
            'future.moves.urllib', 'future.moves.html', 'future.moves.http',
            'future.moves.dbm', 'future.moves.xmlrpc', 'future.types',
            'future.tests', 'future.utils', 'future.builtins',
            'future.backports', 'future.backports.test',
            'future.backports.urllib', 'future.backports.html',
            'future.backports.http', 'future.backports.xmlrpc',
            'future.backports.email', 'future.backports.email.mime',
            'future.standard_library', 'libpasteurize', 'libpasteurize.fixes',
            'socketserver', '_markupbase'
        ]

        if 'platform=windows' in self.spec:
            modules.append('winreg')

        if '+tkinter' in self.spec['python']:
            modules.extend(['tkinter', 'future.moves.tkinter'])

        return modules
