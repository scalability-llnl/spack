# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyudev(PythonPackage):
    """Pure Python libudev binding"""

    homepage = "https://pyudev.readthedocs.io/en/latest/"
    pypi = "pyudev/pyudev-0.9.tar.gz"

    license("LGPL-2.1+")

    version("0.21.0", sha256="094b7a100150114748aaa3b70663485dd360457a709bfaaafe5a977371033f2b")
    version("0.15", sha256="12f462b777388c447edaac9e4b423a38a76eeb43f36b1a42288e771309d663c2")
    version("0.9", sha256="5282ff7178942cfe0cb56316b7743ad6d0189e2749d80f452bf2e04740b81eb2")

    depends_on("py-setuptools", type="build")
