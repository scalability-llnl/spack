# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyDiskcache(PythonPackage):
    """Disk Cache -- Disk and file backed persistent cache."""

    homepage = "http://www.grantjenks.com/docs/diskcache/"
    url      = "https://pypi.io/packages/source/d/diskcache/diskcache-4.1.0.tar.gz"

    version('4.1.0', sha256='bcee5a59f9c264e2809e58d01be6569a3bbb1e36a1e0fb83f7ef9b2075f95ce0')

    depends_on('py-setuptools', type='build')
