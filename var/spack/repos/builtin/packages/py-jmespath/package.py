# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJmespath(PythonPackage):
    """JSON Matching Expressions."""

    homepage = "https://github.com/jmespath/jmespath.py"
    url      = "https://pypi.io/packages/source/j/jmespath/jmespath-0.9.4.tar.gz"

    version('0.9.4', sha256='bde2aef6f44302dfb30320115b17d030798de8c4110e28d5cf6cf91a7a31074c')

    depends_on('py-setuptools', type='build')
