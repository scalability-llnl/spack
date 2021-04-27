# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyFisher(PythonPackage):
    """Fisher's Exact Test.

    Simple, fast implementation of Fisher's exact test."""

    homepage = "https://github.com/brentp/fishers_exact_test"
    pypi = "fisher/fisher-0.1.9.tar.gz"

    version('0.1.9', sha256='d378b3f7e488e2a679c6d0e5ea1bce17bc931c2bfe8ec8424ee47a74f251968d')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy',      type=('build', 'run'))
