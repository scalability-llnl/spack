# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHttplib2(PythonPackage):
    """A comprehensive HTTP client library."""

    homepage = "https://github.com/httplib2/httplib2"
    url      = "https://pypi.io/packages/source/h/httplib2/httplib2-0.13.1.tar.gz"

    version('0.13.1', sha256='6901c8c0ffcf721f9ce270ad86da37bc2b4d32b8802d4a9cec38274898a64044')

    depends_on('py-setuptools', type='build')
