# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPycrypto(PythonPackage):
    """The Python Cryptography Toolkit"""

    homepage = "https://www.dlitz.net/software/pycrypto/"
    pypi = "pycrypto/pycrypto-2.6.1.tar.gz"

    version("2.6.1", sha256="f2ce1e989b272cfcb677616763e0a2e7ec659effa67a88aa92b3a65528f60a3c")

    depends_on("c", type="build")  # generated

    # depends_on('py-setuptools', type='build')
    depends_on("gmp")
