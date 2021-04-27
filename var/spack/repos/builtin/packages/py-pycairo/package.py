# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.pkgkit import *


class PyPycairo(PythonPackage):
    """Pycairo is a set of Python bindings for the cairo graphics library."""

    homepage = "https://www.cairographics.org/pycairo/"
    pypi = "pycairo/pycairo-1.17.1.tar.gz"

    version('1.20.0', sha256='5695a10cb7f9ae0d01f665b56602a845b0a8cb17e2123bfece10c2e58552468c')
    version('1.18.1', sha256='70172e58b6bad7572a3518c26729b074acdde15e6fee6cbab6d3528ad552b786')
    version('1.17.1', sha256='0f0a35ec923d87bc495f6753b1e540fd046d95db56a35250c44089fbce03b698')

    depends_on('cairo@1.15.10: +pdf', when='@1.20.0:')
    depends_on('cairo@1.13.1: +pdf', when='@:1.18.1')
    depends_on('pkgconfig', type='build')
    depends_on('py-setuptools', type='build')
    depends_on('python@2.7:2.8,3.3:', when='@:1.17.1',  type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:3.7.999', when='@1.18.1:1.19.999', type=('build', 'run'))
    depends_on('python@3.6:3.999', when='@1.20.0:', type=('build', 'run'))

    @run_after('install')
    def post_install(self):
        src = self.prefix.lib + '/pkgconfig/py3cairo.pc'
        dst = self.prefix.lib + '/pkgconfig/pycairo.pc'
        if os.path.exists(src) and not os.path.exists(dst):
            copy(src, dst)
