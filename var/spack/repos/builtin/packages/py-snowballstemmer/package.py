# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySnowballstemmer(PythonPackage):
    """This package provides 16 stemmer algorithms (15 + Poerter
    English stemmer) generated from Snowball algorithms."""

    homepage = "https://github.com/shibukawa/snowball_py"
    url      = "https://pypi.io/packages/source/s/snowballstemmer/snowballstemmer-2.0.0.tar.gz"

    version('2.0.0', sha256='df3bac3df4c2c01363f3dd2cfa78cce2840a79b9f1c2d2de9ce8d31683992f52')
    version('1.2.1', sha256='919f26a68b2c17a7634da993d91339e288964f93c274f1343e3bbbe2096e1128')

    depends_on('py-setuptools', when='@2:', type='build')
