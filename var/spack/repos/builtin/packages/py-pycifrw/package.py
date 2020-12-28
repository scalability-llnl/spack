# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPycifrw(PythonPackage):
    """Python library for interacting with Crystallographic Information
    Framework (CIF) files."""

    homepage = "https://bitbucket.org/jamesrhester/pycifrw/src/development/"
    url      = "https://pypi.io/packages/source/P/PyCifRW/PyCifRW-4.4.1.tar.gz"

    version('4.4.1', sha256='cef7662f475e0eb78a55c2d55774d474e888c96b0539e5f08550afa902cdc4e1')

    depends_on('py-setuptools', type='build')
