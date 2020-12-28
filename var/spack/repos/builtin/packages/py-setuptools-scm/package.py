# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySetuptoolsScm(PythonPackage):
    """The blessed package to manage your versions by scm tags."""

    homepage = "https://github.com/pypa/setuptools_scm"
    url      = "https://pypi.io/packages/source/s/setuptools_scm/setuptools_scm-4.1.2.tar.gz"

    version('4.1.2',  sha256='a8994582e716ec690f33fec70cca0f85bd23ec974e3f783233e4879090a7faa8')
    version('3.3.3',  sha256='bd25e1fb5e4d603dcf490f1fde40fb4c595b357795674c3e5cb7f6217ab39ea5')
    version('3.1.0',  sha256='1191f2a136b5e86f7ca8ab00a97ef7aef997131f1f6d4971be69a1ef387d8b40')
    version('1.15.6', sha256='49ab4685589986a42da85706b3311a2f74f1af567d39fee6cb1e088d7a75fb5f')

    variant('toml', default=False, description='Build with TOML support')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.5:', when='@4:', type=('build', 'run'))
    depends_on('py-setuptools@34.4:', type=('build', 'run'))
    depends_on('py-toml', when='+toml', type=('build', 'run'))
