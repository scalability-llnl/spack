# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLibconf(PythonPackage):
    """A pure-Python libconfig reader/writer with permissive license"""

    homepage = "https://pypi.python.org/pypi/libconf"
    url      = "https://pypi.io/packages/source/l/libconf/libconf-1.0.1.tar.gz"

    version('1.0.1', sha256='6dd62847bb69ab5a09155cb8be2328cce01e7ef88a35e7c37bea2b1a70f8bd58')

    depends_on('py-setuptools', type='build')
