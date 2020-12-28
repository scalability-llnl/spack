# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMacs2(PythonPackage):
    """MACS2 Model-based Analysis of ChIP-Seq"""

    homepage = "https://github.com/taoliu/MACS"
    url      = "https://pypi.io/packages/source/M/MACS2/MACS2-2.2.4.tar.gz"

    version('2.2.4',          sha256='b131aadc8f5fd94bec35308b821e1f7585def788d2e7c756fc8cac402ffee25b')
    version('2.1.4',          sha256='e4966d001914320829ab859c7bc8e92c6410aa7bdbddfd00b7625e9a0fb15c97')
    version('2.1.3.3',        sha256='00959e523f45ed92b8429f55944eca6984623ac008d7cdb488c3ffe59c21984a')
    version('2.1.1.20160309', sha256='2008ba838f83f34f8e0fddefe2a3a0159f4a740707c68058f815b31ddad53d26')

    depends_on('python@3.5:',    when='@2.2:', type=('build', 'run'))
    depends_on('python@2.7:2.8', when='@:2.1', type=('build', 'run'))
    depends_on('py-cython', type='build')

    # Most Python packages only require py-setuptools as a build dependency.
    # However, py-macs2 requires py-setuptools during runtime as well.
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-numpy@1.17:', when='@2.2:', type=('build', 'run'))
    depends_on('py-numpy@1.16:', type=('build', 'run'))
