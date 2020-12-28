# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIniparse(PythonPackage):
    """Accessing and Modifying INI files"""

    homepage = "https://github.com/candlepin/python-iniparse"
    url      = "https://pypi.io/packages/source/i/iniparse/iniparse-0.4.tar.gz"
    git      = "https://github.com/candlepin/python-iniparse.git"

    version('master', branch='master')
    version('0.4', sha256='abc1ee12d2cfb2506109072d6c21e40b6c75a3fe90a9c924327d80bc0d99c054')

    depends_on('python@2.4:2.8', when='@:0.4', type=('build', 'run'))
    depends_on('python@2.6:2.8,3.3:', when='@master:', type=('build', 'run'))
