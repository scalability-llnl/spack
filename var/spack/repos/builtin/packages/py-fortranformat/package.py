# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFortranformat(PythonPackage):
    """Mimics Fortran textual IO in Python"""

    homepage = "http://bitbucket.org/brendanarnold/py-fortranformat"
    url      = "https://pypi.io/packages/source/f/fortranformat/fortranformat-0.2.5.tar.gz"

    version('0.2.5', sha256='6b5fbc1f129c7a70543c3a81f334fb4d57f07df2834b22ce69f6d7e8539cd3f9')
