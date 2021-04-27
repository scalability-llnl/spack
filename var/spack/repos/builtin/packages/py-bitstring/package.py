# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyBitstring(PythonPackage):
    """Simple construction, analysis and modification of binary data."""

    homepage = "http://pythonhosted.org/bitstring"
    pypi = "bitstring/bitstring-3.1.5.zip"

    version('3.1.5', sha256='c163a86fcef377c314690051885d86b47419e3e1770990c212e16723c1c08faa')
