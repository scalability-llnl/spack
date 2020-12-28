# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRfc3986(PythonPackage):
    """A Python implementation of RFC 3986 including
       validation and authority parsing."""

    homepage = "http://rfc3986.readthedocs.io/"
    url      = "https://pypi.io/packages/source/r/rfc3986/rfc3986-1.4.0.tar.gz"

    version('1.4.0', sha256='112398da31a3344dc25dbf477d8df6cb34f9278a94fee2625d89e4514be8bb9d')

    depends_on('py-setuptools', type='build')
    depends_on('py-wheel', type='build')

    variant('idna2008', default=False, description='Enable idna2008 Functionality')

    depends_on('py-idna', when='+idna2008')
