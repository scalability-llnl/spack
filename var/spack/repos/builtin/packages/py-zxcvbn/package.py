# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyZxcvbn(PythonPackage):
    """A realistic password strength estimator.

    This is a Python implementation of the library created by the team at
    Dropbox."""

    homepage = "https://github.com/dwolfhub/zxcvbn-python"
    url = "https://github.com/dwolfhub/zxcvbn-python/archive/v4.4.25.tar.gz"

    license("MIT")

    version("4.4.28", sha256="b7275765acdf8028c21aa502d742e56de2252bac604c04ba5e336c39f88d5576")
    version("4.4.27", sha256="9b84927fff7b4cc557b63a49adbd74f7a92026e25edd9e1b2867c1610d15fa5d")
    version("4.4.26", sha256="ee498e9257742972950f33540f0e36112db14c636417ce5b53d99a492dad8aba")
    version("4.4.25", sha256="dfb4d5aee8b59361572e2c12e7982bb22dbf9a1e8ac1c10c8ffea2c72712aabf")

    depends_on("py-setuptools", type="build")
